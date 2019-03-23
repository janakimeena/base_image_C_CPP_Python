#!/bin/bash

#./runcode.sh CPP main.c

#SCRIPTDIR="`dirname $0`/"

SCRIPTDIR="codes/"
TIMEOUTFILE=timeout.txt
TYPE=$1
INPUTFILENAME=$2
TIMEOUT=$3
ERRORSTATUS=0
# 100 kB filesize limit 
ulimit -f 500

if [ "$TYPE" == "C" ]; then
#    echo "gcc $SCRIPTDIR$INPUTFILENAME.c -o $SCRIPTDIR$INPUTFILENAME.out  1>$SCRIPTDIR$INPUTFILENAME-compileout.txt 2>$SCRIPTDIR$INPUTFILENAME-erroroutput.txt"
    gcc -w -lm $SCRIPTDIR$INPUTFILENAME.c -o $SCRIPTDIR$INPUTFILENAME.out  1>$SCRIPTDIR$INPUTFILENAME-compileout.txt 2>$SCRIPTDIR$INPUTFILENAME-erroroutput.txt
    RESULT=$?
    echo $RESULT
    if [ $RESULT -eq 0 ]; then
        echo "No error - Excecuting code"
        timeout $TIMEOUT ./$SCRIPTDIR$INPUTFILENAME.out <"codes/input.txt"  1> $SCRIPTDIR$INPUTFILENAME-stdout.txt 2> $SCRIPTDIR$INPUTFILENAME-stderror.txt
#        echo "No error"
        if [ $? -eq 124 ]; then
            echo 'timeout' > $SCRIPTDIR$TIMEOUTFILE
        else
            echo 'Ran correctly'
        fi
    else
        echo "Error while compiling C Code"
    fi
elif [ "$TYPE" == "CPP" ]; then
    g++ -w -lm -std=c++14 $SCRIPTDIR$INPUTFILENAME.cpp -o $SCRIPTDIR$INPUTFILENAME.out  1>$SCRIPTDIR$INPUTFILENAME-compileout.txt 2>$SCRIPTDIR$INPUTFILENAME-erroroutput.txt
    RESULT=$?
    echo $RESULT
    if [ $RESULT -eq 0 ]; then
        echo "No error Excecuting code"
        timeout $TIMEOUT ./$SCRIPTDIR$INPUTFILENAME.out < "codes/input.txt" 1> $SCRIPTDIR$INPUTFILENAME-stdout.txt 2> $SCRIPTDIR$INPUTFILENAME-stderror.txt
#        echo "No error"
        if [ $? -eq 124 ]; then
            echo 'timeout' > $SCRIPTDIR$TIMEOUTFILE
        else
            echo 'Ran correctly'
        fi
    else
        echo "Error while compiling C++ Code"
    fi
elif [ "$TYPE" == "Python" ]; then
#    echo "firejail --quiet python $SCRIPTDIR$INPUTFILENAME.py 1> $SCRIPTDIR$INPUTFILENAME-stdout.txt 2> $SCRIPTDIR$INPUTFILENAME-stderror.txt"
    timeout $TIMEOUT python3 $SCRIPTDIR$INPUTFILENAME.py < "codes/input.txt" 1> $SCRIPTDIR$INPUTFILENAME-stdout.txt 2> $SCRIPTDIR$INPUTFILENAME-stderror.txt
    if [ $? -eq 124 ]; then
        echo 'timeout' > $SCRIPTDIR$TIMEOUTFILE
    else
        echo 'Ran correctly'
    fi
fi

exit $RESULT
