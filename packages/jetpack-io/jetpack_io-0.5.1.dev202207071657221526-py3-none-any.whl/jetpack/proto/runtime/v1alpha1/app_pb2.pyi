from jetpack.proto.runtime.v1alpha1 import remote_pb2 as _remote_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserApp(_message.Message):
    __slots__ = ["latest_manifest", "revision_to_manifest"]
    class RevisionToManifestEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: str
        def __init__(self, key: _Optional[int] = ..., value: _Optional[str] = ...) -> None: ...
    LATEST_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    REVISION_TO_MANIFEST_FIELD_NUMBER: _ClassVar[int]
    latest_manifest: str
    revision_to_manifest: _containers.ScalarMap[int, str]
    def __init__(self, revision_to_manifest: _Optional[_Mapping[int, str]] = ..., latest_manifest: _Optional[str] = ...) -> None: ...
