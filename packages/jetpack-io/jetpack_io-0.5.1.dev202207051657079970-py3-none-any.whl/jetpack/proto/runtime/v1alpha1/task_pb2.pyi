from jetpack.proto.runtime.v1alpha1 import remote_pb2 as _remote_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CheckpointTracker(_message.Message):
    __slots__ = ["checkpoints", "id"]
    class CheckpointsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    checkpoints: _containers.ScalarMap[str, str]
    id: str
    def __init__(self, id: _Optional[str] = ..., checkpoints: _Optional[_Mapping[str, str]] = ...) -> None: ...

class PersistedTask(_message.Message):
    __slots__ = ["app_name", "current_iteration", "encoded_args", "execution_mode", "id", "manifest", "parent_task_id", "qualified_symbol", "result", "status", "with_checkpointing"]
    class ExecutionMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    CANCELLED: PersistedTask.Status
    CANCELLING: PersistedTask.Status
    CREATED: PersistedTask.Status
    CURRENT_ITERATION_FIELD_NUMBER: _ClassVar[int]
    ENCODED_ARGS_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_JOB: PersistedTask.ExecutionMode
    EXECUTION_MODE_FIELD_NUMBER: _ClassVar[int]
    EXECUTION_WORKER_PUSH: PersistedTask.ExecutionMode
    FAILED: PersistedTask.Status
    FAILING: PersistedTask.Status
    ID_FIELD_NUMBER: _ClassVar[int]
    MANIFEST_FIELD_NUMBER: _ClassVar[int]
    PARENT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    QUALIFIED_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    READY: PersistedTask.Status
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RUNNING: PersistedTask.Status
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUCCEEDED: PersistedTask.Status
    UNKNOWN: PersistedTask.Status
    WAITING: PersistedTask.Status
    WITH_CHECKPOINTING_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    current_iteration: int
    encoded_args: bytes
    execution_mode: PersistedTask.ExecutionMode
    id: str
    manifest: bytes
    parent_task_id: str
    qualified_symbol: str
    result: _remote_pb2.Result
    status: PersistedTask.Status
    with_checkpointing: bool
    def __init__(self, id: _Optional[str] = ..., qualified_symbol: _Optional[str] = ..., encoded_args: _Optional[bytes] = ..., manifest: _Optional[bytes] = ..., status: _Optional[_Union[PersistedTask.Status, str]] = ..., result: _Optional[_Union[_remote_pb2.Result, _Mapping]] = ..., app_name: _Optional[str] = ..., parent_task_id: _Optional[str] = ..., with_checkpointing: bool = ..., current_iteration: _Optional[int] = ..., execution_mode: _Optional[_Union[PersistedTask.ExecutionMode, str]] = ...) -> None: ...
