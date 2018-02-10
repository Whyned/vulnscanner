import unittest
import time
import threading as threading2


from vulnscanner import logger
from vulnscanner.utils import concurrent_worker, craft_url, http_request
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


def test_craft_url_1():
    # Should return a basic url
    url = craft_url('127.0.0.1', 80)
    assert url == 'http://127.0.0.1:80/'

def test_craft_url_2():
    # Should return a basic url with path
    url = craft_url('127.0.0.1', 8080, '/admin/test.html')
    assert url == 'http://127.0.0.1:8080/admin/test.html'

def test_craft_url_3():
    # Should use https if port is 443
    url = craft_url('127.0.0.1', 443, '/admin/test.html')
    assert url == 'https://127.0.0.1:443/admin/test.html'

def test_craft_url_4():
    # Should NOT use https if port is 443 but ssl=False is added
    url = craft_url('127.0.0.1', 443, '/admin/test.html', ssl=False)
    assert url == 'http://127.0.0.1:443/admin/test.html'

def test_http_requests_1():
    result = http_request('google.de', '80', '/', 'GET', {})
    assert result.status_code == 200
