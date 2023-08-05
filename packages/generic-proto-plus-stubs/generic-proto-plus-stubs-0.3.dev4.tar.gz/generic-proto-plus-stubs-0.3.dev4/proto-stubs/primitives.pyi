import enum
from typing import Literal, TypeVar

class ProtoType(enum.IntEnum):
    DOUBLE: int
    FLOAT: int
    INT64: int
    UINT64: int
    INT32: int
    FIXED64: int
    FIXED32: int
    BOOL: int
    STRING: int
    MESSAGE: int
    BYTES: int
    UINT32: int
    ENUM: int
    SFIXED32: int
    SFIXED64: int
    SINT32: int
    SINT64: int

# we can't use the values of the enum, since Pycharm doesn't support it,
# see https://youtrack.jetbrains.com/issue/PY-35235/Support-PEP-586-Literal-Types

T_DOUBLE = Literal[1]
T_FLOAT = Literal[2]
T_INT64 = Literal[3]
T_UINT64 = Literal[4]
T_INT32 = Literal[5]
T_FIXED64 = Literal[6]
T_FIXED32 = Literal[7]
T_BOOL = Literal[8]
T_STRING = Literal[9]
T_MESSAGE = Literal[10]
T_BYTES = Literal[11]
T_UINT32 = Literal[12]
T_ENUM = Literal[13]
T_SFIXED32 = Literal[14]
T_SFIXED64 = Literal[15]
T_SINT32 = Literal[16]
T_SINT64 = Literal[17]

T_enum = TypeVar(
    'T_enum',
    T_DOUBLE,
    T_FLOAT,
    T_INT64,
    T_UINT64,
    T_INT32,
    T_FIXED64,
    T_FIXED32,
    T_BOOL,
    T_STRING,
    T_MESSAGE,
    T_BYTES,
    T_UINT32,
    T_ENUM,
    T_SFIXED32,
    T_SFIXED64,
    T_SINT32,
    T_SINT64,
)
