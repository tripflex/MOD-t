#!/bin/python
import sys
import os
import usb.core
import usb.util
import time
#This script *SHOULD* eventually be the all-encompassing firmware update
#It should call the check FW script, place the Mod-T into DFU mode and flash the firmware
#It should have a command-line arg to flash older firmware versions, none of this is really implemented yet
#Make sure this was called correctly
if not len(sys.argv)==2:
	print("Usage: fw_update.py filename.dfu")
	quit()

#Find the Mod-T - we should probably see if it's in DFU mode, too
#That way we can do emergency flashes from recovery mode
dev = usb.core.find(idVendor=0x2b75, idProduct=0x0002)

#If we didn't find a Mod-T we need to throw an error
if dev is None:
	raise ValueError('No Mod-T detected')

#Make sure the filename supplied is actually a file, and error out appropriately
fname=str(sys.argv[1])
if not os.path.isfile(fname):
	print(fname + " not found")
	quit()

#Set active configuration (first is default)
dev.set_configuration()

#First we mimmick the Mod-T desktop utility
#The initial packet is not human readable
#The second packet puts the Mod-T into DFU mode
dev.write(2, bytearray.fromhex('246a0095ff'))
dev.write(2, '{"transport":{"attrs":["request","twoway"],"id":7},"data":{"command":{"idx":53,"name":"Enter_dfu_mode"}}};')

#Wait for the Mod-T to reattach in DFU mode
time.sleep(2)

