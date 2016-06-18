#! /usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################
""" 
This class build the race object
"""
class RaceObj():

    def __init__(self):

        self.aparId = ''  # APAR ID
        self.compAsserts = []  # Compression asserts which found
        self.noOfCompAsserts = 0  # How many exist
        self.severity = []  # What severity? MAIN/ MAY HAVE
        self.mainAssertCounter = 0 # Must asserts for identification
        self.aparURL = ''  # Debug page URL
        self.found = False  # Bollean if issue found
        self.version = ''  # which version of RACE accured

        return
    #######################################
    # Function which prints founded APAR  #
    # details for the user                #
    #######################################
    def print_race_object(self):
        print "#" * 100
        #TODO: Vers not working
        print "Issue found in version = ", self.version
        print ("APAR ID=" + str(self.aparId) + "\n" + "URL:" + self.aparURL + "\n" + str(self.found))
        for y, z in zip(self.compAsserts,self.severity):
            print "assert=" + str(y) + "sev=" + str(z)
        print "#" * 100 + "\n"

        return
