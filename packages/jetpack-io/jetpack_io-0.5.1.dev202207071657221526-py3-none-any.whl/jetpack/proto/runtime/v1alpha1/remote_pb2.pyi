from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

APPLICATION: ErrorCode
DAYS: Unit
DESCRIPTOR: _descriptor.FileDescriptor
FRIDAY: DayOfWeek
HOURS: Unit
MINUTES: Unit
MONDAY: DayOfWeek
SATURDAY: DayOfWeek
SECONDS: Unit
SUNDAY: DayOfWeek
SYSTEM: ErrorCode
THURSDAY: DayOfWeek
TUESDAY: DayOfWeek
UNKNOWN: ErrorCode
UNKNOWN_DAY: DayOfWeek
UNKNOWN_UNIT: Unit
WEDNESDAY: DayOfWeek
WEEKS: Unit

class CancelTaskRequest(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class CancelTaskResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class CreateTaskRequest(_message.Message):
    __slots__ = ["sdk_version", "task"]
    SDK_VERSION_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    sdk_version: str
    task: Task
    def __init__(self, task: _Optional[_Union[Task, _Mapping]] = ..., sdk_version: _Optional[str] = ...) -> None: ...

class CreateTaskResponse(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class CronJob(_message.Message):
    __slots__ = ["interval", "qualified_symbol", "schedule_rule", "target_day_of_week", "target_time", "unit"]
    INTERVAL_FIELD_NUMBER: _ClassVar[int]
    QUALIFIED_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_RULE_FIELD_NUMBER: _ClassVar[int]
    TARGET_DAY_OF_WEEK_FIELD_NUMBER: _ClassVar[int]
    TARGET_TIME_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    interval: int
    qualified_symbol: str
    schedule_rule: str
    target_day_of_week: DayOfWeek
    target_time: str
    unit: Unit
    def __init__(self, qualified_symbol: _Optional[str] = ..., target_time: _Optional[str] = ..., target_day_of_week: _Optional[_Union[DayOfWeek, str]] = ..., unit: _Optional[_Union[Unit, str]] = ..., interval: _Optional[int] = ..., schedule_rule: _Optional[str] = ...) -> None: ...

class DeregisterAppRequest(_message.Message):
    __slots__ = ["hostname", "namespace"]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    hostname: str
    namespace: str
    def __init__(self, namespace: _Optional[str] = ..., hostname: _Optional[str] = ...) -> None: ...

class DeregisterAppResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Error(_message.Message):
    __slots__ = ["code", "encoded_error", "message"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    ENCODED_ERROR_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: ErrorCode
    encoded_error: bytes
    message: str
    def __init__(self, code: _Optional[_Union[ErrorCode, str]] = ..., message: _Optional[str] = ..., encoded_error: _Optional[bytes] = ...) -> None: ...

class GetSymbolFromEndpointRequest(_message.Message):
    __slots__ = ["endpoint"]
    ENDPOINT_FIELD_NUMBER: _ClassVar[int]
    endpoint: str
    def __init__(self, endpoint: _Optional[str] = ...) -> None: ...

class GetSymbolFromEndpointResponse(_message.Message):
    __slots__ = ["symbol"]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    def __init__(self, symbol: _Optional[str] = ...) -> None: ...

class GetTaskRequest(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class GetTaskResponse(_message.Message):
    __slots__ = ["encoded_args", "id"]
    ENCODED_ARGS_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    encoded_args: bytes
    id: str
    def __init__(self, id: _Optional[str] = ..., encoded_args: _Optional[bytes] = ...) -> None: ...

class PostResultRequest(_message.Message):
    __slots__ = ["exec_id", "result"]
    EXEC_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    exec_id: str
    result: Result
    def __init__(self, exec_id: _Optional[str] = ..., result: _Optional[_Union[Result, _Mapping]] = ...) -> None: ...

class PostResultResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RegisterAppRequest(_message.Message):
    __slots__ = ["cron_jobs", "endpoints", "hostname", "namespace", "qualified_symbols"]
    class EndpointsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CRON_JOBS_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    QUALIFIED_SYMBOLS_FIELD_NUMBER: _ClassVar[int]
    cron_jobs: _containers.RepeatedCompositeFieldContainer[CronJob]
    endpoints: _containers.ScalarMap[str, str]
    hostname: str
    namespace: str
    qualified_symbols: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, namespace: _Optional[str] = ..., hostname: _Optional[str] = ..., cron_jobs: _Optional[_Iterable[_Union[CronJob, _Mapping]]] = ..., qualified_symbols: _Optional[_Iterable[str]] = ..., endpoints: _Optional[_Mapping[str, str]] = ...) -> None: ...

class RegisterAppResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RemoteCallRequest(_message.Message):
    __slots__ = ["json_args", "qualified_symbol"]
    JSON_ARGS_FIELD_NUMBER: _ClassVar[int]
    QUALIFIED_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    json_args: str
    qualified_symbol: str
    def __init__(self, qualified_symbol: _Optional[str] = ..., json_args: _Optional[str] = ...) -> None: ...

class RemoteCallResponse(_message.Message):
    __slots__ = ["json_results"]
    JSON_RESULTS_FIELD_NUMBER: _ClassVar[int]
    json_results: str
    def __init__(self, json_results: _Optional[str] = ...) -> None: ...

class Result(_message.Message):
    __slots__ = ["error", "value"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    error: Error
    value: Value
    def __init__(self, value: _Optional[_Union[Value, _Mapping]] = ..., error: _Optional[_Union[Error, _Mapping]] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ["app_name", "chart_revision", "encoded_args", "hostname", "namespace", "parent_task_id", "qualified_symbol", "target_time", "task_id", "with_checkpointing"]
    APP_NAME_FIELD_NUMBER: _ClassVar[int]
    CHART_REVISION_FIELD_NUMBER: _ClassVar[int]
    ENCODED_ARGS_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    PARENT_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    QUALIFIED_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TARGET_TIME_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    WITH_CHECKPOINTING_FIELD_NUMBER: _ClassVar[int]
    app_name: str
    chart_revision: str
    encoded_args: bytes
    hostname: str
    namespace: str
    parent_task_id: str
    qualified_symbol: str
    target_time: _timestamp_pb2.Timestamp
    task_id: str
    with_checkpointing: bool
    def __init__(self, namespace: _Optional[str] = ..., hostname: _Optional[str] = ..., app_name: _Optional[str] = ..., chart_revision: _Optional[str] = ..., qualified_symbol: _Optional[str] = ..., encoded_args: _Optional[bytes] = ..., parent_task_id: _Optional[str] = ..., target_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., with_checkpointing: bool = ..., task_id: _Optional[str] = ...) -> None: ...

class Value(_message.Message):
    __slots__ = ["encoded_value"]
    ENCODED_VALUE_FIELD_NUMBER: _ClassVar[int]
    encoded_value: bytes
    def __init__(self, encoded_value: _Optional[bytes] = ...) -> None: ...

class WaitForResultRequest(_message.Message):
    __slots__ = ["task_id"]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    task_id: str
    def __init__(self, task_id: _Optional[str] = ...) -> None: ...

class WaitForResultResponse(_message.Message):
    __slots__ = ["result"]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, _Mapping]] = ...) -> None: ...

class ErrorCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Unit(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DayOfWeek(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
