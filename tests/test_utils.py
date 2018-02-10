import unittest
import time
import threading as threading2


from vulnscanner.utils import concurrent_worker
from vulnscanner import logger
logger.attach()

called_workers = 0
max_active_threads = 0
def test_concurrent_worker():
    """
    Should create 200 concurrent workers,
    Should have released all threads after concurrent_worker() unblocks
    """
    global called_workers
    global max_active_threads

    kargs = [42]
    kwargs = {'bar': True}
    limit = 200
    def worker_generator():
        for i in range(0, limit):
            yield (worker, kargs, kwargs)


    def worker(*tkargs, **tkwargs):
        global called_workers
        global max_active_threads
        called_workers += 1
        ac = threading2.active_count()
        if ac > max_active_threads:
            max_active_threads = ac
        time.sleep(0.5)

    concurrent_worker(worker_generator(), limit)
    assert threading2.active_count() == 1
    assert called_workers == limit
    assert max_active_threads == limit + 1
