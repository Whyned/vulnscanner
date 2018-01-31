import random

from .HostPortWaiterInterface import HostPortWaiterInterface

class RandomIPv4Waiter(HostPortWaiterInterface):
    """
    HostPortWaiter which generates random ipv4 adresses
    """
    def __init__(self, options):
        self.ports = options['ports']
        self.limit_generate = options.get('limit_generate', -1)

    def generator(self):
        while self.limit_generate != 0:
            randomIPv4 = generateRandomIPv4()
            yield (randomIPv4, self.ports)
            if self.limit_generate != -1:
                self.limit_generate -= 1

def generateRandomIPv4():
    """
    Helper method to generate a random ipv4 adress
    """
    return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))
