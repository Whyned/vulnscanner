import socket

from .WorkerInterface import WorkerInterface

class PortScannerWorker(WorkerInterface):
    def __init__(self, options):
        self.timeout = options['timeout']

    def processHostPort(self, host, port):
        try:
            socket.create_connection((host, port), self.timeout)
        except Exception:
            return
        print("Open: %s:%s" %(host, port))
