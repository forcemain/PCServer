#! -*- coding: utf-8 -*-


import uuid
import socket


def uuid4():
    return uuid.uuid4().__str__()


def creat_socket(_type, **kwargs):
    socket_types = ('tcp', 'udp')
    assert _type in socket_types, (
        'wrong socket type, only support {0}'.format(socket_types)
    )
    if _type == 'tcp':
        return socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM, **kwargs)

