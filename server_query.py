#!/usr/bin/env python3
# ------------------------------------------------------------------------
# Server Query
# Use Valve protocol to query server
# ------------------------------------------------------------------------

# Generic/Built-in modules
import time                                                     # Time Module
import os                                                       # OS Module
import sys                                                      # Sys Module

# Other modules
import a2s                                                      # Valve protocol module

# Function to clear terminal
def clearTerminal():
    os.system('cls' if os.name=='nt' else 'clear')

# Function to wait on key press and then exit
def waitOnKey():
    try:
        print("Press CTRL-C to stop.")
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        clearTerminal()
        quit()

# Function to process local time
def processLocalTime():
    hour, minute, second = time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec
    hourFirst, hourSecond, minuteFirst, minuteSecond, secondFirst, secondSecond = (int(hour/10)), (int(hour%10)), (int(minute/10)), (int(minute%10)), (int(second/10)), (int(second%10))
    return hour, minute, second, hourFirst, hourSecond, minuteFirst, minuteSecond, secondFirst, secondSecond, second

# Function to query DayZ server
def dayZQuery(serverAddress):
    try:
        serverInfo = a2s.info(serverAddress)
        serverPlayers = serverInfo.player_count
        serverPing = serverInfo.ping
        demarcLine = ""
        for x in range (len(serverInfo.server_name) -1):
            demarcLine += "="

        print (serverInfo.server_name)
        print (demarcLine)
        print ("Game    :",serverInfo.game)
        print ("Map     :",serverInfo.map_name)
        print ("Players :",serverInfo.player_count)
          print (demarcLine)
    except:
        print ("Something went wrong connecting to the server")
        print (sys.exc_info()[0])

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Main
def main():
    clearTerminal()
    print ("Querying server every 60 seconds...")

    # Configuration for DayZ server query
    serverAddress = ("217.182.197.233", 2669)

    # Do the intial time capture
    hour, minute, second, hourFirst, hourSecond, minuteFirst, minuteSecond, secondFirst, secondSecond, second = processLocalTime()
    currentMinute = minute



    while 1:
        hour, minute, second, hourFirst, hourSecond, minuteFirst, minuteSecond, secondFirst, secondSecond, second = processLocalTime()

        # trigger the querey every minute update
        if minute != currentMinute:
            currentMinute = minute
            dayZQuery(serverAddress)
        time.sleep(1)

if __name__ == "__main__":
    main()



