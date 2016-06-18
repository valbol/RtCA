#! /usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################


'''
This class represent file object
'''
class FileObj():

    def __init__(self):

        self.fileName = ''  # file name and sort
        self.lineNoInFile = 0  # Store line number of timestamp
        self.lineExist = False  # Boolean to see if timestamp exist in file

        return


