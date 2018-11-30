New Matter MOD-t 3d Printer Repo
================================

This repository is a collection of files (firmware, test files, configurations, etc) for the NewMatter MOD-t 3d Printer.

**WARNING:** I take absolutely no responsibility for anything you do with these files or instructions, play at your own risk!

MOD-t's Anonymous
---------------
As of February 28, 2018, New Matter has closed its doors and will no longer be providing WiFi connectivity to the MOD-t through the New Matter Store (will be open until Summer 2018).  A few of us that still enjoy our MOD-t have created a Slack group, please feel free to join us if you need help or want to discuss the future of the MOD-t

Unfortunately New Matter has decided to not release any of the source code for the MOD-t, as well as any software, [stating that there's licensed code they can't release](https://www.reddit.com/r/newmatter/comments/7xly0q/request_for_unewmatter_open_source_modt_firmware/), so instead of providing anything they could without licensed code, they provided nothing ... so time to start reverse engineering, **accepting all applications :)**

[Join the MOD-t Users Slack Channel](https://join.slack.com/t/modt-users/shared_invite/enQtMzM4NzI5Mzg2NDY0LTYxZjUyZTNmNGFjNGZmZmVlOWY5NjNhM2E1MTlhYWY0MTc1YTgyYmMwZGRjNTVmMTI0MGUwNzliYTBmYjVjYmU)

[View NewMatter Subreddit](https://www.reddit.com/r/newmatter/)

[New Matter Closing Blog Post](https://newmatter.com/blog/permanent-closure/)
[Archive.org Cached Version](https://web.archive.org/web/20180301202219/https://newmatter.com/blog/permanent-closure/)

FINAL SOFTWARE WARNINGS
-----------------------
Under the software section you will find a `.dmg` for OSX and `.exe` for Windows that is the last and final software version released by New Matter. **BEWARE** if you install this version and upgrade the firmware through the software, this **WILL COMPLETELY DISABLE WIFI ON YOUR MOD-T**

How to print without New New Matter Store
-----------------------------------------
To convert your 3D files into G-code, we recommend two options: Cura, a free software-based slicer, and Astroprint.com, a web-based slicer.

We have prepared a [post on our blog that outlines the entire process for creating G-code with Cura and sending it to your MOD-t through our desktop software application (Web Archive Version)](https://web.archive.org/web/20180301201538/https://newmatter.com/blog/how-to-use-cura-with-the-mod-t/).

[http://www.robosupportsnewmatter.com/blog/how-to-use-cura-with-the-mod-t](http://www.robosupportsnewmatter.com/blog/how-to-use-cura-with-the-mod-t)

Users who prefer not to download and install Cura can continue to “slice” their 3D designs into G-code through a website called Astroprint. This option has the benefit of being web-based, meaning there is no software to download, install, or configure. For a more detailed look at the process for converting your 3D files into G-code using Astroprint, [please see this video](https://www.youtube.com/watch?v=UL1-fpE6NUI).

MOD-t Details
-------------

```
Bed Shape: Rectangular
X Axis: 155.4 mm
Y Axis: 104.6 mm
Z Axis: 130 mm

Nozzle Diameter: 0.4mm
Number of Extruders: 1
Heated Bed: FALSE
```

---

Files
-----

### [`Astroprint.md`](https://github.com/tripflex/MOD-t/tree/master/Astroprint.md)

Information on setting up/configuring Astroprint (with GCode) https://www.astroprint.com/

### [`Basic_GCode.md`](https://github.com/tripflex/MOD-t/tree/master/Basic_GCode.md)

Basic GCode information for setting up the printer (including START and END commands)

### [`clearnozzle.gcode`](https://github.com/tripflex/MOD-t/tree/master/clearnozzle.gcode)

The file `clearnozzle.gcode` is intended to help clear a jammed nozzle on the MOD-t. Just connect your MOD-t to your computer with the USB, launch the MOD-t print tool app and select `Settings > Advanced Mode > Print File`

The MOD-t will do it's little calibration dance and then the nozzle will start to heat to 230ºC (actually it will try, but because the MOD-t is firmware limited to a max temp of 220ºC, it will never get there) and then the print head will move up. The move is just there to indicate that it's gotten to temp. The extruder will then try to push filament through, which should be enough to clear most jams. Finally the print head will move back down and the MOD-t will go back to idle.

---

Directories
-----------

### [Firmware](https://github.com/tripflex/MOD-t/tree/master/firmware)

This directory contains any firmware files I have been able to find, if you have any that are not in the repo, please open an issue or get in contact me with so I can add them.

Go to the directory and see the [Firmware README.md](https://github.com/tripflex/MOD-t/tree/master/firmware) for documentation

### [Slic3r](https://github.com/tripflex/MOD-t/tree/master/Slic3r)

This directory contains configuration files for Slic3r: http://slic3r.org

Launch Slic3r and select `File > Load Config` and select the file

I recommend going in to Preferences in Slic3r and choosing Expert Mode.

### [Cura](https://github.com/tripflex/MOD-t/tree/master/Cura)

Information/Configuration files for Cura https://ultimaker.com/en/products/cura-software

### [Calibration Tests](https://github.com/tripflex/MOD-t/tree/master/Calibration%20Tests)

Settings for the `Extrusion multiplier` in the `Filament Settings` tab of Slic3r, example image, and code to print a single wall.

Go to the directory and see the `README.md` for documentation

### [Scripts](https://github.com/tripflex/MOD-t/tree/master/scripts)

Scripts copied from [Xaero252 Mod-T-Scripts Repo](https://github.com/Xaero252/Mod-T-Scripts) with the exception of `optimize_gcode.py`

`optimize_gcode.py` - is supposed to be the "optimize" from New Matter in the latest version of the software, [quote from reddit](https://www.reddit.com/r/newmatter/comments/7xly0q/request_for_unewmatter_open_source_modt_firmware/):
> Pretty easy to figure out how it works and leads to ~50% smaller gcode files that print much, much faster with much higher print quality.

Go to the directory and see the `README.md` for documentation

---


MOD-t Teardown
-------------
[https://3dprinterwiki.info/newmatter-mod-t/](https://3dprinterwiki.info/newmatter-mod-t/)

[Teardown Pictures](https://flic.kr/s/aHsknFFE6Z)

Resources
---------

-	[MOD-t Reddit](http://www.reddit.com/r/newmatter)
-	[Google MOD-t Group](https://groups.google.com/forum/?#!forum/mod-t)
-	[NewMatter Website](http://www.newmatter.com)
-	[NewMatter MOD-t Support](http://support.newmatter.com)

---

How to contribute
-----------------

If you have a copy of firmware files, update suggestions to configurations, or anything else related to the MOD-t ... please feel free to open a new issue and let me know. I'll be more than happy to update or add anything to this repo.

---

### Credits

The majority of the information and files were obtained from `ajfoul`, make sure to check his repository for any other files or updates he may have added: https://github.com/ajfoul/MOD-t
