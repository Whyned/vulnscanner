import socket

from .Worker import Worker, SKIP_HOST

class PortScannerWorker(Worker):
    def __init__(self, options):
        self.timeout = options['timeout']

    def processHostPort(self, host, port):
        try:
            socket.create_connection((host, port), self.timeout)
        except ConnectionRefusedError:
            return None
        except Exception as e:
            return SKIP_HOST
        print("Open: %s:%s" %(host, port))
