from functools import singledispatch
from typing import Any, List, Mapping, Optional, Tuple, TypeVar, Union
from uuid import UUID

from myst.adapters.utils import _Unset

UUIDOrStr = Union[str, UUID]
IntOrStr = Union[int, str]
Shape = Tuple[int, ...]
CoordinateLabels = Tuple[Tuple[IntOrStr, ...], ...]
AxisLabels = Tuple[IntOrStr, ...]
Metadata = Mapping[str, Union[str, int, float, bool, None]]

T = TypeVar("T")
OptionalParam = Union[Optional[T], _Unset]

# Note: This should be a recursive type alias but `mypy` doesn't support that, so use `List[Any]` instead to allow for
#   an arbitrary amount of nesting.
ItemOrSlice = Union[Tuple[Union[IntOrStr, List[Any]], ...], List[Any], IntOrStr]


@singledispatch
def to_uuid(uuid: UUIDOrStr) -> UUID:
    raise NotImplementedError()


@to_uuid.register
def _uuid_to_uuid(uuid: UUID) -> UUID:
    return uuid


@to_uuid.register
def _str_to_uuid(uuid: str) -> UUID:
    return UUID(uuid)
