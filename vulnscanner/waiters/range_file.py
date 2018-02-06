import socket
import struct

from . import WaiterInterface

class RangeFileWaiter(WaiterInterface):
    def __init__(self, options):
        self.file = open(options['file'], 'r')
        self.ports = options['ports']

    def generator(self):
        for line in self.file:
            line = line.strip()
            pos = line.find(' ')
            if pos == -1 or pos == len(line) -1 or line[0] == '#':
                continue
            start_addr, end_addr = [line[0:pos], line[pos+1:]]
            for curr_addr in ipv4_range(start_addr, end_addr):
                yield(curr_addr, self.ports)

def ipv4_range(start_addr, end_addr):
    start_int = ipv4_to_int(start_addr)
    end_int = ipv4_to_int(end_addr)
    if start_int > end_int:
        raise Exception('Start range is lower than end range')

    for curr_int in range(start_int, end_int+1):
        yield(int_to_ipv4(curr_int))

def ipv4_to_int(addr):
    return struct.unpack("!I", socket.inet_aton(addr))[0]

def int_to_ipv4(addr):
    return socket.inet_ntoa(struct.pack("!I", addr))
