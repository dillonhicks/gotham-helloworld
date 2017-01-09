"""Python Stub implementation of echoexample"""
import sys
from concurrent import futures
import pkg_resources
import time
from subprocess import Popen, PIPE
import logging

import grpc
from thundersnow.dateutil import Delta
from google.protobuf.json_format import MessageToDict

from echoexample import echo_pb2, echo_pb2_grpc
from echoexample.echo_pb2 import (
    HelloRequest,
    HelloResponse,
)


LOG = logging.getLogger(__name__)


class Echo(echo_pb2_grpc.EchoServicer):

    def Hello(self, request, context):
        # type: (HelloRequest, grpc.RpcContext) -> HelloResponse
        LOG.info('Request[%s]: %s', context.peer(), MessageToDict(request))
        LOG.info('Request[%s]: %s', context.peer(), context.invocation_metadata())
        response =  HelloResponse()
        response.message = '{}, {}!'.format(request.greeting, request.name)
        return response


def serve(port, with_proxy_server=False):

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    echo_pb2_grpc.add_EchoServicer_to_server(Echo(), server)

    server.add_insecure_port('[::]:{}'.format(port))
    server.start()

    proxy_process = None
    proxy_filepath = pkg_resources.resource_filename('echoexample', 'bin/rest-proxy-server.bin')
    if sys.platform.lower() == 'darwin':
        proxy_filepath = '.'.join([proxy_filepath, 'darwin'])

    try:
        if with_proxy_server:
            proxy_process = Popen([proxy_filepath])
        while True:
            time.sleep(Delta.one_day.total_seconds())
    except KeyboardInterrupt:
        if proxy_process is not None:
            proxy_process.terminate()

        server.stop(0)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Run echoexample, optionally with the REST Proxy Server',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-p', '--port', type=str, action='store',
                        default=8080,
                        help='server port')

    parser.add_argument('--with-proxy-server', action='store_true',
                        default=False, help='Start the rest proxy server')

    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    serve(args.port, args.with_proxy_server)


if __name__ == '__main__':
    main()
