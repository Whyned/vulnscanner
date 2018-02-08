from ..utils import assertRaisesMessage

from vulnscanner.workers.http_response import HttpResponseWorker, BaseModule

class TestModule(BaseModule):
    def __init__(self, processGotCalled):
        self.processGotCalled = processGotCalled

    def processResult(self, result, method, path):
        self.processGotCalled = True

def test_HttpResponseWorker_addModuleMethodPathOptionsCallable_1():
    worker = HttpResponseWorker({'timeout': 3, 'modules': []})

    assert worker.methods_paths_options_modules == {}

    processGotCalled = False
    tm = TestModule(processGotCalled)

    # Should throw error if requested method is not recognized
    assertRaisesMessage(
        Exception,
        'Illegal method "PET" for module "TestModule" and path "/test/test.html"',
        worker.addModuleMethodPathOptionsCallable, tm, 'PET', '/test/test.html')

    # Should add default processResult module method to internal dict
    worker.addModuleMethodPathOptionsCallable(tm, 'GET', '/test/test.html')
    assert worker.methods_paths_options_modules == {
        'GET': {'/test/test.html': [[{}, tm.processResult]]}
    }

    # Should throw error if we try to add the same module method for the same path twice
    assertRaisesMessage(
        Exception,
        'Module "TestModule" tried to add the same method "GET" for the same path "/test/test.html" twice',
        worker.addModuleMethodPathOptionsCallable,
        tm,
        'GET',
        '/test/test.html')

    # Should be possible to bind a module callable on a POST method with some additional options
    worker.addModuleMethodPathOptionsCallable(
        tm, 'POST', '/test/test.html', {'user-agent': 'Firefox 10'})
    assert worker.methods_paths_options_modules == {
        'GET': {'/test/test.html': [[{}, tm.processResult]]},
        'POST': {'/test/test.html': [[{'user-agent': 'Firefox 10'}, tm.processResult]]}
    }

    # Should be possible to bind an non standard module callable
    c2 = lambda *kargs: True
    worker.addModuleMethodPathOptionsCallable(
        tm, 'GET', '/test/test.html', {}, c2)
    assert worker.methods_paths_options_modules['GET'] == {
        '/test/test.html': [[{}, tm.processResult, c2]]
    }

    # Should be possible to bind a nother module callable to the same route but
    # with different options
    worker.addModuleMethodPathOptionsCallable(
        tm, 'GET', '/test/test.html', {'user-agent': 'Foobar'}, c2)
    assert worker.methods_paths_options_modules['GET'] == {
        '/test/test.html': [[{}, tm.processResult, c2], [{'user-agent': 'Foobar'}, c2]]
    }
