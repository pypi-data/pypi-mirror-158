from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StartJetroutineRequest(_message.Message):
    __slots__ = ["encoded_args", "exec_id", "qualified_symbol"]
    ENCODED_ARGS_FIELD_NUMBER: _ClassVar[int]
    EXEC_ID_FIELD_NUMBER: _ClassVar[int]
    QUALIFIED_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    encoded_args: str
    exec_id: str
    qualified_symbol: str
    def __init__(self, exec_id: _Optional[str] = ..., qualified_symbol: _Optional[str] = ..., encoded_args: _Optional[str] = ...) -> None: ...

class StartJetroutineResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
