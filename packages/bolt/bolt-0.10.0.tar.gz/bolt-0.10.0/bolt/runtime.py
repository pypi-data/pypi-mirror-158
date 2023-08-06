__all__ = [
    "Runtime",
    "Module",
    "CompiledModule",
    "ModuleCacheBackend",
    "GlobalsInjection",
    "ModuleRootParser",
    "Evaluator",
    "ModuleRootSerializer",
    "UnusableCompilationUnit",
]


import builtins
import logging
import marshal
from contextlib import contextmanager
from dataclasses import dataclass, field
from importlib.resources import read_text
from io import BufferedReader, BufferedWriter
from pathlib import Path
from types import CodeType
from typing import Any, Callable, Dict, Iterator, List, Optional, Set, Union

from beet import BubbleException, Context, TextFile, TextFileBase, generate_tree
from beet.core.utils import JsonDict, import_from_string, required_field
from mecha import (
    AstCacheBackend,
    AstCommand,
    AstRoot,
    CommandTree,
    CompilationDatabase,
    CompilationError,
    CompilationUnit,
    Diagnostic,
    DiagnosticCollection,
    Dispatcher,
    Mecha,
    MechaError,
    Parser,
    Visitor,
    rule,
)
from tokenstream import TokenStream, set_location

from .ast import AstModuleRoot
from .codegen import Codegen
from .helpers import get_bolt_helpers
from .loop_info import loop_info
from .parse import get_bolt_parsers
from .utils import internal, rewrite_traceback

logger = logging.getLogger("mecha")


class UnusableCompilationUnit(MechaError):
    """Raised when a compilation unit lacks the necessary information to instantiate a module."""

    message: str
    compilation_unit: CompilationUnit

    def __init__(self, message: str, compilation_unit: CompilationUnit) -> None:
        super().__init__(message, compilation_unit)
        self.message = message
        self.compilation_unit = compilation_unit

    def __str__(self) -> str:
        return self.message


class Module(TextFile):
    """Class representing a bolt module."""

    scope = ("modules",)
    extension = ".bolt"


@dataclass
class CompiledModule:
    """Class holding the state of a compiled module."""

    ast: AstRoot
    code: Optional[CodeType]
    refs: List[Any]
    output: Optional[str]
    resource_location: Optional[str]
    globals: Set[str]
    namespace: JsonDict = field(default_factory=dict)
    executing: bool = False
    executed: bool = False
    execution_hooks: List[Callable[[], Any]] = field(default_factory=list)


