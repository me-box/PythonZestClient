__author__ = 'pooyadav'

import logging
import struct
import os

import zmq

import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

from zestOptions import ZestOptions
from zestHeader import ZestHeader
import pyZestUtil

import PyZestException
import PyZestException.IllegalFormatException

class PyZestClient:
    def __init__(self, server_key, end_point, logger=None):
        """

        :param server_key:
        :param end_point:
        :param certificate_file - Client certificate file used to establish conn with the Server using CURVE zmq api
        """

        self.logger = logger or logging.getLogger(__name__)
        self.serverKey = server_key
        self.endpoint = end_point
        self.logger.debug("Connecting to the server")
        try:
            ctx = zmq.Context()
            auth = ThreadAuthenticator(ctx)
            auth.start()
            auth.configure_curve(domain='*', location=zmq.auth.CURVE_ALLOW_ANY)
            self.socket = ctx.socket(zmq.REQ)
            #client_public, client_secret = zmq.auth.load_certificate(certificate_file)
            client_public, client_secret=zmq.curve_keypair()
            self.socket.curve_secretkey = client_secret
            self.socket.curve_publicKey = client_public

            self.socket.curve_serverKey = server_key
            self.socket.connect(end_point)
            self.logger.info('Connection established with '+end_point)

        except zmq.ZMQError as e:
            self.logger.error("Cannot establish connection" + e.message)


    def post(self):
        """


        """
        self.logger.debug("Posting data to the .. ")
        pass

    def get(self, tokenString, path, contentFormat):
        """

        :param tokenString:
        :param path:
        :param contentFormat:
        """
        self.logger.debug("Getting data from the endpoint")
        header = ZestHeader(code=1,token=tokenString)

        #set header options
        options=[]
        options.append(ZestOptions(number=11,value=path))
        options.append(ZestOptions(number=3,value=os.uname))
        options.append(ZestOptions(number=12,value=bytearray(struct.pack('B',pyZestUtil.content_format_to_int(contentFormat)))))
        header.options = options

        # header marshal into bytes
        header_into_bytes = header.marshall()
        try:
            response = self.send_request_and_await_response(header_into_bytes)
            return response.payload
        except:
            self.logger.error("Error in sending request")


        pass

    def observe(self):
        pass

    def send_request_and_await_response(self, request):
        self.logger.info(" Sending request ...")
        try:
            if self.socket.closed:
                self.logger.error("No active connection")
            else:
                self.socket.send(request)
                response = self.sock.recv(flags=0)
                parsed_response = self.handle_response(response)
                return parsed_response

        except Exception as e:
            self.logger.error("Cannot send request "+ e.message)

    def handle_response(self, msg):
        """

        :param msg: Response from the server

        """
        self.logger.info(" Received response ...")
        zr = ZestHeader()
        try:
            zr.parse(msg)

        except PyZestException as e:
            self.logger.error("Cannot parse the message "+e.message)



