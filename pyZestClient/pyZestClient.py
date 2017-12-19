__author__ = 'pooyadav'

import logging
import struct
import os

import zmq

import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

import zestOptions
import zestHeader
import pyZestUtil
import socket as sc
import json

import pickle as p

from Exception.PyZestException import PyZestException
from Exception.PyZestException import IllegalFormatException


class PyZestClient:
    def __init__(self, server_key, end_point, logger=None):
        """

        :param server_key:
        :param end_point:
        :param certificate_file - Client certificate file used to establish conn with the Server using CURVE zmq api
        """

        self.logger = logger or logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        self.serverKey = server_key
        self.endpoint = end_point
        self.logger.debug("Connecting to the server")
        try:
            ctx = zmq.Context()
            auth = ThreadAuthenticator(ctx)
            auth.start()
            auth.configure_curve(domain='*', location=zmq.auth.CURVE_ALLOW_ANY)
            self.socket = ctx.socket(zmq.REQ)
            # client_public, client_secret = zmq.auth.load_certificate(certificate_file)
            client_public, client_secret = zmq.curve_keypair()
            self.socket.curve_secretkey = client_secret
            self.socket.curve_publicKey = client_public

            self.socket.curve_serverKey = bytes(server_key)
           # self.socket.setsockopt_string("curve_serverKey", server_key)
            self.socket.connect(end_point)
            self.logger.info('Connection established with ' + end_point)

        except zmq.ZMQError as e:
            self.logger.error("Cannot establish connection" + e.message)


    def post(self):
        """


        """
        self.logger.debug("Posting data to the .. ")
        pass

    def get(self,  path, contentFormat,tokenString=None):
        """

        :param tokenString:
        :param path:
        :param contentFormat:
        """
        self.logger.debug("Getting data from the endpoint")
        header = pyZestUtil.zestHeader()
        header["code"]= 1
        header["token"] = tokenString

        print("header" + str(header))


        # set header options
        options = []
        options.append(zestOptions.ZestOptions(number=11, value=path))
        options.append(zestOptions.ZestOptions(number=3, value=sc.gethostname()))
        # options.append(zestOptions.ZestOptions(number=12, value=bytearray(
        #     struct.pack('B', pyZestUtil.content_format_to_int(contentFormat)))))
        options.append(zestOptions.ZestOptions(number=12, value= str(pyZestUtil.content_format_to_int(contentFormat))))
        header["options"] = options

        # header marshal into bytes
        header_into_bytes = pyZestUtil.marshalZestHeader(header)
        try:
            x=p.dumps(header_into_bytes)
            print(x)
            response = self.send_request_and_await_response(x)
            print("Some response received"+response)
            return response.payload
        except Exception as e:
            self.logger.error("Error in sending request "+ e.message)

        pass

    def observe(self):
        pass

    def send_request_and_await_response(self, request):
        self.logger.info(" Sending request ...")
        try:
            if self.socket.closed:
                self.logger.error("No active connection")
            else:
                try:
                    self.socket.send(request)
                except Exception as e:
                    self.logger.error("Error appeared" + e.message)
                try:
                    response = self.socket.recv(flags=0)
                    #response = self.socket.recv_pyobj(flags=0)
                    print("Response received "+ str(response))
                except Exception as e:
                    self.logger.error("Didn't get reponse " + e.message)
                parsed_response = self.handle_response(response)
                return parsed_response

        except Exception as e:
            self.logger.error("Cannot send request " + e.message)

    def handle_response(self, msg):
        """

        :param msg: Response from the server

        """
        self.logger.info(" Received response ...")
        zr = zestHeader.ZestHeader()
        try:
            zr.parse(msg)
            if zr.code == 65:
                return zr
            elif zr.code == 69:
                return zr
            elif zr.code == 128:
                # Code 128 corresponds to bad request
                raise PyZestException(zr, "Bad Request")
            elif zr.code == 129:
                raise PyZestException(zr, "Unauthorized request")
            elif zr.code == 143:
                raise PyZestException(zr, "UnSupported content format")
            else:
                raise PyZestException(zr, "Invalid code" + str(zr.code))

        except PyZestException as e:
            self.logger.error("Cannot parse the message " + e.message)


def main():
    p=PyZestClient('vl6wu0A@XP?}Or/&BR#LSxn>A+}L)p44/W[wXL3<',"tcp://127.0.0.1:5555")
    p.get(tokenString="",path='/kv/foo',contentFormat="JSON")

if __name__=="__main__":
    logging.info("Begin")
    main()

