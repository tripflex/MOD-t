#!/bin/python
import sys
import os
import usb.core
import usb.util
import time
#This script just finds a mod-t and puts it in DFU mode.


dev = usb.core.find(idVendor=0x2b75, idProduct=0x0002)

#If we didn't find a Mod-T we need to throw an error
if dev is None:
	raise ValueError('No Mod-T detected')

#Set active configuration (first is default)
dev.set_configuration()

#First we mimmick the Mod-T desktop utility
#The initial packet is not human readable
#The second packet puts the Mod-T into DFU mode
dev.write(2, bytearray.fromhex('246a0095ff'))
dev.write(2, '{"transport":{"attrs":["request","twoway"],"id":7},"data":{"command":{"idx":53,"name":"Enter_dfu_mode"}}};')

#Wait for the Mod-T to reattach in DFU mode
time.sleep(2)

