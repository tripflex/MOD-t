## MOD-t Scripts
Original source from https://github.com/Xaero252/Mod-T-Scripts

##First and foremost:
**USE THESE SCRIPTS AT YOUR OWN RISK!**
These scripts aren't very well tested and almost none of them are completely finished. They work to interface with the printer but it's all very manual.

##Overview and license
This is a basic set of utility scripts to interface with the New Matter Mod-T 3d printer on Linux. You are free to fork and contribute as you see fit.
This work falls under the MIT license. See the LICENSE file for more information.
I must also credit /u/modtdev on reddit for the work on getting the gcode sent to the Mod-T

###Depdencies

1. curl
2. *dfu-util
3. *python3
4. *python3-pyusb


##Usage

First, I recommend creating a udev rule for the Mod-T similar to the following:
/etc/udev/rules.d/51-modt.rules:
    SUBSYSTEM=="usb", ATTR{idVendor}=="2b75", ATTR{idProduct}=="0002", GROUP="users", MODE="0674"
SUBSYSTEM=="usb", ATTR{idVendor}=="2b75", ATTR{idProduct}=="0003", GROUP="users", MODE=0674"

In the above I have everyone in the `users` group enabled, however you can restrict access as needed.
This allows a regular user to run the scripts and still have them operate as intended.


From there most scripts are pretty straightforward. Simply flag them executable and run them. The `send_gcode.py`, `flash_firmware.sh`, and `fw_update.py` are the only scripts requiring arguments, each of them expect a single argument containing the path to an appropriate file for the function requested.  

If you do choose to use these scripts to print things by sending gcode, monitor the output of the `send_gcode.py` script until you see `STATE_JOB_QUEUED` as the printer status. If you press the front panel button prior to seeing this state you will have a broken print job, which will not print correctly.
