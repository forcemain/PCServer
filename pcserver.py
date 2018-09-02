#! -*- coding: utf-8 -*-


import sys


from server.database import get_serverdir
from server.core.tcpserver import TcpServer
from server.common.scheduler import Scheduler


reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.insert(0, get_serverdir())


if __name__ == '__main__':
    tcpserver = TcpServer(host='0.0.0.0', port=1314)
    scheduler = Scheduler()
    scheduler.spawn_all(*[
        tcpserver.run_forever()
    ])
    scheduler.main_loop()
