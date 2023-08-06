"""Object serializers."""

from __future__ import annotations

import functools
import importlib
import os
import sys
import typing as t
import urllib.parse

from identify import identify

from project_config.compat import (
    NotRequired,
    Protocol,
    TypeAlias,
    TypedDict,
    tomllib_package_name,
)
from project_config.exceptions import ProjectConfigException


SerializerResult = t.Dict[str, t.Any]


class SerializerFunction(Protocol):
    """Typecheck protocol for function resolved by serialization factory."""

    def __call__(  # noqa: D102
        self,
        string: str,
        **kwargs: t.Any,
    ) -> SerializerResult:  # pragma: no cover
        ...


class SerializerError(ProjectConfigException):
    """Error happened serializing content as JSON."""


SerializerFunctionKwargs: TypeAlias = t.Dict[str, t.Any]


class SerializerDefinitionType(TypedDict):
    """Serializer definition type."""

    module: str

    function: NotRequired[str]
    function_kwargs_from_url_path: NotRequired[
        t.Callable[[str], SerializerFunctionKwargs]
    ]


SerializerDefinitionsType: TypeAlias = t.List[SerializerDefinitionType]

serializers: t.Dict[str, SerializerDefinitionsType] = {
    ".json": [{"module": "json"}],
    ".json5": [{"module": "pyjson5"}, {"module": "json5"}],
    ".yaml": [
        {
            # Implementation notes:
            #
            # PyYaml is currently using the Yaml 1.1 specification,
            # which converts some words like `on` and `off` to `True`
            # and `False`. This leads to problems, for example, checking
            # `on.` objects in Github workflows.
            #
            # There is an issue open to track the progress to support
            # YAML 1.2 at https://github.com/yaml/pyyaml/issues/486
            #
            # Comparison of v1.1 vs v1.2 at:
            # https://perlpunk.github.io/yaml-test-schema/schemas.html
            #
            # "module": "yaml",
            # "function": "load",
            # "function_kwargs": {
            #    "Loader": {
            #        "module": "yaml",
            #        "object": "CSafeLoader",
            #        "object_fallback": "SafeLoader",
            #    },
            # },
            #
            # So we use ruamel.yaml, which supports v1.2 by default
            "module": "project_config.serializers.yaml",
        },
    ],
    ".toml": [{"module": tomllib_package_name}],
    ".ini": [{"module": "project_config.serializers.ini"}],
    ".editorconfig": [{"module": "project_config.serializers.editorconfig"}],
    ".py": [
        {
            "module": "project_config.serializers.python",
            "function_kwargs_from_url_path": lambda path: {
                "namespace": {"__file__": path},
            },
        },
    ],
}

serializers_fallback: SerializerDefinitionsType = [
    {"module": "project_config.serializers.text"},
]


def _identify_serializer(filename: str) -> SerializerDefinitionsType:
    serializer = None
    for tag in identify.tags_from_filename(filename):
        if f".{tag}" in serializers:
            serializer = serializers[f".{tag}"]
            break
    return serializer if serializer is not None else serializers_fallback


def _get_serializer(url: str) -> SerializerFunction:
    url_parts = urllib.parse.urlsplit(url)
    ext = os.path.splitext(url_parts.path)[-1]
    try:
        serializer = serializers[ext]
    except KeyError:
        # try to guess the file type with identify
        serializer = _identify_serializer(os.path.basename(url_parts.path))

    # prepare serializer function
    serializer_definition, module = None, None
    for i, serializer_def in enumerate(serializer):
        try:
            module = importlib.import_module(serializer_def["module"])
        except ImportError:  # pragma: no cover
            # if module for implementation is not importable, try next maybe
            if i > len(serializer) - 1:
                raise
        else:
            serializer_definition = serializer_def
            break
    serializer_definition = t.cast(
        SerializerDefinitionType,
        serializer_definition,
    )

    loader_function: SerializerFunction = getattr(
        module,
        serializer_definition.get("function", "loads"),
    )

    function_kwargs: SerializerFunctionKwargs = {}

    """
    if "function_kwargs" in serializer:
        function_kwargs = {}
        for kwarg_name, kwarg_values in serializer[
            "function_kwargs"
        ].items():
            mod = importlib.import_module(kwarg_values["module"])
            try:
                obj = getattr(mod, kwarg_values["object"])
            except AttributeError:
                # fallback object, as with pyyaml use CSafeLoader instead
                # of SafeLoader if libyyaml bindings are available
                if "fallback_object" in kwarg_values:
                    obj = getattr(mod, kwarg_values["object"])
                else:
                    raise
            function_kwargs[kwarg_name] = obj
    """

    if "function_kwargs_from_url_path" in serializer_definition:
        function_kwargs.update(
            serializer_definition["function_kwargs_from_url_path"](
                os.path.basename(url_parts.path),
            ),
        )

    return functools.partial(loader_function, **function_kwargs)


def _file_can_not_be_serialized_as_object_error(
    url: str,
    error_message: str,
) -> str:
    return f"'{url}' can't be serialized as a valid object:{error_message}"


def serialize_for_url(url: str, string: str) -> SerializerResult:
    """Serializes to JSON a string according to the given URI.

    Args:
        url (str): URI of the file, used to detect the type of the file,
            either using the extension or through `identify`_.
        string (str): File content to serialize.

    Returns:
        dict: Result of the object serialization.

    .. _identify: https://github.com/pre-commit/identify
    """
    try:
        # serialize
        result = _get_serializer(url)(string)
    except Exception:
        # handle exceptions in third party packages without importing them
        exc_class, exc, _ = sys.exc_info()
        package_name = exc_class.__module__.split(".")[0]
        if package_name in (  # Examples:
            "json",  # json.serializer.JSONDecodeError
            "pyjson5",  # pyjson5.Json5IllegalCharacter
            "tomli",  # tomli.TOMLDecodeError
            # "tomlkit",  # tomlkit.exceptions.UnexpectedEofError
        ):
            raise SerializerError(
                _file_can_not_be_serialized_as_object_error(
                    url,
                    f" {exc.args[0]}",  # type: ignore
                ),
            )
        elif package_name == "ruamel":
            # Example: ruamel.yaml.scanner.ScannerError
            raise SerializerError(
                _file_can_not_be_serialized_as_object_error(
                    url,
                    f"\n{str(exc)}",
                ),
            )
        raise  # pragma: no cover
    return result
