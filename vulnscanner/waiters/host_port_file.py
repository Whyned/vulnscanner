import random

from . import WaiterInterface

class HostPortFileWaiter(WaiterInterface):
    def __init__(self, options):
        self.file = open(options['file'], 'r')


    def generator(self):
        for line in self.file:
            line = line.strip()
            pos = line.find(':')
            if pos == -1 or pos == len(line)-1 or line[0] == '#':
                continue
            host = line[:pos]
            try:
                port = int(line[pos+1:])
            except ValueError:
                continue
            yield(host, [port])
