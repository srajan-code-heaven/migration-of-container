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

#real dump freezes all in memory states and dump it into a directory image 
def real_dump(precopy, postcopy,base_path,container):
    old_cwd = os.getcwd()
    os.chdir(base_path)
    cmd = 'runc checkpoint --image-path image --leave-running'
    cmd = 'runc checkpoint --image-path image '
    if precopy:
        cmd += ' --parent-path ../parent'
    if postcopy:
        cmd += ' --lazy-pages'
        cmd += ' --page-server localhost:27'
	try:
	    os.unlink('/tmp/postcopy-pipe')
        except:
            pass
        os.mkfifo('/tmp/postcopy-pipe')
	cmd += ' --status-fd /tmp/postcopy-pipe'
    cmd += ' ' + container
    start = time.time()
    print cmd
    p = subprocess.Popen(cmd, shell=True)
    if postcopy:
        p_pipe = os.open('/tmp/postcopy-pipe', os.O_RDONLY)
	ret = os.read(p_pipe, 1)
        if ret == '\0':
            print 'Ready for lazy page transfer'
	ret = 0
    else:
        ret = p.wait()

    end = time.time()
    print "%s finished after %.2f second(s) with %d" % (cmd, end - start, ret)
    os.chdir(old_cwd)
    if ret != 0:
        error()
