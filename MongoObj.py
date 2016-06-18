#! /usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################

class MongoObj():

    def __init__(self):


        self.aparId = ''  # Serial of an issue
        self.compAsserts = []  # Store all the asserts related
        self.noOfCompAsserts = 0  # amount of asserts
        self.severity = []  # MAIN/MAYHAVE
        self.mainAssertCounter = 0  # How many must be
        self.aparURL = ''  # debug page URL
        self.analysis_time = 0.0  # How much time took in order to analyse this issue
    pass

