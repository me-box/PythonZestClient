__author__ = 'pooyadav'

import logging
import struct
import os

import binascii
import zmq

import zmq.auth
from zmq.auth.thread import ThreadAuthenticator

import pyZestUtil
import socket as sc


from Exception.PyZestException import PyZestException

dealer_endpoint = ""

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
            client_public, client_secret = zmq.curve_keypair()
            self.socket.curve_secretkey = client_secret
            self.socket.curve_publicKey = client_public

            self.socket.curve_serverKey = bytes(server_key, 'utf8')
           # self.socket.setsockopt_string("curve_serverKey", server_key)
            self.socket.connect(end_point)
            self.logger.info('Connection established with ' + end_point)

        except zmq.ZMQError as e:
            self.logger.error("Cannot establish connection" + e.message)


    def post(self,path, payLoad, contentFormat,tokenString=None):

        self.logger.debug("Posting data to the endpoint")
        header = pyZestUtil.zestHeader()
        header["code"] = 2
        header["token"] = tokenString
        header["tkl"] = len(tokenString)
        header["payload"] = payLoad
        header["oc"] = 3
        print("header " + str(header))


        # set header options
        options = []
        options.append({"number":11,
        "len": len(path),
        "value": path,})

        options.append({"number": 3,
                        "len": len(sc.gethostname()),
                        "value": sc.gethostname(),})

        options.append({"number": 12,
                        "len": 2,
                        "value": pyZestUtil.content_format_to_int(contentFormat),})

        print(options)
        header["options"] = options
        # header marshal into bytes
        header_into_bytes = pyZestUtil.marshalZestHeader(header)

        try:
            print("data "+ str(header_into_bytes))
            response = self.send_request_and_await_response(header_into_bytes)
            try:
                parsed_response = self.handle_response(response)
            except Exception as e:
                self.logger.error("Error in handling response " + str(e.args))

                return parsed_response["payload"]
        except Exception as e:
            self.logger.error( "Message sending error  " + str(e.args))



    def get(self, path, contentFormat, tokenString=None):
        self.logger.debug("Getting data from the endpoint")
        header = pyZestUtil.zestHeader()
        header["code"] = 1
        header["token"] = tokenString
        header["tkl"] = len(tokenString)
        header["oc"] = 3
        print("header " + str(header))


        # set header options
        options = []
        options.append({"number":11,
        "len": len(path),
        "value": path,})

        options.append({"number": 3,
                        "len": len(sc.gethostname()),
                        "value": sc.gethostname(),})

        options.append({"number": 12,
                        "len": 2,
                        "value": pyZestUtil.content_format_to_int(contentFormat),})

        print(options)
        header["options"] = options

        # header marshal into bytes
        header_into_bytes = pyZestUtil.marshalZestHeader(header)

        try:
            print("data "+ str(header_into_bytes))
            response = self.send_request_and_await_response(header_into_bytes)
            try:
                parsed_response = self.handle_response(response)
            except Exception as e:
                self.logger.error("Error in handling response " + str(e.args))
            return parsed_response["payload"]
        except Exception as e:
            self.logger.error( "Message sending error  " + str(e.args))


    def observe(self, path, contentFormat, tokenString=None, timeOut = 0):
        self.logger.debug("Observing data from the endpoint")
        header = pyZestUtil.zestHeader()
        header["code"] = 1
        header["token"] = tokenString
        header["tkl"] = len(tokenString)
        header["oc"] = 5
        print("header " + str(header))
        options = []
        options.append({"number": 11,
                        "len": len(path),
                        "value": path,})
        options.append({"number": 3,
                        "len": len(sc.gethostname()),
                        "value": sc.gethostname(),})
        options.append({"number": 6,
                    "len": 0,
                    "value":"",})
        options.append({"number": 12,
                    "len": 2,
                    "value": pyZestUtil.content_format_to_int(contentFormat),})
        options.append({"number": 14,
                        "len": 4,
                        "value": timeOut,})
        print(options)
        header["options"] = options

        header_into_bytes = pyZestUtil.marshalZestHeader(header)
        try:
            print("data: "+ str(header_into_bytes))
            response = self.send_request_and_await_response(header_into_bytes)
            try:
                parsed_response = self.handle_response(response)
            except Exception as e:
                self.logger.error("Error in handling response " + str(e.args))
                print(parsed_response)
                return parsed_response["payload"]
        except Exception as e:
            self.logger.error( "Message sending error  " + str(e.args))

    def resolve(self, header):
        print("Inside resolve")
        newCtx = zmq.Context()
        dealer = newCtx.socket(zmq.DEALER)
        try:
            print(header["options"])
            #dealer.identity = header["payload"]
        except Exception as e:
            self.logger.error("Error setting identity" + str(e.args))

        for i in range(len(header["options"])):
            if(header["options"][i]["number"] == 0):
                serverKeyOption = header["options"][i]
                print(serverKeyOption)
                serverKey = serverKeyOption["value"]
                print("Identity" + str(header["payload"]))
                print(type(serverKey))

        client_public, client_secret = zmq.curve_keypair()
        dealer.curve_secretkey = client_secret
        dealer.curve_publicKey = client_public
        dealer.curve_serverKey = bytes(binascii.hexlify(serverKey.encode('utf-8')))
        dealer.connect(dealer_endpoint)

    def send_request_and_await_response(self, request):
        self.logger.info(" Sending request ...")
        try:
            if self.socket.closed:
                self.logger.error("No active connection")
            else:
                try:
                    self.socket.send(request)
                except Exception as e:
                    self.logger.error("Error appeared " + str(e.args))
                try:
                    response = self.socket.recv(flags=0)
                    print("Response received "+ str(response))
                    return response
                except Exception as e:
                    self.logger.error("Didn't get reponse " + str(e.args))
        except Exception as e:
            self.logger.error("Cannot send request " + str(e.args))

    def handle_response(self, msg):
        """

        :param msg: Response from the server

        """
        self.logger.info(" Received response ...")
        zr = pyZestUtil.parse(msg)
        #zr = zestHeader.ZestHeader()
        try:
            #zr.parse(msg)
            if zr["code"] == 65:
                print("Code 65 received")
                return zr
            elif zr["code"] == 69:
                print("Code 69 received")
                self.resolve(zr)
                return;
            elif zr["code"]== 128:
                # Code 128 corresponds to bad request
                raise PyZestException(zr, "Bad Request")
            elif zr["code"] == 129:
                raise PyZestException(zr, "Unauthorized request")
            elif zr["code"] == 143:
                raise PyZestException(zr, "UnSupported content format")
            else:
                raise PyZestException(zr, "Invalid code" + str(zr.code))

        except PyZestException as e:
            self.logger.error("Cannot parse the message " + str(e.args))


def main():
    p=PyZestClient('vl6wu0A@XP?}Or/&BR#LSxn>A+}L)p44/W[wXL3<',"tcp://127.0.0.1:5555")
    p.get(tokenString="",path='/kv/foo',contentFormat="JSON")
    p.post(tokenString="",path='/kv/test',payLoad='{"name":"testuser", "age":35}', contentFormat="JSON")
    p.get(tokenString="",path='/kv/test',contentFormat="JSON")
    p.observe(tokenString="",path='/kv/test',contentFormat="JSON", timeOut=30)
if __name__=="__main__":
    logging.info("Begin")
    main()

