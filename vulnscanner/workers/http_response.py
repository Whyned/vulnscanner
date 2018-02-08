from vulnscanner.workers import Worker, SKIP_HOST

ALLOWED_METHODS = ['GET', 'POST']

class HttpResponseWorker(Worker):
    def __init__(self, options):
        self.timeout = options['timeout']
        self.modules = options['modules']
        self.methods_paths_options_modules = {}

    def addModuleMethodPathOptionsCallable(self, module, method, path, options={}, callable=None):
        if method not in ALLOWED_METHODS:
            raise Exception(
                'Illegal method "%s" for module "%s" and path "%s"'
                %(method, type(module).__name__, path))

        mpom = self.methods_paths_options_modules
        if method not in mpom:
            mpom[method] = {}
        if path not in mpom[method]:
            mpom[method][path] = []

        option_callable_index = None
        for i in range(0, len(mpom[method][path])):
            if mpom[method][path][i][0] == options:
                option_callable_index = i
                break
        if option_callable_index is None:
            mpom[method][path].append([options])
            option_callable_index = len(mpom[method][path]) - 1

        if callable is None:
            callable = module.processResult
        if callable in mpom[method][path][option_callable_index]:
            raise Exception(
                'Module "%s" tried to add the same method "%s" for the same path "%s" twice'
                %(type(module).__name__, method, path))
        mpom[method][path][option_callable_index].append(callable)

    def iterateMPOM(self):
        mpom = self.methods_paths_options_modules
        for (method, path_options_callables) in mpom.items():
            for (path, options_callables) in mpom[method].items():
                for options_callables in options_callables:
                    options = options_callables[0]
                    for callable in options_callables[1:]:
                        yield (method, path, options, callable)

    def processHostPort(self, host, port):
        for (method, path, options, callable) in self.iterateMPOM():
            pass


class BaseModule():
    def __init__(self):
        pass

    def registerMPOM(self):
        return [
            ('GET', '/admin/index.html')
        ]

    def processResult(result, method, path, options):
        pass
def test_module(method, path):
    print(method, path)
