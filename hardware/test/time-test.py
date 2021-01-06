#!/usr/bin/python
# coding: utf8

import signal, sys

# install a SIGALRM handler 

def handler(signum, frame):
    print "got signal, exiting"
    sys.exit(1)

signal.signal(signal.SIGALRM, handler)

# emit SIGALRM after 5 secs

signal.setitimer(signal.ITIMER_REAL, 5)

# do stuff

i = 1
while True:
    if i % 100000 == 0:
        print i
    i += 1