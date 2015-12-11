Firmware Upgrade/Downgrade Instructions
---------------------------------------

**WARNING:** I take absolutely no responsibility for anything you do with these files or instructions, play at your own risk!

#### Windows

1.	Download firmware file
2.	Copy firmware_modt_override.dfu from the downloaded destination into `C:\firmware_modt_override.dfu`
3.	Run the printer utility and upgrade the FW when prompted.
4.	After FW upload is done look at your About your MOD-t section under the settings section in the printer to check the FW version is X.X.X
5.	Remove/Delete the file under `C:\firmware_modt_override.dfu`

#### MAC OSX (and probably Linux)

1.	Download firmware file
2.	Copy `firmware_modt_override.dfu` from the downloaded destination into `/tmp/firmware_modt_override.dfu`
3.	Run the printer utility and upgrade the FW when prompted.
4.	After FW upload is done look at your About your MOD-t section under the settings section in the printer to check the FW version is X.X.X
5.	Remove/Delete the file under `/tmp/firmware_modt_override.dfu`

**Please follow step 5 or the printer will printer utility will never alert you about updated firmware in the future. Have an amazing Thanksgiving and hopefully this brings you good printing fortune!**

**Note:** You can also use [dfu-util](http://dfu-util.sourceforge.net) directly from the command line to swap firmware. `dfu-util` is installed by the MOD-t print tool and is what does the actual flashing in automated process above.

On a Mac it's within the app's package:`/Applications/MOD-t\ printer\ tool.app/Contents/MacOS/dfu-util`

On Windows it's located at:`C:\Program Files (x86)\MOD-t\RMbin`
