from vulnscanner.workers import Worker, SKIP_HOST

ALLOWED_METHODS = ['GET', 'POST']

class HttpResponseWorker(Worker):
    def __init__(self, options):
        self.timeout = options['timeout']
        self.modules = options['modules']
        self.methods_paths_options_modules = {}

    def addModuleMethodPathOptionsCallable(self, module, method, path, options={}, callable=None):
        if method not in ALLOWED_METHODS:
            raise Exception('Illegal method "%s" for module "%s" and path "%s"' %(method, type(module).__name__, path))

        if method not in self.methods_paths_options_modules:
            self.methods_paths_options_modules[method] = {}
        if path not in self.methods_paths_options_modules[method]:
            self.methods_paths_options_modules[method][path] = []

        option_callable_index = None
        for i in range(0, len(self.methods_paths_options_modules[method][path])):
            if self.methods_paths_options_modules[method][path][i][0] == options:
                option_callable_index = i
                break
        if option_callable_index is None:
            self.methods_paths_options_modules[method][path].append([options])
            option_callable_index = len(self.methods_paths_options_modules[method][path]) - 1

        if callable is None:
            callable = module.processResult
        if callable in self.methods_paths_options_modules[method][path][option_callable_index]:
            raise Exception('Module "%s" tried to add the same method "%s" for the same path "%s" twice' %(type(module).__name__, method, path))
        self.methods_paths_options_modules[method][path][option_callable_index].append(callable)


    def processHostPort(self, host, port):
        for method_paths_modules in self.operation_paths:
            method = method_paths_modules[0]
            paths_modules = method_paths_modules[1]
            for path_modules in paths_modules:
                path = path_modules[0]
                modules = path_modules[1]
                for module in modules:
                    module(result, method, path)


class BaseModule():
    def __init__(self):
        pass

    def registerMethodsAndPaths(self):
        return [
            ('GET', '/admin/index.html')
        ]

    def processResult(result, method, path):
        pass
def test_module(method, path):
    print(method, path)
