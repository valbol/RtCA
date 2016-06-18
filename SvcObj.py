#! /usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################

"""
This class represent SVC object
"""
class SvcObj():

    def __init__(self):

        self.errorDate = 0  # Date of the issue accured
        self.errorCode = 0  # SVC error code -> 2030/1862/1196 etc.
        self.relevant = False  # Is the error code is in relevant dates range

        return
