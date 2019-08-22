#!/usr/bin/python
import socket
import sys
import select
import time
import os
import shutil
import subprocess
import distutils.util

def touch(fname):
    open(fname, 'a').close()

#gives floating ip to server so that access our server from connected hosts in network
def give_ip(dest):
    print "Giving floating IP to " + dest
    touch('/tmp/give_up_master_99')
    cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cs.connect((dest, 8888))
    cs.send('{ "take_ip" : "/tmp/give_up_master_99" }')
    os.system('systemctl stop keepalived')
    cs.close()
