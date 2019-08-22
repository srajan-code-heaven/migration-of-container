#!/usr/bin/python
import socket		#socket programming
import sys		#to access system specific parameters and functions
import select		#to call select() available in os
import time
import os		#for os dependent functionality
import shutil		#for directories or file operations 
import subprocess	#allows to spawn new processes
import distutils.util	#misclleneous utility functions

#base directory for containerson both source and destination
runc_base = "/runc/containers/"

#default values for optimization parameters
lazy = False
pre = False

#help
if len(sys.argv) < 3:
    print "Usage: " + sys.argv[0] + " [container id] [destination] [pre-copy] [post-copy]"
    sys.exit(1)

#arguments saving and conversion
container = sys.argv[1]
dest = sys.argv[2]
if len(sys.argv) > 3:
    pre = distutils.util.strtobool(sys.argv[3])
if len(sys.argv) > 4:
    lazy = distutils.util.strtobool(sys.argv[4])


#preparing directories path for container checkpoint images
base_path = runc_base + container
image_path = base_path + "/image"
parent_path = base_path + "/parent"

#q -quiet mode, a-archive mode, z-to compress while transfer 
rsync_opts = "-aqz"

def error():
    print "Something did not work. Exiting!"
    sys.exit(1)

#prepare removes already existing image_path or parent_path
def prepare():
    try:
        shutil.rmtree(image_path)
    except:
        pass
    try:
        shutil.rmtree(parent_path)
    except:
        pass

#modules or components required 
import predump
import realdump
import xferpredump
import xferrealdump
import giveip
prepare()
if pre:
    predump.pre_dump(base_path,container)
    xferpredump.xfer_pre_dump(rsync_opts,parent_path, dest, base_path)
realdump.real_dump(pre, lazy,base_path,container)
#giveip.give_ip(dest)
xferrealdump.xfer_final(rsync_opts, image_path, dest, base_path)

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect((dest, 8888))

input = [cs,sys.stdin]


cs.send('{ "restore" : { "path" : "' + base_path + '", "name" : "' + container + '" , "image_path" : "' + image_path + '" , "lazy" : "' + str(lazy) + '" } }')

while True:
    inputready, outputready, exceptready = select.select(input,[],[], 5)

    if not inputready:
        break

    for s in inputready:
         answer = s.recv(1024)
         print answer


