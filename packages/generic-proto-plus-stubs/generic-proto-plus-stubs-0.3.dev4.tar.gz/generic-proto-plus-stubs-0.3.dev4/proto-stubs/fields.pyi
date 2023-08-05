from __future__ import annotations
import typing as t

from google.protobuf import descriptor_pb2
from proto.message import Message as ProtoMessage

T = t.TypeVar('T')

class Field(t.Generic[T]):
    repeated: bool
    mcls_data: t.Any
    parent: t.Any
    number: t.Any
    proto_type: int
    message: t.Type[T] | None
    enum: t.Type[T] | None
    json_name: t.Any
    optional: bool
    oneof: str

    @t.overload
    def __init__(
            self: Field[t.Any],
            proto_type: int,
            number: int,
            *,
            message: None = ...,
            enum: None = ...,
            oneof: str = ...,
            json_name: str = ...,
            optional: bool = ...
    ) -> None: ...

    @t.overload
    def __init__(
            self: Field[T],
            proto_type: int,
            number: int,
            *,
            message: t.Type[T] = ...,
            enum: None = ...,
            oneof: str = ...,
            json_name: str = ...,
            optional: bool = ...
    ) -> None: ...

    @t.overload
    def __init__(
            self: Field[T],
            proto_type: int,
            number: int,
            *,
            message: None = ...,
            enum: t.Type[T] = ...,
            oneof: str = ...,
            json_name: str = ...,
            optional: bool = ...
    ) -> None: ...

    @property
    def descriptor(self) -> descriptor_pb2.FieldDescriptorProto: ...

    @property
    def name(self) -> str: ...

    @property
    def package(self) -> str: ...

    @property
    def pb_type(self): ...

    @t.overload
    def __get__(self: Field[T], instance: object, owner: t.Type[t.Any] | None = None) -> T:
        ...


class RepeatedField(Field[T]):
    repeated: bool

    @t.overload
    def __get__(self: RepeatedField[T], instance: object, owner: t.Type[t.Any] | None = None) -> t.Iterable[T]:
        ...

class MapField(Field[T]):
    map_key_type: t.Any

    def __init__(
            self,
            key_type,
            value_type,
            number: int,
            *,
            message: t.Any | None = ...,
            enum: t.Any | None = ...
    ) -> None: ...
