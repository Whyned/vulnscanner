from ..utils import assertRaisesMessage, assertRaises

from vulnscanner.waiters.range_file import RangeFileWaiter
from vulnscanner.waiters.range_file import ipv4_to_int
from vulnscanner.waiters.range_file import int_to_ipv4
from vulnscanner.waiters.range_file import ipv4_range

def test_RangeFileWaiter():
    waiter = RangeFileWaiter({
        'ports': [80,8080],
        'file': './test_files/range_file_1.txt'
    })

    generator = waiter.generator()
    for i in range(0, 256):
        ip, ports = next(generator)
        assert ip == '0.0.0.' + str(i)
        assert ports == [80,8080]
    for i in range(0, 5):
        ip, ports = next(generator)
        assert ip == '0.0.1.' + str(i)
        assert ports == [80,8080]
    for i3 in range(0, 256):
        for i4 in range(0, 256):
            assertIp = '1.1.%s.%s' %(str(i3),str(i4))
            ip, ports = next(generator)
            print(ip, assertIp)
            assert ip == assertIp
            assert ports == [80,8080]
    assert next(generator) == ('1.2.0.0', [80,8080])
    assertRaises(StopIteration, next, generator)


def test_ipv4_range():
    generator = ipv4_range('127.0.0.1', '127.0.0.0')
    assertRaisesMessage(
        Exception, 'Start range is lower than end range',
        next, generator)

    generator = ipv4_range('127.0.0.1', '127.0.1.20')
    for i in range(1, 256):
        assert next(generator) == '127.0.0.' + str(i)
    for i in range(0, 21):
        assert next(generator) == '127.0.1.' + str(i)
    assertRaises(StopIteration, next, generator)

def test_ipv4_to_int():
    assert ipv4_to_int('0.0.0.0') == 0
    assert ipv4_to_int('127.0.0.1') == 2130706433

def test_int_to_ipv4():
    assert int_to_ipv4(0) == '0.0.0.0'
    assert int_to_ipv4(2130706433) == '127.0.0.1'
