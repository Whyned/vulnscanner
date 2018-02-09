from vulnscanner.workers import Worker, SKIP_HOST

ALLOWED_METHODS = ['GET', 'POST']

class HttpResponseWorker(Worker):
    def __init__(self, options):
        self.timeout = options['timeout']
        self.modules = options['modules']
        self.methods_paths_options_modules = []

    def addModule(self, module, method, path, options={}, *callables):
        if method not in ALLOWED_METHODS:
            raise Exception(
                'Illegal method "%s" for module "%s" and path "%s"'
                %(method, type(module).__name__, path))

        if len(callables) == 0:
            callables = [module.processResult]

        indexMPOMC = None
        for i in range(0, len(self.methods_paths_options_modules)):
            mpomc = self.methods_paths_options_modules[i]
            if mpomc[0] == method and mpomc[1] == path and mpomc[2] == options:
                for c in callables:
                    if c in mpomc[3:]:
                        raise Exception(
                            'Module "%s" tried to add the same callable "%s" for the same path "%s" twice'
                            %(type(module).__name__, c.__name__, path))
                indexMPOMC = i
                break

        if indexMPOMC is None:
            self.methods_paths_options_modules.append(
                [method, path, options, *callables])
        else:
            self.methods_paths_options_modules[indexMPOMC].append(*callables)

    def processHostPort(self, host, port):
        for mpom in self.iterateMPOM():
            method, route, options = mpom[0], mpom[1], mpom[2]
            callables = mpom[3:]


class BaseModule():
    def __init__(self):
        pass

    def registerMPOM(self):
        pass

    def processResult(result, method, path, options):
        pass
