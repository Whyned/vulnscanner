from ..utils import assertRaises

from vulnscanner.waiters.host_port_file import HostPortFileWaiter

def test_host_port_waiter_1():
    waiter = HostPortFileWaiter({'file': './test_files/host_port_file_1.txt'})
    generator = waiter.generator()
    assert next(generator) == ('127.0.0.1', [80])
    assert next(generator) == ('13.1', [80])
    assert next(generator) == ('hostname', [80])
    assertRaises(StopIteration, next, generator)
