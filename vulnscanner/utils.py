import threading

NO_KARGS = []
NO_KWARGS = {}

def concurrent_worker(worker_generator, limit):
    """
    This method runs N (limit) workers at the same time, and as soon one
    completes, it will get a new one from worker_generator. worker_generator
    has to be a normal generator (pass it already initialized) which has to
    a tuple with 3 elements. First needs to be a callable (the worker method),
    second kargs and third kwargs.
    This method blocks until worker_generator doesn't yield any more workers
    and all workers are finished.
    """

    work_loader_lock = threading.Lock()
    def work_loader():
        """
        This method should be run in it's own thread and executes one worker
        after the other until worker_generator doesn't yield any more workers.
        """
        while True:
            # With the lock we make sure that only one work_loader tries to
            # get the next worker
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
