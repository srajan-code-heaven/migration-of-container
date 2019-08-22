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

# rsync share that pre-dump parent directory to destination
def xfer_pre_dump(rsync_opts,parent_path, dest, base_path):
    sys.stdout.write('PRE-DUMP size: ')
    sys.stdout.flush()
    cmd = 'du -hs %s' % parent_path		#shows predump size in human redable format
    ret = os.system(cmd)
    cmd = 'rsync %s %s %s:%s/' % (rsync_opts, parent_path, dest, base_path)
    print "Transferring PRE-DUMP to %s" % dest
    start = time.time()
    ret = os.system(cmd)
    end = time.time()
    print "PRE-DUMP transfer time %s seconds" % (end - start)
    if ret != 0:
        error()
