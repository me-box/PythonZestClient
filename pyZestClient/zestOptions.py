__author__ = 'pooyadav'

import logging
import struct


class ZestOptions:
    def __init__(self, number, value,length=None,logger=None):
        self.number = number
        self.value = value
        self.length = len(str(value))

    def marshal(self):
        b = list()
        b.append(bytes([self.number]))
        b.append(bytes([self.length]))
        b.append(self.value.encode())
        return b

    def unmarshal(self,packed_data):
        if len(packed_data) <4:
            raise PyZestException("Not enough bytes to unmarshall")
        self.number = int.from_bytes(packed_data[0],byteorder='big')
        self.length = int.from_bytes(packed_data[1],byteorder='big')
        self.value = packed_data[2].decode("utf-8")




