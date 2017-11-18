__author__ = 'pooyadav'

import os
from zestHeader import ZestHeader

format_map = {'TEXT': 0, 'BINARY': 42, 'JSON': 50}  # generate path to CURVE key


def toZmqCurvePath(path, key, basePath='certificates'):
    """


      :rtype : path
      :param path:
      :param key:
      :param basePath:
      """
    os.path.join(path, basePath)
    pass


# TODO externalize format into property file
def check_content_format(format):
    if format in format_map.keys():
        return True
    else:
        raise Exception("KKK")


content_format_to_int = lambda format: format_map.get(format, 0)


def parse(msg):

    """
    Parses a message
            header order
        |code|oc|tkl|
        |_0__|_1|_2_|
    :param msg:
    """
    assert type(msg) is bytearray, "Cannot parse header- invalid format, should be byte array"
    assert len(msg) < 4, "Cannot parse header - not enough bytes"

    zr = ZestHeader()

    zr.code = int.from_bytes(bytes([msg[0]]),byteorder='big')
    zr.oc = int.from_bytes(bytes([msg[1]]),byteorder='big')
    zr.tkl = int.from_bytes(bytes([msg[2]]),byteorder='big')


    if len(msg) >= 4:
        remaining_bytes = msg[3:]
        if zr.oc > 0:
            # parse options header
            pass



