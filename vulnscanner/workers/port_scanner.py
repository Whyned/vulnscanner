import socket
import errno

from vulnscanner import logger
from vulnscanner.workers import Worker, SKIP_HOST

RESULT_FILE = 'open_ports.result'

class PortScannerWorker(Worker):
    def __init__(self, options):
        self.timeout = options['timeout']

    def processHostPort(self, host, port):
        logger.debug('PortScannerWorker Checking: %s:%s' %(host, port))
        try:
            socket.create_connection((host, port), self.timeout)
        except Exception as e:
            if e.errno == errno.ECONNREFUSED:
                logger.debug('PortScannerWorker Connection refused on %s:%s' %(host, port))
                return None
            logger.debug('PortScannerWorker Catched Exception: %s' %e)
            return SKIP_HOST
        logger.result('PortScanner', 'open', RESULT_FILE, '%s:%s' %(host, port))
