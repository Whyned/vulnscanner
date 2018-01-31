import threading

NO_KARGS = []
NO_KWARGS = {}

def concurrent_worker(worker_generator, limit):
    """
    Executes parallel workers. We don't execute more than by limit defined
    workers at the same time. Workers need to get produced by worker_generator
    which is a function which should return a tuple with 3 elements where the
    first element is a reference to the worker function, second kargs and third
    kwargs. If worker_generator can't produce any more workers, it's enough to
    return False.
    """

    work_loader_lock = threading.Lock()
    def work_loader():
        while True:
            work_loader_lock.acquire()
            try:
                worker, kargs, kwargs = next(worker_generator)
            except StopIteration:
                worker = False
            work_loader_lock.release()

            if worker is False: break
            worker(*kargs, **kwargs)

    threads = []
    for i in range(0, limit):
        t = threading.Thread(target=work_loader)
        t.start()
        threads.append(t)

    # Block till all threads are finished
    while len(threads) > 0: threads.pop(0).join()
