#!/usr/bin/python

###################################
# RTCS - Made by Valery Boltavsky #
###################################

import Analyzer
import getpass
import time
import MongoDB
import sys
import os
import Stats




###################################################
# start of process execution - check performance #
##################################################
start_time = time.time()


def main():

    ######################################################################
    # Dictionary -  converting month format from number to appropriate   #
    # short name for the file format in order to search                  #
    ######################################################################
    monthDic = {1:'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}


    print "userID is =", getpass.getuser()
    args = len(sys.argv) # Arguments count
    ##################################
    # If Statistics report required  #
    ##################################
    if args == 1:

        print "#" * 50
        print "##### Statistics has been created on your desktop ##########\n"
        print "#" * 50
        ##################################
        # Make png. files for Statistics #
        ##################################
        Stats.Stats().pie_chart()
        Stats.Stats().grid_chart()

    ##################################
    # If Analysis report required  #
    ##################################
    elif args == 6:

        #####################################################
        # User input from Web -- Format: DD M YYYY hh:mm:ss #
        #####################################################
        raceNo = sys.argv[1]
        weekday = "\w{3}"  # add weekday argument as match for every word - for later use
        tmpMonth = int(sys.argv[3])
        month = monthDic[tmpMonth]
        day = sys.argv[2]
        tmpTime = sys.argv[5]
        tm = tmpTime[:6] + "\d{2}"  # Ignore seconds - cut from input hours and minutes only!
        year = sys.argv[4]

        eventTimeStamp = weekday + " " + month + " " + day + " " + tm + " " + year
        print "analyzing.............."
        rtcScanner = Analyzer.Analyzer(raceNo, eventTimeStamp)
        raceApar = rtcScanner.analyze_issue()

        if raceApar.found:
            analysis_time = (time.time() - start_time)
            print "---- Analysis took: %s seconds ----" % analysis_time
            print "\nAPAR is:"
            raceApar.print_race_object()
        else:
            print "---- Sorry the issue is not recognised ----"

        #######################################################
        # Check if already this RACE issue have been scanned  #
        #  If not --> add to STATISTICS DB                    #
        #######################################################
        id = raceApar.aparId
        check = MongoDB.MongoDB().check_exist(raceNo)

        if check == False:
            MongoDB.MongoDB().insert_statistics( id, analysis_time, raceNo)
        else: print "This issue already analyzed by RTCS!"
    ######################################
    # Wrong amount of arguments provided #
    ######################################
    else:
        print "\n======WRONG INPUT!!!!!!!!!!!!======"
        print "args len = ", len(sys.argv)


if __name__ == "__main__":
    main()
