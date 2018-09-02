#! -*- coding: utf-8 -*-


import os


def get_basedir():
    return os.path.dirname(__file__)


def get_serverdir():
    return os.path.dirname(get_basedir())


def get_projectdir():
    return os.path.dirname(get_serverdir())
