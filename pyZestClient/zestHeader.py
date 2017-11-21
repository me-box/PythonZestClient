__author__ = 'pooyadav'

import struct
from zestOptions import ZestOptions




class ZestHeader:
    """ Implementation of the header in the zest protocol @see https://jptmoore.github.io/zest/protocol
    """

    def __init__(self, code=None, tkl=None, payload=None, zest_options=None, oc=None, token=None):
        """

        :param payload: Payload
        :param code: COAP specified
        :param oc: number of options present
        :param zest_options:
        :param tkl: token length if present in the options header
        :param token: Optional parameter.
        """
        self.oc = oc
        self.code = code
        self.tkl = tkl
        self.Token = token

        self.options = zest_options
        self.payload = payload

    def marshall(self):
        """

        :rtype : object
        """
        self.oc = len(self.options)

        # Option token length must be big-endian
        self.tkl = len(self.Token)

        # header attributes marshaled into marshaled_header
        marshaled_header = []
        marshaled_header.append(bytes([self.code]))
        marshaled_header.append(bytes([self.oc]))
        marshaled_header.append(bytes([self.tkl]))
        # marshaled_header = bytearray()
        # marshaled_header.append(struct.pack('B', self.code))
        # marshaled_header.append(struct.pack('B', self.oc))
        # marshaled_header.extend(struct.pack('>H',self.tkl))

        if self.tkl > 0:
            #marshaled_header.append(bytearray(self.Token))
            marshaled_header.append(bytes([self.Token]))


        # append the options
        for opt in self.options:
            try:
                assert isinstance(opt, ZestOptions)
                opt_bytes = opt.marshal()
                marshaled_header.append(opt_bytes)
            except Exception as e:
                raise TypeError("Cannot parse options "+e.message)

        # append payload
        #marshaled_header.append(self.payload)
        return marshaled_header








