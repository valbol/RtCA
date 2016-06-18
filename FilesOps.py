#!/usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################

import os
import fnmatch
import re
from datetime import datetime
import FileObj
import SvcObj

'''REGEX'''
RACE_VERS_REGEX ='\w{7}\s[v]\d\.\d\.'
TIME_STAMP_REGEX = '[\b\w{3}\b\s\w{3}\s\d{2}\s\d{2}\:\d{2}\:\d{2}\s\d{4}]'
DIGIT_REGEX = '[\b\w{1,3}\b\s\w{1,3}\b\s\s[0-9]\b]' #\s\d\d\:\d\d\:\d\d\s\d\d\d\d'
SVC_START_LINE = 'svcinfo lseventlog'
SVC_END_LINE = 'svcinfo lssystem -delim'
SVC_ERRORS = '\s1862\s|\s2030\s'


FILES_DATE_PATTERN = "%a %b %d %H:%M:%S %Y"
MY_DATE_PATTERN = "%Y%m%d%H%M%S"


REDUCED_LINES = 500 #TODO: decide how many lines to reduce
EOF = "\0"
LOCAL_DIR_PATH = '/home/support/Desktop/RACE-'

LOG_FILE = '*.log'
COUNTERS_FILE = '*.counters'
SEQ_FILE = '*.seq.txt'
SVC_FILE = 'svcout.*'



tmpTIME = 'Wed May  4 20:12:\d 2016' #TODO: build regex!!!!!!!!!!!!!!!!!!

################################TODO: finish details
# This class handle all the file operations including extracting information
# works with regex in order to find relevant information
################################


