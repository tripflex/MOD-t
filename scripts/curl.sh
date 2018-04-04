#!/bin/bash
#This script just downloads the firmware from the new matter store
#This script is adapted for a websocket fronted and processes
#$_POST data expected ?url=<actual firmware url here>
#Evaluating that query string results in setting the variable "url" to the actual intended download url
#kind of hacky but really the only way to interface with websockets. Needs sanitization etc.
#echo for debugging, eval to actually put the variable in
echo $QUERY_STRING

eval $QUERY_STRING

#Another echo for debugging, let's make sure we have a url variable now
echo $url

#start downloading, log the download progress, and fork into the background
curl -# --limit-rate 5K --output /dev/null $url > /tmp/curl.log 2>&1 &

#capture the PID for the while loop
pid=$!

#Loop while curl is still alive
while kill -0 $pid 2>/dev/null; do
    #We just need the progress percentage
    progress=`grep -ao '[^ ]*%' /tmp/curl.log | tail -1`
    #Send that over to the webpage
    echo $progress
    #Doesn't need to update very often
    sleep 0.1
done

#We won't always capture the 100% mark, so we force it if we make it this far.
#Suggested fix: check if $pid curl exits gracefully. use try...catch statement to handle HTTP response codes
echo "100%"

/*
 *TODO: The above is ugly, and breaks easily
 *Need to implement error handling, etc, what if the server is down?
 *No internet? What if the data passed to the url variable is malformed?
 */
