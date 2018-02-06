import re

from vulnscanner.waiters.random_ipv4 import generateRandomIPv4
from vulnscanner.waiters.random_ipv4 import RandomIPv4Waiter

re_match_ipv4 = re.compile('^(([01]?[0-9]?[0-9]|2[0-4][0-9]|2[5][0-5])\.){3}([01]?[0-9]?[0-9]|2[0-4][0-9]|2[5][0-5])$')

def test_generateRandomIPv4():
    """
    Should on
    ly generate valid ipv4 adresses
    """
    for i in range(0, 200):
        assert re_match_ipv4.match(generateRandomIPv4()) is not None

def test_RandomIPv4Waiter_1():
    """
    Generator should return same ip adress for each port, ip adresses should
    be valid ipv4 adresses
    """
    r = RandomIPv4Waiter({'ports':(80,8080)})
    generator = r.generator()
    for i in range(0, 200):
        ip, ports = next(generator)
        assert re_match_ipv4.match(ip) is not None
        assert ports == (80,8080)

def test_RandomIPv4Waiter_2():
    """
    Should only generate as many ipv4 adresses as defined in
    options.limit_generate
    """
    r = RandomIPv4Waiter({'ports':(80,8080), 'limit_generate': 200})
    generator = r.generator()
    i = 0
    for ip, ports in generator:
        i += 1
    assert i == 200
