from ..utils import assertRaisesMessage

from vulnscanner.workers.http_response import HttpResponseWorker, BaseModule

class TestModule(BaseModule):
    def __init__(self, processGotCalled):
        self.processGotCalled = processGotCalled

    def processResult(self, result, method, path):
        self.processGotCalled = True

tm = TestModule(False)

def test_HttpResponseWorker_addModule_1():
    worker = HttpResponseWorker({'timeout': 3, 'modules': []})
    assert worker.methods_paths_options_modules == []

def test_HttpResponseWorker_addModule_2():
    # Should throw error if requested method is not recognized
    worker = HttpResponseWorker({'timeout': 3, 'modules': []})
    assertRaisesMessage(
        Exception,
        'Illegal method "PET" for module "TestModule" and path "/test/test.html"',
        worker.addModule, tm, 'PET', '/test/test.html')

def test_HttpResponseWorker_addModule_3():
    # Should add default processResult module method to internal dict
    worker = HttpResponseWorker({'timeout': 3, 'modules': []})
    worker.addModule(tm, 'GET', '/test/test.html')
    assert worker.methods_paths_options_modules == [
        ['GET', '/test/test.html', {}, tm.processResult]
    ]

def test_HttpResponseWorker_addModule_4():
    # Should throw error if we try to add the same module method for the same path twice
    worker = HttpResponseWorker({'timeout': 3, 'modules': []})
    worker.addModule(tm, 'GET', '/test/test.html')
    assertRaisesMessage(
        Exception,
        'Module "TestModule" tried to add the same callable "processResult" for the same path "/test/test.html" twice',
        worker.addModule,
        tm,
        'GET',
        '/test/test.html')

def test_HttpResponseWorker_addModule_5():
    # Should be possible to bind a module callable on a POST method with some additional options
    worker = HttpResponseWorker({'timeout': 3, 'modules': []})
    worker.addModule(
        tm, 'POST', '/test/test.html', {'user-agent': 'Firefox 10'})
    assert worker.methods_paths_options_modules == [
        ['POST', '/test/test.html', {'user-agent': 'Firefox 10'}, tm.processResult]
    ]

def test_HttpResponseWorker_addModule_6():
    # Should be possible to bind an non standard module callable
    worker = HttpResponseWorker({'timeout': 3, 'modules': []})
    c2 = lambda *kargs: True
    worker.addModule(tm, 'GET', '/test/test.html')
    worker.addModule(tm, 'GET', '/test/test.html', {}, c2)
    assert worker.methods_paths_options_modules == [
        ['GET', '/test/test.html', {}, tm.processResult, c2]
    ]

def test_HttpResponseWorker_addModule_7():
    # Should be possible to bind another module callable to the same route but
    # with different options
    worker = HttpResponseWorker({'timeout': 3, 'modules': []})
    c2 = lambda *kargs: True
    worker.addModule(tm, 'GET', '/test/test.html', {}, tm.processResult, c2)
    worker.addModule(tm, 'GET', '/test/test.html', {'user-agent': 'Foobar'}, c2)
    assert worker.methods_paths_options_modules == [
        ['GET', '/test/test.html', {}, tm.processResult, c2],
        ['GET', '/test/test.html', {'user-agent': 'Foobar'}, c2]
    ]
