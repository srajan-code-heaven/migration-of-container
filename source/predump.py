#!/usr/bin/python
import socket
import sys
import select
import time
import os
import shutil
import subprocess
import distutils.util

def error():
    print "Something did not work. Exiting!"
    sys.exit(1)

#pre dumps images into directory parent 
def pre_dump(base_path,container):
    old_cwd = os.getcwd()
    os.chdir(base_path)
    cmd = 'runc checkpoint  --pre-dump --image-path parent'
    cmd += ' ' + container
    start = time.time()
    ret = os.system(cmd)
    end = time.time()
    print "%s finished after %d second(s) with %d" % (cmd, end - start, ret)
    os.chdir(old_cwd)
    if ret != 0:
        error()
