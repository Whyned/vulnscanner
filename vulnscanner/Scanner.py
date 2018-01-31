import threading as threading2
import time

from waiters.RandomIPv4 import RandomIPv4Waiter
from workers.PortScanner import PortScannerWorker
from workers.Worker import SKIP_HOST as SKIP_HOST

from utils import threading

class Scanner:
    def __init__(self, waiters, workers, limit):
        self.waiters = [w.generator() for w in waiters]
        if len(workers) == 0:
            raise Exception('Without workers, who should do the work?')
        self.workers = workers
        self.limit = limit

    def run(self):
        threading.concurrent_worker(self.worker_generator(), self.limit)

    def worker_generator(self):
        while len(self.waiters) > 0:
            for host, port in self.waiters.pop(0):
                yield (self.worker, (host, port), threading.NO_KWARGS)

    def worker(self, host, ports):
        for w in self.workers:
            for port in ports:
                return_value = w.processHostPort(host, port)
                if return_value == SKIP_HOST:
                    return

if __name__ == '__main__':
    waiters = [
        RandomIPv4Waiter({'ports': (80,8080)})
    ]
    workers = [
        PortScannerWorker({'timeout': 3})
    ]
    s = Scanner(waiters, workers, 200)
    s.run()
