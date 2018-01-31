import threading

NO_KARGS = []
NO_KWARGS = {}

def start_new_thread(fnc, *kargs, **kwargs):
    """
    Executes passed function in a new threads with kargs/kwargs.
    Returns started thread.
    """
    t = threading.Thread(target=fnc, args=kargs, kwargs=kwargs)
    t.start()
    return t

def start_new_thread_cb(fnc, cb, *kargs, **kwargs):
    """
    Executes passed function in a new thread with kargs/kwargs and executes
    callback as soon as function is finished.
    Returns started thread.
    """
    def wrapped_fnc(*kargs, **kwargs):
        fnc(*kargs, **kwargs)
        cb()
    return start_new_thread(wrapped_fnc, *kargs, **kwargs)

def concurrent_worker(worker_producer, limit):
    """
    Executes parallel workers. We don't execute more than by limit defined
    workers at the same time. Workers need to get produced by worker_producer
    which is a function which should return a tuple with 3 elements where the
    first element is a reference to the worker function, second kargs and third
    kwargs. If worker_producer can't produce any more workers, it's enough to
    return False.
    """
    semaphor = threading.BoundedSemaphore(limit)

    def worker_finished():
        semaphor.release()

    while True:
        semaphor.acquire()
        producer_return = worker_producer()
        if producer_return is False:
            break
        new_worker, kargs, kwargs = producer_return
        #print('Starting new worker with kargs: %s kwargs: %s' %(kargs, kwargs))
        start_new_thread_cb(new_worker, worker_finished, *kargs, **kwargs)

    # Wait till all threads got released
    while semaphor._value > 0:
        print('Waiting for %s workers to finish' %(semaphor._value))
        semaphor.acquire()
