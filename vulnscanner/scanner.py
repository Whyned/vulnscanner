import threading as threading2
import time

import logger
from workers import SKIP_HOST
from workers.port_scanner import PortScannerWorker
from waiters.random_ipv4 import RandomIPv4Waiter
from utils import concurrent_worker, NO_KWARGS

class Scanner:
    def __init__(self, waiters, workers, limit):
        if len(workers) == 0:
            raise Exception('Without workers, who should do the work?')
        self.workers = workers

        # We only need the initialized waiter generators
        self.waiters = [waiter.generator() for waiter in waiters]

        self.limit = limit

    def run(self):
        concurrent_worker(self.worker_generator(), self.limit)

    def worker_generator(self):
        while len(self.waiters) > 0:
            for host, port in self.waiters.pop(0):
                yield (self.worker, (host, port), NO_KWARGS)

    def worker(self, host, ports):
        for w in self.workers:
            for port in ports:
                if w.processHostPort(host, port) == SKIP_HOST: return

if __name__ == '__main__':
    logger.LOG_LEVELS_FILES['debug.txt'] = [logger.LOG_SILLY, logger.LOG_DEBUG]
    waiters = [
        RandomIPv4Waiter({'ports': (80,8080)})
    ]
    workers = [
        PortScannerWorker({'timeout': 3})
    ]

    s = Scanner(waiters, workers, 1000)
    s.run()
