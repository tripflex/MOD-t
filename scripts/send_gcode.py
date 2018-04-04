#!/usr/bin/env python

# USAGE: send_gcode.py file.gcode
# Requires read/write permission to the Mod-T via USB.

import sys
import os
import usb.core
import usb.util
import time
from zlib import adler32

# Adler32 checksum function 
# Based on https://gist.github.com/kofemann/2303046
# For some reason, mod-t uses 0, not 1 as the basis of the adler32 sum
BLOCKSIZE=256*1024*1024

def adler32_checksum(fname):
 asum = 0 
 f = open(fname, "rb")
 while True:
   data = f.read(BLOCKSIZE)
   if not data:
        break
   asum = adler32(data, asum)
   if asum < 0:
        asum += 2**32
 f.close()
 return asum

# Read pending data from MOD-t (bulk reads of 64 bytes)
def read_modt(ep):
 text=''.join(map(chr, dev.read(ep, 64)))
 fulltext = text
 while len(text)==64:
        text=''.join(map(chr, dev.read(ep, 64)))
        fulltext = fulltext + text
 return fulltext

# Main program
if __name__ == '__main__':

    if not len(sys.argv)==2:
        print("Usage: send_gcode.py filename.gcode")
        quit()

# Read filename argument and check that the file exists
fname=str(sys.argv[1])
if not os.path.isfile(fname):	
	print(fname + " not found")
	quit()

# Get the size of the gcode file
size = os.path.getsize(fname)

# Get the adler32 checksum of the gcode file
checksum=adler32_checksum(fname)

# Open gcode file and read into buffer
f = open(fname, "rb")
gcode = f.read()
f.close()

# Find MOD-t usb device
dev = usb.core.find(idVendor=0x2b75, idProduct=0x0002)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

# These came from usb dump. 
# Some commands are human readable some are maybe checksums 
dev.write(2, bytearray.fromhex('246a0095ff'))
dev.write(2, '{"transport":{"attrs":["request","twoway"],"id":3},"data":{"command":{"idx":0,"name":"bio_get_version"}}};')
print(read_modt(0x81))

dev.write(4, '{"metadata":{"version":1,"type":"status"}}')
print(read_modt(0x83))

dev.write(2, bytearray.fromhex('248b0074ff'))
dev.write(2, '{"transport":{"attrs":["request","twoway"],"id":5},"data":{"command":{"idx":22,"name":"wifi_client_get_status","args":{"interface_t":0}}}};')
print(read_modt(0x81))

dev.write(2, bytearray.fromhex('246a0095ff'))
dev.write(2, '{"transport":{"attrs":["request","twoway"],"id":7},"data":{"command":{"idx":0,"name":"bio_get_version"}}};')
print(read_modt(0x81))

dev.write(4, '{"metadata":{"version":1,"type":"status"}}')
print(read_modt(0x83))

dev.write(4, '{"metadata":{"version":1,"type":"status"}}')
print(read_modt(0x83))

# Start writing actual gcode
# File size and adler32 checksum calculated earlier
dev.write(4, '{"metadata":{"version":1,"type":"file_push"},"file_push":{"size":'+str(size)+',"adler32":'+str(checksum)+',"job_id":""}}')

# Write gcode in batches of 20 bulk writes, each 5120 bytes. 
# Read mod-t status between these 20 bulk writes

start=0
counter=0
while True:
 if (start+5120-1>size-1):
        end=size
 else:
        end=start+5120
 block = gcode[start:end]
 print(str(counter)+':' +str(start)+'-'+str(end-1)+'\t'+str(len(block)))
 counter += 1
 if counter>=20:
  temp=read_modt(0x83)
  counter = 0
 dev.write(4, block)
 if (start == 0):
  temp=read_modt(0x83)
 start = start + 5120
 if (start>size):
        break;

# Gcode sent. Finally, loop and query mod-t status every 5 seconds 
while True:
 dev.write(4, '{"metadata":{"version":1,"type":"status"}}')
 print(read_modt(0x83))
 time.sleep(5)