"""Helper for using type annotations to recursively generate instantiator functions,
which map strings (or, in some cases, sequences of strings) to the annotated type.

Some examples of type annotations and the desired instantiators:
```
    int

        lambda string: int(str)

    List[int]

        lambda strings: list(
            [int(x) for x in strings]
        )

    List[Color], where Color is an enum

        lambda strings: list(
            [Color[x] for x in strings]
        )

    Tuple[int, float]

        lambda strings: tuple(
            [
                typ(x)
                for typ, x in zip(
                    (int, float),
                    strings,
                )
            ]
        )
```
"""

import collections.abc
import dataclasses
import enum
import inspect
import warnings
from typing import (
    Any,
    Callable,
    Dict,
    Hashable,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

from typing_extensions import Annotated, Final, Literal, get_args, get_origin

from . import _strings

# Most standard fields: these are converted from strings from the CLI.
_StandardInstantiator = Callable[[str], Any]
# Sequence fields! This should be used whenever argparse's `nargs` field is set.
_SequenceInstantiator = Callable[[List[str]], Any]
# Special case: the only time that argparse doesn't give us a string is when the
# argument action is set to `store_true` or `store_false`. In this case, we get
# a bool directly, and the field action can be a no-op.
_FlagInstantiator = Callable[[bool], bool]

Instantiator = Union[_StandardInstantiator, _SequenceInstantiator, _FlagInstantiator]


@dataclasses.dataclass
class InstantiatorMetadata:
    nargs: Optional[Union[str, int]]
    metavar: Union[str, Tuple[str, ...]]
    choices: Optional[Tuple[str, ...]]
    is_optional: bool


class UnsupportedTypeAnnotationError(Exception):
    """Exception raised when an unsupported type annotation is detected."""


_builtin_set = set(
    filter(
        lambda x: isinstance(x, Hashable),  # type: ignore
        __builtins__.values(),  # type: ignore
    )
)


def instantiator_from_type(
    typ: Type, type_from_typevar: Dict[TypeVar, Type]
) -> Tuple[Instantiator, InstantiatorMetadata]:
    """Recursive helper for parsing type annotations.

    Returns two things:
    - An instantiator function, for instantiating the type from a string or list of
      strings. The latter applies when argparse's `nargs` parameter is set.
    - A metadata structure, which specifies parameters for argparse.
    """

    # Resolve typevars.
    if typ in type_from_typevar:
        return instantiator_from_type(
            type_from_typevar[typ],  # type: ignore
            type_from_typevar,
        )

    if typ is Any:
        warnings.warn("Found field with type `Any`, which will be parsed as a string.")
        return lambda arg: arg, InstantiatorMetadata(
            nargs=None,
            metavar="ANY",
            choices=None,
            is_optional=False,
        )

    # Address container types. If a matching container is found, this will recursively
    # call instantiator_from_type().
    container_out = _instantiator_from_container_type(typ, type_from_typevar)
    if container_out is not None:
        return container_out

    # Validate that typ is a `(arg: str) -> T` type converter, as expected by argparse.
    if typ in _builtin_set:
        pass
    elif not callable(typ):
        raise UnsupportedTypeAnnotationError(
            f"Expected {typ} to be a `(arg: str) -> T` type converter, but is not"
            " callable."
        )
    else:
        param_count = 0
        has_var_positional = False
        signature = inspect.signature(typ)
        for i, param in enumerate(signature.parameters.values()):
            if i == 0 and param.annotation not in (str, inspect.Parameter.empty):
                raise UnsupportedTypeAnnotationError(
                    f"Expected {typ} to be a `(arg: str) -> T` type converter, but got"
                    f" {signature}. You may have a nested type in a container, which is"
                    " unsupported."
                )
            if param.kind is inspect.Parameter.VAR_POSITIONAL:
                has_var_positional = True
            elif param.default is inspect.Parameter.empty and param.kind is not (
                inspect.Parameter.VAR_KEYWORD
            ):
                param_count += 1

        # Raise an error if parameters look wrong.
        if not (param_count == 1 or (param_count == 0 and has_var_positional)):
            raise UnsupportedTypeAnnotationError(
                f"Expected {typ} to be a `(arg: str) -> T` type converter, but got"
                f" {signature}. You may have a nested type in a container, which is"
                " unsupported."
            )

    # Special case `choices` for some types, as implemented in `instance_from_string()`.
    auto_choices: Optional[Tuple[str, ...]] = None
    if typ is bool:
        auto_choices = ("True", "False")
    elif isinstance(typ, type) and issubclass(typ, enum.Enum):
        auto_choices = tuple(x.name for x in typ)

    return lambda arg: _strings.instance_from_string(typ, arg), InstantiatorMetadata(
        nargs=None,
        metavar=typ.__name__.upper()
        if auto_choices is None
        else "{" + ",".join(map(str, auto_choices)) + "}",
        choices=auto_choices,
        is_optional=False,
    )


def _instantiator_from_container_type(
    typ: Type, type_from_typevar: Dict[TypeVar, Type]
) -> Optional[Tuple[Instantiator, InstantiatorMetadata]]:
    """Attempt to create an instantiator from a container type. Returns `None` is no
    container type is found."""

    type_origin = get_origin(typ)
    if type_origin is None:
        return None

    # Unwrap Annotated and Final types.
    if type_origin in (Annotated, Final):
        contained_type = get_args(typ)[0]
        return instantiator_from_type(contained_type, type_from_typevar)

    # List, tuples, and sequences.
    if type_origin in (
        collections.abc.Sequence,  # different from typing.Sequence!
        list,  # different from typing.List!
        set,  # different from typing.Set!
    ):
        (contained_type,) = get_args(typ)
        container_type = type_origin
        if container_type is collections.abc.Sequence:
            container_type = list

        make, inner_meta = _instantiator_from_type_inner(
            contained_type,
            type_from_typevar,
            allow_sequences=False,
        )
        return lambda strings: container_type(
            [make(x) for x in strings]
        ), InstantiatorMetadata(
            nargs="+",
            metavar=inner_meta.metavar,
            choices=inner_meta.choices,
            is_optional=False,
        )

    # Tuples.
    if type_origin is tuple:
        types = get_args(typ)
        typeset = set(types)  # Note that sets are unordered.
        typeset_no_ellipsis = typeset - {Ellipsis}  # type: ignore

        if typeset_no_ellipsis != typeset:
            # Ellipsis: variable argument counts. When an ellipsis is used, tuples must
            # contain only one type.
            assert len(typeset_no_ellipsis) == 1
            (contained_type,) = typeset_no_ellipsis

            make, inner_meta = _instantiator_from_type_inner(
                contained_type,
                type_from_typevar,
                allow_sequences=False,
            )
            return lambda strings: tuple(
                [make(x) for x in strings]
            ), InstantiatorMetadata(
                nargs="+",
                metavar=inner_meta.metavar,
                choices=inner_meta.choices,
                is_optional=False,
            )

        else:
            instantiators = []
            metas = []
            for t in types:
                a, b = _instantiator_from_type_inner(
                    t,
                    type_from_typevar,
                    allow_sequences=False,
                )
                instantiators.append(a)
                metas.append(b)

            if len(set(m.choices for m in metas)) > 1:
                raise UnsupportedTypeAnnotationError(
                    "Due to constraints in argparse, all choices in fixed-length tuples"
                    " must match. This restricts mixing enums & literals with other"
                    " types."
                )
            return lambda strings: tuple(
                make(x) for make, x in zip(instantiators, strings)
            ), InstantiatorMetadata(
                nargs=len(types),
                metavar=tuple(cast(str, m.metavar) for m in metas),
                choices=metas[0].choices,
                is_optional=False,
            )

    # Optionals.
    if type_origin is Union:
        options = set(get_args(typ))
        if len(options) != 2 or type(None) not in options:
            # Note that the subparsers logic happens much earlier.
            raise UnsupportedTypeAnnotationError(
                "Union must be either over dataclasses (for subparsers) or Optional"
                " (Union[T, None])"
            )
        (typ,) = options - {type(None)}
        inner_instantiator, metadata = _instantiator_from_type_inner(
            typ,
            type_from_typevar,
            allow_sequences=True,
        )
        instantiator = (
            lambda string: None if string == "None" else inner_instantiator(string)
        )
        return instantiator, dataclasses.replace(
            metadata,
            metavar=f"({metadata.metavar} | None)",
            is_optional=True,
        )

    # Literals.
    if type_origin is Literal:
        choices = get_args(typ)
        if not len(set(map(type, choices))) == 1:
            raise UnsupportedTypeAnnotationError(
                "All choices in literal must have the same type!"
            )
        contained_type = type(next(iter(choices)))
        if issubclass(contained_type, enum.Enum):
            choices = tuple(map(lambda x: x.name, choices))
        instantiator, metadata = _instantiator_from_type_inner(
            contained_type,
            type_from_typevar,
            allow_sequences=False,
        )
        assert (
            # Choices provided by the contained type
            metadata.choices is None
            or len(set(choices) - set(metadata.choices)) == 0
        )
        return instantiator, dataclasses.replace(
            metadata,
            choices=tuple(map(str, choices)),
            metavar="{" + ",".join(map(str, choices)) + "}",
            is_optional=False,
        )

    # Dictionaries.
    if type_origin in (dict, collections.abc.Mapping):
        key_type, val_type = get_args(typ)
        key_instantiator, key_metadata = _instantiator_from_type_inner(
            key_type,
            type_from_typevar,
            allow_sequences=False,
        )
        val_instantiator, val_metadata = _instantiator_from_type_inner(
            val_type,
            type_from_typevar,
            allow_sequences=False,
        )

        def dict_instantiator(strings: List[str]) -> Any:
            out = {}
            if len(strings) % 2 != 0:
                raise ValueError("incomplete set of key value pairs!")
            for i in range(len(strings) // 2):
                k = strings[i * 2]
                v = strings[i * 2 + 1]
                if key_metadata.choices is not None and k not in key_metadata.choices:
                    raise ValueError(
                        f"invalid choice: {k} (choose from {key_metadata.choices}))"
                    )
                if val_metadata.choices is not None and v not in val_metadata.choices:
                    raise ValueError(
                        f"invalid choice: {v} (choose from {val_metadata.choices}))"
                    )
                out[key_instantiator(k)] = val_instantiator(v)  # type: ignore
            return out

        return dict_instantiator, InstantiatorMetadata(
            nargs="+",
            metavar=f"{key_metadata.metavar} {val_metadata.metavar}",
            choices=None,
            is_optional=False,
        )

    raise UnsupportedTypeAnnotationError(  # pragma: no cover
        f"Unsupported type {typ} with origin {type_origin}"
    )


@overload
def _instantiator_from_type_inner(
    typ: Type,
    type_from_typevar: Dict[TypeVar, Type],
    allow_sequences: Literal[False],
) -> Tuple[_StandardInstantiator, InstantiatorMetadata]:
    ...


@overload
def _instantiator_from_type_inner(
    typ: Type,
    type_from_typevar: Dict[TypeVar, Type],
    allow_sequences: Literal[True],
) -> Tuple[Instantiator, InstantiatorMetadata]:
    ...


def _instantiator_from_type_inner(
    typ: Type,
    type_from_typevar: Dict[TypeVar, Type],
    allow_sequences: bool,
) -> Tuple[Instantiator, InstantiatorMetadata]:
    """Thin wrapper over instantiator_from_type, with some extra asserts for catching
    errors."""
    out = instantiator_from_type(typ, type_from_typevar)
    if not allow_sequences and out[1].nargs is not None:
        raise UnsupportedTypeAnnotationError("Nested sequence types are not supported!")
    return out