class Runtime:
    """The bolt runtime."""

    modules: Dict[TextFileBase[Any], CompiledModule]
    stack: List[CompiledModule]
    commands: List[AstCommand]
    helpers: Dict[str, Any]
    globals: JsonDict
    builtins: Set[str]

    directory: Path
    database: CompilationDatabase
    codegen: Codegen
    evaluate: Dispatcher[AstRoot]

    def __init__(self, ctx: Union[Context, Mecha]):
        self.modules = {}
        self.stack = []
        self.commands = []
        self.helpers = get_bolt_helpers()
        self.globals = {"ctx": None, "loop_info": loop_info}
        self.builtins = {name for name in dir(builtins) if not name.startswith("_")}

        if isinstance(ctx, Context):
            ctx.require(
                "mecha.contrib.relative_location",
                "mecha.contrib.inline_function_tag",
                "mecha.contrib.nesting",
                "mecha.contrib.nested_resources",
                "mecha.contrib.nested_yaml",
                "mecha.contrib.implicit_execute",
                self.finalize,
            )

            ctx.data.extend_namespace.append(Module)

            self.globals["ctx"] = ctx

            self.expose("generate_path", ctx.generate.path)
            self.expose("generate_id", ctx.generate.id)
            self.expose("generate_hash", ctx.generate.hash)
            self.expose("generate_objective", ctx.generate.objective)
            self.expose(
                "generate_tree",
                lambda *args, **kwargs: generate_tree(
                    kwargs.pop("root") if "root" in kwargs else self.get_path(),
                    *args,
                    name=(
                        kwargs.pop("name")
                        if "name" in kwargs
                        else ctx.generate["tree"][self.get_path()].format("tree_{incr}")
                    ),
                    **kwargs,
                ),
            )

            mc = ctx.inject(Mecha)

        else:
            mc = ctx

        mc.cache_backend = ModuleCacheBackend(runtime=self)

        commands_json = read_text("bolt.resources", "commands.json")
        mc.spec.add_commands(CommandTree.parse_raw(commands_json))
        mc.spec.parsers.update(get_bolt_parsers(mc.spec.parsers, mc.database))
        mc.spec.parsers["root"] = GlobalsInjection(
            runtime=self,
            parser=ModuleRootParser(mc.database, mc.spec.parsers["root"]),
        )

        mc.providers.append(Module)

        self.directory = mc.directory
        self.database = mc.database
        self.codegen = Codegen()

        self.evaluate = Evaluator(runtime=self)
        mc.steps.insert(0, self.evaluate)

        mc.serialize.extend(ModuleRootSerializer())

    def get_path(self) -> str:
        """Return the current path."""
        if not self.stack:
            raise ValueError("No module currently executing.")
        if path := self.stack[-1].resource_location:
            return path
        raise ValueError("No resource location corresponding to the current module.")

    def expose(self, name: str, function: Callable[..., Any]):
        """Expose a utility function."""
        self.globals[name] = lambda *args, **kwargs: function(*args, **kwargs)  # type: ignore

    def get_module(
        self,
        target: Optional[Union[AstRoot, str]] = None,
        current: Optional[TextFileBase[Any]] = None,
    ) -> CompiledModule:
        """Retrieve an executable module."""
        if self.stack and not target and not current:
            return self.stack[-1]

        if isinstance(target, str):
            current = self.database.index[target]
        elif current is None:
            current = self.database.current

        module = self.modules.get(current)
        compilation_unit = self.database[current]
        name = compilation_unit.resource_location or "<unknown>"

        if module:
            if isinstance(target, AstRoot) and module.ast is not target:
                logger.debug("Code generation due to ast update for module %s.", name)
            else:
                return module
        else:
            if not isinstance(target, AstRoot):
                target = compilation_unit.ast
                if not target:
                    raise UnusableCompilationUnit(
                        f"No ast for module {name}.", compilation_unit
                    )
            logger.debug("Code generation for module %s.", name)

        source, output, refs = self.codegen(target)

        if source and output:
            filename = (
                str(self.directory / compilation_unit.filename)
                if compilation_unit.filename
                else name
            )

            code = compile(source, filename, "exec")

        else:
            code = None

        module = CompiledModule(
            ast=target,
            code=code,
            refs=refs,
            output=output,
            resource_location=compilation_unit.resource_location,
            globals=set(self.globals),
        )
        self.modules[current] = module

        return module

    def get_output(self, module: CompiledModule) -> AstRoot:
        """Run the module and return the output ast."""
        if not module.executed:
            module.executed = True
            for hook in module.execution_hooks:
                hook()

        if not module.code or not module.output:
            return module.ast
        if module.output in module.namespace:
            return module.namespace[module.output]

        if module.executing:
            raise ValueError("Import cycle detected.")

        logger.debug("Evaluate module %s.", module.resource_location or "<unknown>")

        module.namespace.update(self.globals)
        module.namespace["_bolt_runtime"] = self
        module.namespace["_bolt_refs"] = module.refs
        module.namespace["__name__"] = module.resource_location
        module.namespace["__file__"] = module.code.co_filename

        self.stack.append(module)
        module.executing = True

        try:
            with self.error_handler():
                exec(module.code, module.namespace)
        finally:
            module.executing = False
            self.stack.pop()

        return module.namespace[module.output]

    @contextmanager
    def scope(
        self,
        commands: Optional[List[AstCommand]] = None,
    ) -> Iterator[List[AstCommand]]:
        """Create a new scope to gather commands."""
        if commands is None:
            commands = []

        previous_commands = self.commands
        self.commands = commands

        try:
            yield commands
        finally:
            self.commands = previous_commands

    @contextmanager
    def error_handler(self):
        """Handle errors coming from compiled modules."""
        try:
            yield
        except Exception as exc:
            raise rewrite_traceback(exc) from None

    @internal
    def import_module(self, resource_location: str) -> CompiledModule:
        """Import module."""
        try:
            module = self.get_module(resource_location)
        except KeyError:
            msg = f'Couldn\'t import "{resource_location}".'
            raise ImportError(msg) from None
        if not module.executing:
            self.get_output(module)
        return module

    @internal
    def from_module_import(self, resource_location: str, *args: str) -> Any:
        """Import a specific name from a module."""
        module = self.import_module(resource_location)
        try:
            values = [module.namespace[name] for name in args]
        except KeyError as exc:
            msg = f'Couldn\'t import {exc} from "{resource_location}".'
            raise ImportError(msg) from None
        return values[0] if len(values) == 1 else values

    def finalize(self, ctx: Context):
        """Plugin that removes modules at the end of the build."""
        yield
        ctx.data[Module].clear()