class FilesOps():

    def __init__(self, race_num, timeGiven):




        self.localDirPath = LOCAL_DIR_PATH + str(race_num)
        self.fileNamesArr = []  # Array of all files in the directory
        self.fileAssertArr = []  # Array of all the Asserts and/or Errors
        self.sotrtedAssertArr = []  # Main array to work with

        self.timeGiven = timeGiven


        if len(self.timeGiven) == 29:
            self.timeOrgForamt = "Sun" + timeGiven[5:19] + "30" + timeGiven[24:]
            print  "\nEvent timestamp = ", self.timeOrgForamt
        elif len(self.timeGiven) == 28:
            self.timeOrgForamt = "Sun" + timeGiven[5:18] + "30" + timeGiven[23:]
            self.timeGiven = "Wed May  4 20:12:39 2016"
            print "\nEvent timestamp = ", self.timeOrgForamt



        #######################################
        # Convert given timestamp into number #
        #######################################
        tmpTimestamp = datetime.strptime(self.timeOrgForamt, FILES_DATE_PATTERN)
        self.timestamp = datetime.strftime(tmpTimestamp, MY_DATE_PATTERN)

        self.fileObjectsArr = []

        self.raceVers = 0.0
        self.raceVersFull = 0.0

        return

    ################################################
    # get function for latter use in MongoDB class #
    ################################################
    def getVers(self):

        return self.raceVers

    ##########################################################
    # Find in a file, the line number of the issue timestamp #
    ##########################################################
    def __seek_line_no(self, f):

        for num, l in enumerate(f, 0):

            if re.search(self.timeGiven, l):  # find bug DATE - entrance point to seek in file
                print "===>>> MATCH=",  self.timeGiven
                print l.strip()
                print "Timestamp found in line no. :", num
                return num
        print "NO MATCH=%s in this file" % self.timeGiven
        return -1  # In case the timestamp is wrong or not in the file

    ######################################################
    # In a given directory search for the relevant files #
    ######################################################
    def __find_files(self, pattern, path):

        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    self.fileNamesArr.append(os.path.join(root, name))
        return self.fileNamesArr


    ###############################################################
    # Function which collect the relevant lines                   #
    # DO the first filtering and sort the lines in order not to   #
    ###############################################################
    def __convert_timestamp(self, line):

        if re.match('Frame\s\d{2}', line):
            self.sotrtedAssertArr.append(line)
        elif re.match(TIME_STAMP_REGEX, line):
            tmpBegin = line[:24]
            if re.match('Frame 11: /data/race/lib', tmpBegin):
                return
            elif re.match(DIGIT_REGEX, tmpBegin):
                print "FOUND=", tmpBegin
                tmpBegin = tmpBegin[:8] + '0' + tmpBegin[9:]

            issueDate = datetime.strptime(tmpBegin, FILES_DATE_PATTERN)
            lineStart = datetime.strftime(issueDate, MY_DATE_PATTERN)
            lineEnd = line[24:]
            #TODO: timestamp -> need to be from seeking line start!!!!!!!!!!!!!!!!!!
            if int(self.timestamp)-100000000 < int(lineStart):
                self.sotrtedAssertArr.append(lineStart+lineEnd)

        return

    ###############################
    # Finds RACE current version  #
    ###############################
    def collect_race_version(self,fileName):

        with open(fileName, "rb+") as fileReader:
            for line in fileReader:
                if re.search(RACE_VERS_REGEX, line):
                    ## Convert RACE vers to flout
                    self.raceVers = float(line[45:48])
                    self.raceVersFull = line[45:]
                    fileReader.close()
                    break

        fileReader.close()

    def find_timestamp_in_file(self, filesArr):

        for i, fileName in enumerate(filesArr):
            fileObj = FileObj.FileObj()
            fileObj.fileName = fileName

            print "fileName===" + str(fileName) + " --i=" + str(i)
            try:
                with open(fileName, "rb+") as fileReader:
                    ## Find line no. in the file ##
                    lineNum = self.__seek_line_no(fileReader)
                    if lineNum == -1:
                        print "ERROR: Timestamp is incorrect or not exist in the file!!!", self.timeOrgForamt

                        fileReader.close()
                        next(iter(filesArr))
                    else:
                        fileObj.lineExist = True
                        fileObj.lineNoInFile = lineNum
                        print "Timestamp found !!"

                fileReader.close()
                print "1.file closed!"
                print "#" * 20
            except IOError as e:
                print "I/O error({0}): {1}".format(e.errno, e.strerror)
            except Exception as e:
                print "Other exception: " + e.message + str(e.__class__)
            self.fileObjectsArr.append(fileObj)
        return

    ##################################################################
    # Function which locates the relevant line for later examination #
    # know to handle with different structure of lines               #
    ##################################################################
    def collect_issues(self):

        filesArr = self.__find_files(LOG_FILE, self.localDirPath)
        ################################################################
        # Find timestamp in file if exist and build the fileObjectsArr #
        ###############################################################
        self.find_timestamp_in_file(filesArr)
        badDataArr = []  # Collect trash lines


        for i, fileObj in enumerate(self.fileObjectsArr):

            if fileObj.lineExist == True:
                print "FOUND=", fileObj.fileName
                #####################
                # Find race version #
                #####################
                self.collect_race_version(fileObj.fileName)

            with open(fileObj.fileName, "rb+") as fileReader:
                ##################################################################
                # START from seeking point...                                    #
                # find  bug DATE - entrance point to seek in file                #
                # Start seeking the file from XXX lines before issue time stamp  #
                ##################################################################
                for line in fileReader.readlines()[fileObj.lineNoInFile-REDUCED_LINES:]:
                    ##############################################################
                    # find --> return index no. if found, -1 otherwise           #
                    # If line contain Assert/Error add it to the asserts array   #
                    ##############################################################
                    if re.match(TIME_STAMP_REGEX, line):
                        if line.find("Assert") != -1 or line.find("Error") != -1 \
                                or line.find("ERROR") != -1 or line.find("Frame") != -1:
                            self.fileAssertArr.append(line)

                        elif line.startswith(EOF):
                            ###################################################################################
                            # In case there is an empty output to the file --> @@@@@@@@@@@@ == (Binary '\0')  #
                            ###################################################################################
                            break

            fileReader.close()

        ###########################################################
        # Convert date to NEW format and sort Files lines by date #
        ###########################################################
        for assertLine in self.fileAssertArr:
            self.__convert_timestamp(assertLine)
        self.sotrtedAssertArr.sort()



        print "#" * 40
        print "num of lines detected: ", self.fileAssertArr.__len__()
        print "num of lines After first scan: ", self.sotrtedAssertArr.__len__()
        print "#" * 40
        print "\n\n"

        return




    def find_SVC_errors(self):

        SVCFile = self.__find_files(SVC_FILE, self.localDirPath)
        tmpARR = []

        try:
            with open(SVCFile[0], "rb+") as fileReader:

        ## locate seeking point ##
                for i, line in enumerate(fileReader.readlines()):
                    if re.match(SVC_START_LINE, line):
                       # while not re.match(SVC_END_LINE, line):
                        startLineSVC = i+1


                    elif re.match(SVC_END_LINE, line):
                        endLineSVC = i-2

            fileReader.close()

        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except Exception as e:
            print "Other exception: " + e.message + str(e.__class__)
        try:
            with open(SVCFile[0], "rb+") as fileReader:
                print "SVC Errors --------Issue Timestamp---------------------Event Error code"
                counter = 0
                for i, line in enumerate(fileReader.readlines()[startLineSVC:endLineSVC]):
                    if re.search(SVC_ERRORS, line):
                        tmpLine = line[16:136].rstrip()
                        tmpARR.append(tmpLine)# Collect only the error No.
                        print "SVCERROR[" + str(counter + 1) + "] =" + str(tmpARR[counter])
                        counter += 1
            fileReader.close()

            print "#" * 80
        except IOError as e:
            print "I/O error({0}): {1}".format(e.errno, e.strerror)
        except Exception as e:
            print "Other exception: " + e.message + str(e.__class__)

        svcObjectsArr = []

        for i, line in enumerate(tmpARR):
            ####################################################
            # 1. Split line by tokens                          #
            # 2. Create SVC object and fill with relevant data #
            ####################################################
            svcObj = SvcObj.SvcObj()
            tokens = line.split(" ")

            if tokens[-1] == "":
                pass
            else:
                svcObj.errorCode = int(tokens[-1])

            svcObj.errorDate = int("20" + tokens[0]) # Build the correct format for timestamp
            svcObjectsArr.append(svcObj)
        for item in svcObjectsArr:
            ################################################
            # Search until one month behind still relevant #
            ################################################
            if item.errorDate >= (int(self.timestamp) - 200000000):
                item.relevant = True
                print "SVC timestamp=",item.errorDate
                print "SVC Error Code=", item.errorCode
                print "#" * 80

        for item in svcObjectsArr:

            if item.relevant == True:
                return item.errorCode

        return -1

