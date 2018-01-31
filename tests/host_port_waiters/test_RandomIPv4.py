import re

from ..utils_test import assertRaises

from vulnscanner.host_port_waiters.RandomIPv4 import generateRandomIPv4
from vulnscanner.host_port_waiters.RandomIPv4 import RandomIPv4Waiter

re_match_ipv4 = re.compile('^(([01]?[0-9]?[0-9]|2[0-4][0-9]|2[5][0-5])\.){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|2[5][0-5])$')

def test_generateRandomIPv4():
    """
    Should only generate valid ipv4 adresses
    """
    for i in range(0, 200):
        assert re_match_ipv4.match(generateRandomIPv4()) is not None

def test_RandomIPv4Waiter_1():
    """
    Generator should return same ip adress for each port, ip adresses should
    be valid ipv4
    """
    r = RandomIPv4Waiter({'ports':(80,8080)})
    generator = r.generator()
    flip = False
    for i in range(0, 200):
        ip, port = next(generator)
        assert re_match_ipv4.match(ip) is not None
        assert port == 8080 if flip else port == 80
        flip = not flip

def test_RandomIPv4Waiter_2():
    """
    Should only generate as many ipv4 adresses as defined in
    options.limit_generate
    """
    r = RandomIPv4Waiter({'ports':(80,8080), 'limit_generate': 200})
    generator = r.generator()
    flip = False
    for i in range(0, 401):
        if i == 400:
            assertRaises(StopIteration, next, generator)
            break

        ip, port = next(generator)
        assert re_match_ipv4.match(ip) is not None
        assert port == 8080 if flip else port == 80
        flip = not flip
