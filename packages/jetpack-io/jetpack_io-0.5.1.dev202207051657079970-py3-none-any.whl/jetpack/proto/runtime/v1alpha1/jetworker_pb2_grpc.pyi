"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import jetpack.proto.runtime.v1alpha1.jetworker_pb2

class JetworkerStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    StartJetroutine: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.jetworker_pb2.StartJetroutineRequest,
        jetpack.proto.runtime.v1alpha1.jetworker_pb2.StartJetroutineResponse]


class JetworkerServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def StartJetroutine(self,
        request: jetpack.proto.runtime.v1alpha1.jetworker_pb2.StartJetroutineRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.jetworker_pb2.StartJetroutineResponse: ...


def add_JetworkerServicer_to_server(servicer: JetworkerServicer, server: grpc.Server) -> None: ...
