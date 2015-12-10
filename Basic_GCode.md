Basic GCode
===========

Here are the basic GCode start and end commands for the MOD-t ... check the other configuration files for more information.

### START commands:

```
M42 P10 S1 ; Turn on LED
G21 ; set units to millimeters
G90 ; use absolute coordinates
M82 ; use absolute distances for extrusion
M204 S500

G0 Z1 F300 ; Make sure main Z drop isn’t too fast

;Move to side and put down a line to prime the nozzle
G1 X64.332 Y24.938 F9000
G1 Z0.315 F300
G92 E0
G1 X74.332 Y-44.938 E3.9642 F2520
G1 X74.964 Y-44.938 E4.0001
G1 X74.964 Y24.938 E7.9643
G1 X74.532 Y24.938 E7.9888
G1 X74.332 Y24.938 F2520
G1 X73.876 Y25.394 F9000
G92 E0
G1 X73.876 Y-45.394 E4.0159 F1680
G1 X75.42 Y-45.394 E4.1035
G1 X75.42 Y25.394 E8.1195
G1 X74.076 Y25.394 E8.1957
G1 X73.876 Y25.394 F1680
G1 X73.876 Y23.394 F1680

G0 Z1 F300
G0 X0 Y0 F5000

G92 X77.7 Y52.3 ; Offset Origin from center to top right corner to accommodate Astroprint requirement
G92 E0
```

### END commands:

```
G92 E0
G0 Z130 F300; Go high

G0 X77.7 Y52.3 F3000
G92 X0 Y0 ; Change Offset back to center

G0 X0 Y50 F3000; Go front and center
M104 S0 ; Turn off temperature
M107 ; Turn on fan
M84 ; Disable motors
```

Original Source: http://support.newmatter.com/customer/portal/questions/14427572-how-do-change-print-settings-like-infill-support-etc-
