#!/usr/bin/python3
import zmq
import time
import os
import shutil

port = "5557"
print ("Running on port ", port)


context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind("tcp://*:%s" % port)

while True:
    #  Wait for next request from client
    message = socket.recv_json()
    print ("Received request: ", message)
    if os.path.exists('codes'):
        dir_status = "Exist"
    else:
        dir_status = "Do not exist"
    os.makedirs('codes', exist_ok=True)
    # time.sleep(1)
    try:
        out = {'compileout':'', 'compileerror':'', 'stdout':'', 'stderror':'',
               'testcase_compileout':'', 'testcase_compileerror':'', 'testcase_stdout':'', 'testcase_stderror':'',
               'status':'', 'id': message['id'], 'dir':dir_status}
        lang = message['language']
        timestamp = time.time().__str__()

        testcasepresent = message.get('testcasepresent',False)
        timeout = message.get('timeout', '10s')
        code_stdin = message.get('code_stdin','')
        with open('codes/input.txt','w') as f:
            f.write(code_stdin)
        if lang == 'C':
            with open('codes/{}-{}-{}.c'.format(message['id'],port, timestamp), 'w') as f:
                f.write(message['code'])
            print ("excecuting C code ./runcode.sh C {}-{}-{} {}".format(message['id'], port, timestamp,timeout))
            command = './runcode.sh C {}-{}-{} {}'.format(message['id'],port, timestamp, timeout)
            os.system(command)
            if os.path.exists('codes/{}-{}-{}-compileout.txt'.format(message['id'],port, timestamp)):
                with open('codes/{}-{}-{}-compileout.txt'.format(message['id'],port, timestamp), 'r') as myfile:
                    out['compileout'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-compileout.txt'.format(message['id'],port, timestamp)):
                    os.remove('codes/{}-{}-{}-compileout.txt'.format(message['id'],port, timestamp))
            if os.path.exists('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp)):
                with open('codes/{}-{}-{}-erroroutput.txt'.format(message['id'],port, timestamp), 'r') as myfile:
                    out['compileerror'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp))
            if os.path.exists('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                with open('codes/{}-{}-{}-stdout.txt'.format(message['id'],port, timestamp), 'r') as myfile:
                    out['stdout'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp))
            if os.path.exists('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                with open('codes/{}-{}-{}-stderror.txt'.format(message['id'],port, timestamp), 'r') as myfile:
                    out['stderror'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp))
            if os.path.isfile('codes/{}-{}-{}.c'.format(message['id'],port, timestamp)):
                os.remove('codes/{}-{}-{}.c'.format(message['id'],port, timestamp))
            if os.path.isfile('codes/{}-{}-{}.out'.format(message['id'],port, timestamp)):
                os.remove('codes/{}-{}-{}.out'.format(message['id'],port, timestamp))
            if os.path.isfile('codes/timeout.txt'):
                os.remove('codes/timeout.txt')
                out['codetimeout'] = True

            if testcasepresent:
                print ("running testcase")
                with open('codes/{}-{}-{}.c'.format(message['id'], port, timestamp), 'w') as f:
                    f.write(message['testcase'])
                print ("excecuting C code ./runcode.sh C {}-{}-{} {}".format(message['id'], port, timestamp, timeout))
                command = './runcode.sh C {}-{}-{} {}'.format(message['id'], port, timestamp, timeout)
                os.system(command)
                if os.path.exists('codes/{}-{}-{}-compileout.txt'.format(message['id'], port, timestamp)):
                    with open('codes/{}-{}-{}-compileout.txt'.format(message['id'], port, timestamp), 'r') as myfile:
                        out['testcase_compileout'] = myfile.read()
                    if os.path.isfile('codes/{}-{}-{}-compileout.txt'.format(message['id'], port, timestamp)):
                        os.remove('codes/{}-{}-{}-compileout.txt'.format(message['id'], port, timestamp))
                if os.path.exists('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp)):
                    with open('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp), 'r') as myfile:
                        out['testcase_compileerror'] = myfile.read()
                    if os.path.isfile('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp)):
                        os.remove('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp))
                if os.path.exists('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                    with open('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp), 'r') as myfile:
                        out['testcase_stdout'] = myfile.read()
                    if os.path.isfile('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                        os.remove('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp))
                if os.path.exists('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                    with open('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp), 'r') as myfile:
                        out['testcase_stderror'] = myfile.read()
                    if os.path.isfile('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                        os.remove('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp))
                if os.path.isfile('codes/{}-{}-{}.c'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}.c'.format(message['id'], port, timestamp))
                if os.path.isfile('codes/{}-{}-{}.out'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}.out'.format(message['id'], port, timestamp))
                if os.path.isfile('codes/timeout.txt'):
                    os.remove('codes/timeout.txt')
                    out['testcase_timeout'] = True

        if lang == 'CPP':
            print ("excecuting CPP code {}-{}-{}".format(message['id'],port, timestamp))
            with open('codes/{}-{}-{}.cpp'.format(message['id'],port, timestamp), 'w') as myfile:
                myfile.write(message['code'])
            print ("excecuting CPP code {}-{}-{} {}".format(message['id'], port, timestamp, timeout))
            command = './runcode.sh CPP {}-{}-{} {}'.format(message['id'], port, timestamp, timeout)
            os.system(command)
            if os.path.exists('codes/{}-{}-{}-compileout.txt'.format(message['id'],port, timestamp)):
                with open('codes/{}-{}-{}-compileout.txt'.format(message['id'],port, timestamp), 'r') as myfile:
                    out['compileout'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-compileout.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-compileout.txt'.format(message['id'], port, timestamp))
            if os.path.exists('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp)):
                with open('codes/{}-{}-{}-erroroutput.txt'.format(message['id'],port, timestamp), 'r') as myfile:
                    out['compileerror'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-erroroutput.txt'.format(message['id'], port, timestamp))
            if os.path.exists('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                with open('codes/{}-{}-{}-stdout.txt'.format(message['id'],port, timestamp), 'r') as myfile:
                    out['stdout'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp))
            if os.path.exists('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                with open('codes/{}-{}-{}-stderror.txt'.format(message['id'],port, timestamp), 'r') as myfile:
                    out['stderror'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp))
            if os.path.isfile('codes/{}-{}-{}.cpp'.format(message['id'],port, timestamp)):
                os.remove('codes/{}-{}-{}.cpp'.format(message['id'],port, timestamp))
            if os.path.isfile('codes/{}-{}-{}.out'.format(message['id'],port, timestamp)):
                os.remove('codes/{}-{}-{}.out'.format(message['id'],port, timestamp))
            if os.path.isfile('codes/timeout.txt'):
                os.remove('codes/timeout.txt')
                out['codetimeout'] = True

        elif lang == 'JAVA':
            print("executing java code")
            with open('codes/Main.java','w') as myfile:
                myfile.write(message['code'])
            
            command = './runcode.sh JAVA {}'.format(timeout)
            os.system(command)
            
            if os.path.exists('codes/Main-compileout.txt'):
                with open('codes/Main-compileout.txt', 'r') as myfile:
                    out['compileout'] = myfile.read()
                if os.path.isfile('codes/Main-compileout.txt'):
                    os.remove('codes/Main-compileout.txt')
            if os.path.exists('codes/Main-erroroutput.txt'):
                with open('codes/Main-erroroutput.txt', 'r') as myfile:
                    out['compileerror'] = myfile.read()
                if os.path.isfile('codes/Main-erroroutput.txt'):
                    os.remove('codes/Main-erroroutput.txt')
            if os.path.exists('codes/Main-stdout.txt'):
                with open('codes/Main-stdout.txt', 'r') as myfile:
                    out['stdout'] = myfile.read()
                if os.path.isfile('codes/Main-stdout.txt'):
                    os.remove('codes/Main-stdout.txt')
            if os.path.exists('codes/Main-stderror.txt'):
                with open('codes/Main-stderror.txt', 'r') as myfile:
                    out['stderror'] = myfile.read()
                if os.path.isfile('codes/Main-stderror.txt'):
                    os.remove('codes/Main-stderror.txt')
            if os.path.isfile('codes/Main.java'):
                os.remove('codes/Main.java')
            if os.path.isfile('codes/Main.out'):
                os.remove('codes/Main.out')
            if os.path.isfile('codes/timeout.txt'):
                os.remove('codes/timeout.txt')
                out['codetimeout'] = True
            
        elif lang == 'Python':
            print ("excecuting python code {}-{}-{}".format(message['id'],port, timestamp))
            with open('codes/{}-{}-{}.py'.format(message['id'],port, timestamp), 'w') as myfile:
                myfile.write(message['code'])
            command = './runcode.sh Python {}-{}-{} {}'.format(message['id'], port, timestamp, timeout)
            os.system(command)
            if os.path.exists('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                with open('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp), 'r') as myfile:
                    out['stdout'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp))
            if os.path.exists('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                with open('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp), 'r') as myfile:
                    out['stderror'] = myfile.read()
                if os.path.isfile('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp))
            if os.path.isfile('codes/{}-{}-{}.py'.format(message['id'],port, timestamp)):
                os.remove('codes/{}-{}-{}.py'.format(message['id'],port, timestamp))
            if os.path.isfile('codes/{}-{}-{}.pyc'.format(message['id'],port, timestamp)):
                os.remove('codes/{}-{}-{}.pyc'.format(message['id'],port, timestamp))
            if os.path.isfile('codes/timeout.txt'):
                os.remove('codes/timeout.txt')
                out['codetimeout'] = True

            if testcasepresent:
                with open('codes/{}-{}-{}.py'.format(message['id'], port, timestamp), 'w') as myfile:
                    myfile.write(message['testcase'])
                command = './runcode.sh Python {}-{}-{} {}'.format(message['id'], port, timestamp, timeout)
                os.system(command)
                if os.path.exists('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                    with open('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp), 'r') as myfile:
                        out['testcase_stdout'] = myfile.read()
                    if os.path.isfile('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp)):
                        os.remove('codes/{}-{}-{}-stdout.txt'.format(message['id'], port, timestamp))
                if os.path.exists('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                    with open('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp), 'r') as myfile:
                        out['testcase_stderror'] = myfile.read()
                    if os.path.isfile('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp)):
                        os.remove('codes/{}-{}-{}-stderror.txt'.format(message['id'], port, timestamp))
                if os.path.isfile('codes/{}-{}-{}.py'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}.py'.format(message['id'], port, timestamp))
                if os.path.isfile('codes/{}-{}-{}.pyc'.format(message['id'], port, timestamp)):
                    os.remove('codes/{}-{}-{}.pyc'.format(message['id'], port, timestamp))
                if os.path.isfile('codes/timeout.txt'):
                    os.remove('codes/timeout.txt')
                    out['testcase_timeout'] = True
        socket.send_json(out)
        shutil.rmtree('/usr/src/app/codes',ignore_errors=True)
    except Exception as e:
        print (e.__str__())
        out['status'] = 'Exception occured {}'.format(e.__str__())
        socket.send_json(out)
