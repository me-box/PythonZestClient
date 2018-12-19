import pythonzestclient
import sys, getopt

zestEndpoint="tcp://127.0.0.1:5555"
zestDealerEndpoint="tcp://127.0.0.1:5556"
CORE_STORE_KEY="vl6wu0A@XP?}Or/&BR#LSxn>A+}L)p44/W[wXL3<"
tokenString=b"secrete"

client = pythonzestclient.PyZestClient(CORE_STORE_KEY,zestEndpoint,zestDealerEndpoint)


cmd = input("input request > ")
while cmd != 'exit()':
    args = cmd.split()

    if args[0] == 'get':
        try:
            contentFormat, path = args[1:3]
            print(f"Sending {args[0]} request...")
            # request example: get json /kv/test/key
            print("Response: ", client.get(path, contentFormat,tokenString))
        except:
            print("ERROR: wrong number of arguments")

    elif args[0] == 'post':
        try:
            contentFormat, path, payLoad = args[1:4]
            print(f"Sending {args[0]} request...")
            # request example: post json /kv/test/key "{\"name\":\"tosh\",\"age\":38}"}
            print("Response: ", client.post(path, payLoad, contentFormat, tokenString))
        except:
            print("ERROR: wrong number of arguments")

    elif args[0] == 'delete':
        try:
            contentFormat, path = args[1:3]
            print(f"Sending {args[0]} request...")
            # request example: delete json /kv/test/key
            print("Response: ", client.delete(path, contentFormat, tokenString))
        except:
            print("ERROR: wrong number of arguments")

    elif args[0] == 'observe':
        try:
            contentFormat, path, observeMode, timeOut = args[1:5]
            print(f"Sending {args[0]} request...")
            # request example: observe json /kv/test/key data 0
            print("Response: ", client.observe(path, contentFormat, tokenString, observeMode, int(timeOut)))
        except:
            print("ERROR: wrong number of arguments")
    else:
        print("ERROR: unsupported request method")
        
    cmd = input("input request > ")
