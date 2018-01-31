import threading as threading2
import time

from host_port_waiters.RandomIPv4 import RandomIPv4Waiter
from workers.PortScanner import PortScannerWorker

from utils import threading

class Scanner:
    def __init__(self, waiters, workers, limit):
        self.waiters = [w.generator() for w in waiters]
        if len(workers) == 0:
            raise Exception('Without workers, we can\'t do a thing')
        self.workers = workers
        self.limit = limit

    def run(self):
        threading.concurrent_worker(self.worker_producer(), self.limit)

    def worker_producer(self):
        while len(self.waiters) > 0:
            for host, port in self.waiters[0]:
                yield (self.worker_wrapper, (host, port), threading.NO_KWARGS)

            self.waiters.pop(0)

    def worker_wrapper(self, host, port):
        #print(host, port)
        for w in self.workers:
            w.processHostPort(host, port)

if __name__ == '__main__':
    waiters = [
        RandomIPv4Waiter({'ports': (80,8080)})
    ]
    workers = [
        PortScannerWorker({'timeout': 3})
    ]
    s = Scanner(waiters, workers, 200)
    s.run()
