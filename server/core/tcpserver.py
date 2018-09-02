#! -*- coding: utf-8 -*-


from server.common import customcall
from server.common.logger import Logger
from server.common.shortcut import creat_socket



logger = Logger.get_logger(__name__)


class TcpServer(object):
    SOCKET_TYPE = 'tcp'

    def __init__(self, host='0.0.0.0', port=1314, **kwargs):
        self.host = host
        self.port = port
        self.max_conns = kwargs.get('max_conns', 1024)
        self.socket = creat_socket(self.__class__.SOCKET_TYPE)
        self.socket.bind((host, port))
        self.socket.listen(self.max_conns)

    def _handle(self, client, address, buffersize=4096):
        try:
            while True:
                yield customcall.CanReadCall(client)
                data = client.recv(buffersize)
                logger.debug('recv {0} data: {1}'.format(address, data))
                client.sendall(data.upper())
        except Exception:
            client.close()
            logger.debug('conn {0} closed'.format(address))

    def run_forever(self):
        while True:
            yield customcall.CanReadCall(self.socket)
            client_socket, address = self.socket.accept()
            logger.info('new conn from {0}'.format(address))
            yield customcall.ForkTaskCall(self._handle(client_socket, address))