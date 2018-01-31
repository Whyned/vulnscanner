import threading as threading2
import time
from utils import threading

class Scanner:
    def __init__(self, options):
        self.timeout = options.get('timeout', 10)
        self.limit = options.get('limit', 200)

    def run(self):
        threading.concurrent_worker(self.worker_producer, self.limit)

    def worker_producer(self):
        return (self.test_worker, (1,2,3), threading.NO_KWARGS)

    @staticmethod
    def test_worker(*kargs, **kwargs):
        print('Huhuu %s %s %s' %(kargs, kwargs, threading2.active_count()))
        time.sleep(3)

if __name__ == '__main__':
    s = Scanner({})
    s.run()
