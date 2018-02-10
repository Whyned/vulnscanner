from vulnscanner import logger
from vulnscanner.workers import Worker, SKIP_HOST
from vulnscanner.utils import http_request

ALLOWED_METHODS = ['GET', 'POST']

class HttpResponseWorker(Worker):
    def __init__(self, options):
        self.timeout = options['timeout']
        self.methods_paths_options_modules = []
        self.modules = []
        if 'modules' not in options or len(options['modules']) == 0:
            logger.warn('HttpResponseWorker got initialized without options.modules')
        else:
            self.registerModules(options['modules'])

    def registerModules(self, modules):
        for m in modules:
            logger.debug('HttpResponseWorker registering module %s' %m)
            mpoms = m.registerMPOM()
            for mpom in mpoms:
                self.addMPOM(m, *mpom)

    def addMPOM(self, module, method, path, options={}, *callables):
        if method not in ALLOWED_METHODS:
            raise Exception(
                'Illegal method "%s" for module "%s" and path "%s"'
                %(method, module.__class__.__name__, path))

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
                            %(module.__class__.__name__, c.__name__, path))
                indexMPOMC = i
                break

        if indexMPOMC is None:
            mpom = [method, path, options]
            for c in callables:
                mpom.append(c)
            self.methods_paths_options_modules.append(mpom)
        else:
            self.methods_paths_options_modules[indexMPOMC].append(*callables)

    def processHostPort(self, host, port):
        for mpom in self.methods_paths_options_modules:
            method, path, options = mpom[0], mpom[1], mpom[2]
            callables = mpom[3:]

            result = http_request(host, port, method, path, options)

            for c in callables:
                c(return_request, method, path, options)
