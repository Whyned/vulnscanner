import socket

from . import Worker, SKIP_HOST
import logger

class PortScannerWorker(Worker):
    def __init__(self, options):
        self.timeout = options['timeout']

    def processHostPort(self, host, port):
        logger.debug('PortScannerWorker Checking: %s:%s' %(host, port))
        try:
            socket.create_connection((host, port), self.timeout)
        except ConnectionRefusedError:
            logger.debug('PortScannerWorker Port closed: %s:%s' %(host, port))
            return None
        except Exception as e:
            logger.debug('PortScannerWorker Catched Exception: %s' %e)
            return SKIP_HOST
        logger.debug('PortScannerWorker Open: %s:%s' %(host, port))
