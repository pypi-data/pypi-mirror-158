"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import jetpack.proto.runtime.v1alpha1.remote_pb2

class RemoteExecutorStub:
    def __init__(self, channel: grpc.Channel) -> None: ...
    CreateTask: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.CreateTaskRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.CreateTaskResponse]

    CancelTask: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.CancelTaskRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.CancelTaskResponse]

    PostResult: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.PostResultRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.PostResultResponse]

    WaitForResult: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.WaitForResultRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.WaitForResultResponse]

    GetTask: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.GetTaskRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.GetTaskResponse]

    GetSymbolFromEndpoint: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.GetSymbolFromEndpointRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.GetSymbolFromEndpointResponse]
    """GetSymbolFromEndpoint is not used by SDK. It's a way for runtime web server to find
    symbols of endpoints to handle endpoint http requests.
    """

    RegisterApp: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.RegisterAppRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.RegisterAppResponse]

    DeregisterApp: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.DeregisterAppRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.DeregisterAppResponse]

    RemoteCall: grpc.UnaryUnaryMultiCallable[
        jetpack.proto.runtime.v1alpha1.remote_pb2.RemoteCallRequest,
        jetpack.proto.runtime.v1alpha1.remote_pb2.RemoteCallResponse]
    """Golang prototype"""


class RemoteExecutorServicer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def CreateTask(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.CreateTaskRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.CreateTaskResponse: ...

    @abc.abstractmethod
    def CancelTask(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.CancelTaskRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.CancelTaskResponse: ...

    @abc.abstractmethod
    def PostResult(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.PostResultRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.PostResultResponse: ...

    @abc.abstractmethod
    def WaitForResult(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.WaitForResultRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.WaitForResultResponse: ...

    @abc.abstractmethod
    def GetTask(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.GetTaskRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.GetTaskResponse: ...

    @abc.abstractmethod
    def GetSymbolFromEndpoint(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.GetSymbolFromEndpointRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.GetSymbolFromEndpointResponse:
        """GetSymbolFromEndpoint is not used by SDK. It's a way for runtime web server to find
        symbols of endpoints to handle endpoint http requests.
        """
        pass

    @abc.abstractmethod
    def RegisterApp(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.RegisterAppRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.RegisterAppResponse: ...

    @abc.abstractmethod
    def DeregisterApp(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.DeregisterAppRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.DeregisterAppResponse: ...

    @abc.abstractmethod
    def RemoteCall(self,
        request: jetpack.proto.runtime.v1alpha1.remote_pb2.RemoteCallRequest,
        context: grpc.ServicerContext,
    ) -> jetpack.proto.runtime.v1alpha1.remote_pb2.RemoteCallResponse:
        """Golang prototype"""
        pass


def add_RemoteExecutorServicer_to_server(servicer: RemoteExecutorServicer, server: grpc.Server) -> None: ...
