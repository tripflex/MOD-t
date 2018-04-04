import copy
import math


infname = 'myfile.gcode'
outfname = 'myfile-150.gcode'

# ERROR THRESHOLD HERE!
ERRORTHRESH = 0.150 #millimeters - threshold for trajectory error
# ERROR THRESHOLD HERE!

def writeGcode(outFile, XYZ, E, F):
    # we're here because the sequence is ready to be "closed out" and written to the output file
    # this may have happened because of a change in feedrate, extruder behavior, a non-G1 code,
    # or that the error may have been too great. regardless, it's time to just write one line
    # of g-code to the output file
    global curXYZ
    global curE
    global lastF

    outline = 'G1'

    if lastF != F:
        outline = outline + ' F' + str(F)
    lastF = F
    if XYZ[0] != curXYZ[0]:
        outline = outline + ' X' + str(XYZ[0])
    if XYZ[1] != curXYZ[1]:
        outline = outline + ' Y' + str(XYZ[1])
    if XYZ[2] != curXYZ[2]:
        outline = outline + ' Z' + str(XYZ[2])
    if E != curE:
        outline = outline + ' E' + str(E)

    outline = outline + '\n'

    outFile.write(outline)

    curXYZ = copy.deepcopy(XYZ)
    curE = copy.deepcopy(E)

def cross(a, b):
    c = [a[1]*b[2] - a[2]*b[1],
         a[2]*b[0] - a[0]*b[2],
         a[0]*b[1] - a[1]*b[0]]

    return c

def mag(a):
    m = a[0]*a[0] + a[1]*a[1] + a[2]*a[2]
    m = math.sqrt(m)

    return m


def initSequence(flags, args, curXYZ, curE):
    global newSequence
    global sequenceXYZ
    global sequenceE
    global sequenceFeedrate
    global sequenceExtruding
    global nextXYZ
    global nextE

    # initialize a new sequence
    # define sequence feedrate, if it is set
    if flags[1]:
        sequenceFeedrate = args[1]

    # add this G-code's target to the position sequence
    nextXYZ = copy.deepcopy(curXYZ)
    nextE = copy.deepcopy(curE)

    if flags[2]:
        nextXYZ[0] = args[2]
    if flags[3]:
        nextXYZ[1] = args[3]
    if flags[4]:
        nextXYZ[2] = args[4]
    if flags[5]:
        nextE = args[5]

    sequenceXYZ = [copy.copy(nextXYZ)]
    sequenceE = [copy.copy(nextE)]
    #sequenceXYZ = []
    #sequenceE = []

    # check if this sequence is moving the extruder forward, backward, or not
    if nextE > curE:
        sequenceExtruding = 1
    elif nextE < curE:
        sequenceExtruding = -1
    else:
        sequenceExtruding = 0

    # set the new sequence flag to false now, since we just primed a new sequence
    newSequence = False

##############################################################

global newSequence
global sequenceXYZ
global sequenceE
global sequenceFeedrate
global sequenceExtruding
global nextXYZ
global nextE
global curXYZ
global curE
global lastF


outFile = open(outfname,'w')

indices = {'G': 0, 'F': 1, 'X': 2, 'Y': 3, 'Z': 4, 'E': 5}
curXYZ = [0,0,0]
curE = 0
newSequence = True
lastF = -1

