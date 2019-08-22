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

# rsync share that real-dump image directory to destination
def xfer_final(rsync_opts, image_path, dest, base_path):
    sys.stdout.write('DUMP size: ')
    sys.stdout.flush()
    cmd = 'du -hs %s' % image_path
    ret = os.system(cmd)
    cmd = 'rsync %s %s %s:%s/' % (rsync_opts, image_path, dest, base_path)
    print "Transferring DUMP to %s" % dest
    start = time.time()
    ret = os.system(cmd)
    end = time.time()
    print "DUMP transfer time %s seconds" % (end - start)
    if ret != 0:
        error()
