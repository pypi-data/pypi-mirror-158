# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from jetpack.proto.runtime.v1alpha1 import jetworker_pb2 as jetpack_dot_proto_dot_runtime_dot_v1alpha1_dot_jetworker__pb2


class JetworkerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.StartJetroutine = channel.unary_unary(
                '/jetworker.Jetworker/StartJetroutine',
                request_serializer=jetpack_dot_proto_dot_runtime_dot_v1alpha1_dot_jetworker__pb2.StartJetroutineRequest.SerializeToString,
                response_deserializer=jetpack_dot_proto_dot_runtime_dot_v1alpha1_dot_jetworker__pb2.StartJetroutineResponse.FromString,
                )


class JetworkerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def StartJetroutine(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_JetworkerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'StartJetroutine': grpc.unary_unary_rpc_method_handler(
                    servicer.StartJetroutine,
                    request_deserializer=jetpack_dot_proto_dot_runtime_dot_v1alpha1_dot_jetworker__pb2.StartJetroutineRequest.FromString,
                    response_serializer=jetpack_dot_proto_dot_runtime_dot_v1alpha1_dot_jetworker__pb2.StartJetroutineResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'jetworker.Jetworker', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Jetworker(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def StartJetroutine(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/jetworker.Jetworker/StartJetroutine',
            jetpack_dot_proto_dot_runtime_dot_v1alpha1_dot_jetworker__pb2.StartJetroutineRequest.SerializeToString,
            jetpack_dot_proto_dot_runtime_dot_v1alpha1_dot_jetworker__pb2.StartJetroutineResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
