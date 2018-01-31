import unittest
import time
import threading as threading2

from vulnscanner.utils import threading

def test_start_new_thread():
    """
    Should execute passed function in a new thread and pass all kargs/kwargs to it.
    Should additionally return the thread object.
    """
    test_start_new_thread.got_called = False
    def test_fnc(a,b,c, d=0):
        test_start_new_thread.got_called = True
        assert a == 1
        assert b == 2
        assert c == 3
        assert d == 5
    t = threading.start_new_thread(test_fnc, 1, 2, 3, d=5)
    t.join()
    assert test_start_new_thread.got_called is True

def test_start_new_thread_cb():
    """
    Should start a new thread and execute passed callback method when thread is finished.
    """
    test_start_new_thread_cb.fnc_got_called = False
    test_start_new_thread_cb.cb_got_called = False

    def test_fnc(a,b,c, d=0):
        test_start_new_thread_cb.fnc_got_called = True
        assert a == 1
        assert b == 2
        assert c == 3
        assert d == 5

    def callback():
        test_start_new_thread_cb.cb_got_called = True

    t = threading.start_new_thread_cb(test_fnc, callback, 1, 2, 3, d=5)
    t.join()
    assert test_start_new_thread_cb.fnc_got_called is True
    assert test_start_new_thread_cb.cb_got_called is True

def test_concurrent_worker():
    test_concurrent_worker.produced_workers = 0
    def worker_producer():
        if test_concurrent_worker.produced_workers >= 200:
            return False
        test_concurrent_worker.produced_workers += 1
        return (worker, [42], {'bar':True})

    test_concurrent_worker.called_worker = 0
    test_concurrent_worker.max_parallel_workers = 0
    def worker(foo, bar=False):
        assert foo == 42
        assert bar is True
        test_concurrent_worker.called_worker += 1
        ac = threading2.active_count()
        if ac > test_concurrent_worker.max_parallel_workers:
            test_concurrent_worker.max_parallel_workers = ac
        time.sleep(1)

    threading.concurrent_worker(worker_producer, 205)
    assert test_concurrent_worker.produced_workers == 200
    assert test_concurrent_worker.called_worker == 200
    assert test_concurrent_worker.max_parallel_workers == 201
