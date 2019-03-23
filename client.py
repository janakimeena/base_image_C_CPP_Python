#!/usr/bin/python3
import zmq

port = "5557"

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
# socket.connect ("tcp://ec2-18-216-14-94.us-east-2.compute.amazonaws.com:%s" % port)
socket.connect ("tcp://13.233.110.224:%s" % port)
# socket.connect ("tcp://35.200.198.80:%s" % port)
# socket.connect("tcp://18.216.14.94:%s" % port)
#socket.connect("tcp://35.200.177.245:%s" % port)

'''with open("main.c") as file:  
    codeC = file.read() '''
with open("main.cpp") as file:  
    codeCPP = file.read() 
'''with open("main.py") as file:  
    codePython = file.read() '''



'''with open("main_testcase.c") as file:
    codeCTestCase = file.read()'''
with open("main_testcase.cpp") as file:
    codeCPPTestCase  = file.read()
'''with open("main_testcase.py") as file:
    codePythonTestCase  = file.read()'''

# codeC = '#include <stdio.h>\nvoid main(){\nprintf("Hello World");}\n'
# codeCPP = '#include <iostream>\nusing namespace std;\nint  main(){\ncout<<"Hello world from C++";\nreturn 0;\n}\n'
# codePython = 'import time\nprint "HelloWorld From Python"'

#  Do 2 requests, waiting each time for a response without test case
# for request in range(1):
#     print ("Sending request ", "...")
#     socket.send_json ({'language': 'C', 'code': codeC, 'id':"mainc"})
#     #  Get the reply.
#     message = socket.recv_json()
#     print ("Received reply ",  "[", message, "]")
#
#     print ("Sending request ", "...")
#     socket.send_json({'language': 'CPP', 'code': codeCPP, 'id': "maincpp"})
#     #  Get the reply.
#     message = socket.recv_json()
#     print ("Received reply ", "[", message, "]")
#
#     print ("Sending request ", "...")
#     socket.send_json ({'language': 'Python', 'code': codePython, 'id': "main"})
#     #  Get the reply.
#     message = socket.recv_json()
#     print ("Received reply ",  "[", message, "]")

#  Do 2 requests, waiting each time for a response with test case
for request in range(1):
    '''print ("Sending request ", "...")
    socket.send_json ({'language': 'C', 'code': codeC, 'id':"mainc", 'testcasepresent': True, 'testcase': codeCTestCase})
    #  Get the reply.
    message = socket.recv_json()
    print ("Received reply ",  "[", message, "]")'''
    #
    print ("Sending request ", "...")
    socket.send_json({'language': 'CPP', 'code': codeCPP, 'id': "maincpp", 'testcasepresent': True, 'testcase': codeCPPTestCase})
    #  Get the reply.
    message = socket.recv_json()
    print ("Received reply ", "[", message, "]")

    '''print ("Sending request ", "...")
    socket.send_json ({'language': 'Python', 'code': codePython, 'id': "main", 'testcasepresent': True, 'testcase': codePythonTestCase, 'timeout': '5s'})
    #  Get the reply.
    message = socket.recv_json()
    print ("Received reply ",  "[", message, "]")'''



