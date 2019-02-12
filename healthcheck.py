#!/usr/bin/python3
import zmq

port = "5557"

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
# socket.connect ("tcp://ec2-13-250-60-248.ap-southeast-1.compute.amazonaws.com:%s" % port)
socket.connect ("tcp://127.0.0.1:%s" % port)
# socket.connect("tcp://18.216.14.94:%s" % port)

codeC = '#include <stdio.h>\nvoid main(){\nprintf("Hello World");}\n'
print ("Sending request ", "...")
socket.send_json ({'language': 'C', 'code': codeC, 'id':"mainc"})
# #  Get the reply.
message = socket.recv_json()
print (message)
if message['stdout'].rstrip() != 'Hello World':
    print ('not correct')
    raise Exception("Not having good health")
else:
    print ('correct')