@dataclass
class ModuleCacheBackend(AstCacheBackend):
    """Cache backend that also restores the generated modules."""

    runtime: Runtime = required_field()
    bolt_version: str = import_from_string("bolt.__version__")

    def load_data(self, f: BufferedReader) -> JsonDict:
        data = super().load_data(f)
        if data["bolt"] != self.bolt_version:
            raise ValueError("Version mismatch.")
        return data

    def dump_data(self, data: JsonDict, f: BufferedWriter):
        data["bolt"] = self.bolt_version
        super().dump_data(data, f)

    def load(self, f: BufferedReader) -> AstRoot:
        data = self.load_data(f)
        ast = data["ast"]

        if data["globals"] != set(self.runtime.globals):
            raise ValueError("Globals mismatch.")

        self.runtime.modules[self.runtime.database.current] = CompiledModule(
            ast=ast,
            code=marshal.load(f),
            refs=data["refs"],
            output=data["output"],
            resource_location=data["resource_location"],
            globals=data["globals"],
        )

        return ast

    def dump(self, node: AstRoot, f: BufferedWriter):
        module = self.runtime.get_module(node)

        self.dump_data(
            {
                "ast": module.ast,
                "refs": module.refs,
                "output": module.output,
                "resource_location": module.resource_location,
                "globals": module.globals,
            },
            f,
        )

        marshal.dump(module.code, f)


@dataclass
class GlobalsInjection:
    """Inject global identifiers."""

    runtime: Runtime
    parser: Parser

    def __call__(self, stream: TokenStream) -> Any:
        with stream.provide(
            identifiers=set(self.runtime.globals)
            | self.runtime.builtins
            | {"__name__"},
        ):
            return self.parser(stream)


@dataclass
class ModuleRootParser:
    """Parser for module root."""

    database: CompilationDatabase
    parser: Parser

    def __call__(self, stream: TokenStream) -> Any:
        node = self.parser(stream)
        if isinstance(node, AstRoot) and isinstance(self.database.current, Module):
            node = set_location(AstModuleRoot(commands=node.commands), node)
        return node


@dataclass
class Evaluator(Visitor):
    """Visitor that evaluates modules."""

    runtime: Runtime = required_field()

    @rule(AstRoot)
    def root(self, node: AstRoot) -> AstRoot:
        module = self.runtime.get_module(node)
        try:
            return self.runtime.get_output(module)
        except BubbleException:
            raise
        except UnusableCompilationUnit as exc:
            if not exc.compilation_unit.diagnostics.error:
                raise
            raise DiagnosticCollection()
        except Exception as exc:
            msg = "Top-level statement raised an exception."
            if module.resource_location:
                msg += f" ({module.resource_location})"
            tb = exc.__traceback__.tb_next.tb_next  # type: ignore
            raise CompilationError(msg) from exc.with_traceback(tb)


class ModuleRootSerializer(Visitor):
    """Serializer for checking that modules don't emit any commands."""

    @rule(AstModuleRoot)
    def module_root(self, node: AstModuleRoot, result: List[str]):
        if node.commands:
            command = node.commands[0]
            name = command.identifier.partition(":")[0]
            raise set_location(
                Diagnostic("warn", f'Standalone "{name}" command in module.'),
                command,
                command.arguments[0] if command.arguments else command,
            )
