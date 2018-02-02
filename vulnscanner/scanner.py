import threading as threading2
import time

from vulnscanner import logger
from vulnscanner.workers import SKIP_HOST
from vulnscanner.workers.port_scanner import PortScannerWorker
from vulnscanner.waiters.random_ipv4 import RandomIPv4Waiter
from vulnscanner.utils import concurrent_worker, NO_KWARGS

class Scanner:
    def __init__(self, waiters, workers, limit):
        if len(workers) == 0:
            raise Exception('Without workers, who should do the work?')
        self.workers = workers

        # We only need the initialized waiter generators
        self.waiters = [waiter.generator() for waiter in waiters]

        self.limit = limit
        logger.debug('Scanner workers: %s' %self.workers)
        logger.debug('Scanner waiters: %s' %self.waiters)
        logger.debug('Scanner limit: %s' %self.limit)

    def run(self):
        try:
            concurrent_worker(self.worker_generator(), self.limit)
        except Exception:
            logger.error('Scanner: Unexpected Error: %s' %traceback.format_exc())

    def worker_generator(self):
        while len(self.waiters) > 0:
            for host, port in self.waiters.pop(0):
                yield (self.worker, (host, port), NO_KWARGS)

    def worker(self, host, ports):
        for w in self.workers:
            for port in ports:
                if w.processHostPort(host, port) == SKIP_HOST: return
