import unittest
import time
import threading as threading2


from vulnscanner.utils import concurrent_worker
from vulnscanner import logger
logger.attach()

def test_concurrent_worker():
    """
    Should create 200 concurrent workers,
    Should have released all threads after concurrent_worker() unblocks
    """
    kargs = [42]
    kwargs = {'bar': True}
    limit = 200
    def worker_generator():
        for i in range(0, limit):
            yield (worker, kargs, kwargs)

    test_concurrent_worker.called_workers = 0
    test_concurrent_worker.max_active_threads = 0
    def worker(*tkargs, **tkwargs):
        test_concurrent_worker.called_workers += 1
        ac = threading2.active_count()
        if ac > test_concurrent_worker.max_active_threads:
            test_concurrent_worker.max_active_threads = ac
        time.sleep(0.5)

    concurrent_worker(worker_generator(), limit)
    assert threading2.active_count() == 1
    assert test_concurrent_worker.called_workers == limit
    assert test_concurrent_worker.max_active_threads == limit + 1