with open(infname) as readfileobject:
    for thisLine in readfileobject:
        # ignore empty lines
        if thisLine == '\n':
            continue

        # if it's anything other than a G0 or G1 command, just echo it to the output file
        # but only after writing any g-codes from an unfinished sequence
        # also flag that a new movement sequence needs to be started
        if not((thisLine[0:3] == 'G0 ') | (thisLine[0:3] == 'G1 ')):
            if not(newSequence):
                writeGcode(outFile, sequenceXYZ[-1], sequenceE[-1], sequenceFeedrate)
            newSequence = True
            outFile.write(thisLine)

            # check for G92 line, and reset current axis positions accordingly.
            # Writing out the g-code first, if necessary
            if (thisLine[0:3] == 'G92'):
                codes = thisLine.rstrip().split(' ')
                flags = [False, False, False, False, False, False] # GFXYZE commanded flags
                args = [0,0,0,0,0,0] # GFXYZE arguments
                for code in codes:
                    key = code[0]
                    idx = indices.get(key, 'default')
                    if idx == 2:
                        curXYZ[0] = float(code[1:])
                    elif idx == 3:
                        curXYZ[1] == float(code[1:])
                    elif idx == 4:
                        curXYZ[2] == float(code[1:])
                    elif idx == 5:
                        curE = float(code[1:])
            continue

        # Okay, we're here for a G0 or G1. Parse it.
        # first remove trailing comments and leading and trailing whitespace,
        # and split into words
        codes = thisLine.split(';')[0].strip().split(' ')

        flags = [False, False, False, False, False, False] # GFXYZE commanded flags
        args = [0,0,0,0,0,0] # GFXYZE arguments
        for code in codes:
            key = code[0]
            idx = indices.get(key, 'default')
            flags[idx] = True
            args[idx] = float(code[1:])

        # check if it's the first move in a sequence
        if newSequence:
            # don't worry about checking anything, just continue with next g-code line
            # after prepping variables for next loop

            initSequence(flags, args, curXYZ, curE)

        else:
            # check feedrate versus previous move
            if flags[1]:
                if args[1] != sequenceFeedrate:
                    # the commanded feedrate is different than the sequence feedrate,
                    # so we need to write out the G-code and start a new sequence with this move
                    writeGcode(outFile, sequenceXYZ[-1], sequenceE[-1], sequenceFeedrate)
                    initSequence(flags, args, curXYZ, curE)
                    continue

            # check extruder activity versus previous move
            # note that I'm only checking consistency of direction of extruder motion (+/-/0)
            # theoretically, an inrease or decrease in speed will mess this up, but I don't
            # expect incoming G code to do that. Something to fix later perhaps.
            if flags[5]: # an E position is commanded
                deltaE = args[5] - sequenceE[-1]
                if deltaE > 0:
                    eDir = 1
                elif deltaE < 0:
                    eDir = -1
                else:
                    eDir = 0
            else:
                eDir = 0

            if eDir != sequenceExtruding:
                # the extruder is starting, stopping, or changing direction, so we need
                # to start a new sequence
                writeGcode(outFile, sequenceXYZ[-1], sequenceE[-1], sequenceFeedrate)
                initSequence(flags, args, curXYZ, curE)
                continue

            # we've made it this far, so the feedrate and extruder behavior haven't changed.
            # so now we check the geometry of the path in XYZ - how much error would be
            # introduced if we eliminate this segment and just link it to the previous?

            # calculate the orthogonal distances between all intermediate points and the
            # "shortcut" line. see http://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html

            nextXYZ = copy.deepcopy(sequenceXYZ[-1])

            if flags[2]:
                nextXYZ[0] = args[2]
            if flags[3]:
                nextXYZ[1] = args[3]
            if flags[4]:
                nextXYZ[2] = args[4]
            if flags[5]:
                nextE = args[5]

            x2 = copy.deepcopy(nextXYZ)
            x1 = copy.deepcopy(curXYZ)
            d = []
            if (x2[0]==x1[0]) and (x2[1]==x1[1]) and (x2[2]==x1[2]): #start and finish in same place
                for x0 in sequenceXYZ:
                    tmp = [x0[0]-x1[0], x0[1]-x1[1], x0[2]-x1[2]]
                    d.append(mag(tmp))
            else:
                for x0 in sequenceXYZ:
                    a = [x0[0]-x1[0], x0[1]-x1[1], x0[2]-x1[2]]
                    b = [x0[0]-x2[0], x0[1]-x2[1], x0[2]-x2[2]]
                    c = [x2[0]-x1[0], x2[1]-x1[1], x2[2]-x1[2]]

                    d.append(mag(cross(a,b)) / mag(c))

            errorLarge = False
            for thisD in d:
                if thisD > ERRORTHRESH:
                    errorLarge = True

            # check for z-axis position change. if so, make a new segment regardless of error
            zNotEqual = (nextXYZ[2] != curXYZ[2])

            if errorLarge or zNotEqual:
                # the error is too great, so we need to close out the previous sequence
                # and start a new one
                writeGcode(outFile, sequenceXYZ[-1], sequenceE[-1], sequenceFeedrate)
                initSequence(flags, args, curXYZ, curE)
                continue

            else:
                # the errors are all below the threshold, so continue the sequence
                sequenceXYZ.append(copy.deepcopy(nextXYZ))
                sequenceE.append(copy.deepcopy(nextE))
                continue

# we're at the end of the file, so write out the final open sequence (if there is one)
if not(newSequence):
    writeGcode(outFile, sequenceXYZ[-1], sequenceE[-1], sequenceFeedrate)


outFile.close()
