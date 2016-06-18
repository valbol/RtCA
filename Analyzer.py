#! /usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################

import os
import ClientOps
import MongoDB
import FilesOps
import RaceObj
import shutil

MAYHAVE_ASSERT = "MAYHAVE_ASSERT"
MAIN_ASSERT = "MAIN_ASSERT"

FILES_DATE_PATTERN = "%a %b %d %H:%M:%S %Y"
MY_DATE_PATTERN = "%Y%m%d%H%M%S"
LOCAL_DIR_PATH = '/home/support/Desktop/RACE-'

""" Analyzer Class is the main class of the project,
    This class is initiate all the Modules in this system """
class Analyzer():

    def __init__(self, raceNo, eventTimeStamp):

        ################################################################
        # Analyzer constructor initiate all the modulus of the program #
        # This is the main module of the project - the Brain which     #
        # Main module == in charge of all the other modules            #
        ################################################################


        ###########################################################################################
        # If folder does not exist on user local PC, then connect to remote server and copy files #
        ###########################################################################################
        if os.path.isdir(LOCAL_DIR_PATH + str(raceNo)) == False:
            client = ClientOps.ClientOps(raceNo)

        ############################################################
        # Start the analyzing process - execute Modules functions  #
        ############################################################
        self.mongo = MongoDB.MongoDB()
        self.fileObj = FilesOps.FilesOps(raceNo, eventTimeStamp)
        #self.fileObj.find_SVC_errors()
        svcErrorCode = self.fileObj.find_SVC_errors()
        if svcErrorCode == -1:
            print "SVC File error! -- File does not exist! or SVC Error not found"
            return

        self.fileObj.collect_issues()
        self.fileObj.sotrtedAssertArr
        print "#" *20
        print "RACE VERSION:", self.fileObj.getVers()
        print "#" *20

        #######################################################################
        # Find in SVC file the relevant error code which related to the issue #
        #######################################################################

        self.mongo.find_apar(svcErrorCode, self.fileObj.raceVers)
        self.raceObjects = []  # List of RACE objects
        return

    ##################################################
    # Function which creates instance of race object #
    ##################################################
    @staticmethod
    def create_race_obj(mongoItem, vers):

        raceObj = RaceObj.RaceObj()
        raceObj.aparId = mongoItem.aparId
        raceObj.mainAssertCounter = mongoItem.mainAssertCounter
        raceObj.aparURL = mongoItem.aparURL
        raceObj.version = vers
        return raceObj

    #############################################################
    # Function which check if all compression errors are unique #
    #############################################################
    def confirm_issue(self):

        for item in self.raceObjects:
            seen = set()
            ##############################
            # Ignore defect race objects #
            ##############################
            if item.compAsserts != [] and item.mainAssertCounter == 0:
                ######################################################################
                # If all the Items in compAsserts are unique return True, else False #
                ######################################################################
                item.found = not any(i in seen or seen.add(i) for i in item.compAsserts)
                print "Confirm Item found = ", item.found
                #print "item" , item.compAsserts
        return

    #######################################################################
    # Main Module function which build the objects and identify the issue #
    #######################################################################
    def analyze_issue(self):
        vers = self.fileObj.getVers()
        for mongoItem in self.mongo.mongoObjects:

            #####################################################################################
            # Create RACE object for the issue and start scanning the lines in sotrtedAssertArr #
            #####################################################################################
            raceObj = Analyzer.create_race_obj(mongoItem,vers)  # ---> Static method syntax -- ClassName.method

            for item in self.fileObj.sotrtedAssertArr:
                ###################################################################
                # For each assert in compression asserts if exist in a given line #
                ###################################################################

                for j in range(len(mongoItem.compAsserts)):
                    #############################################################
                    # Search in sotrtedAssertArr for issues from Mongo objects, #
                    # if found add it to RACE object and update relevant values #
                    #############################################################
                    if item.find(mongoItem.compAsserts[j]) != -1 and raceObj.mainAssertCounter > 0:

                        raceObj.compAsserts.append(item)
                        raceObj.severity.append(mongoItem.severity[j])
                        if raceObj.severity[-1] == MAIN_ASSERT:
                            raceObj.mainAssertCounter -= 1


                        #####################################################################################
                        # If found --> pop the Item from Mongo-Object in order to avoid ASSERT duplication, #
                        # Don't search again for this kind of issue inside sotrtedAssertArr                 #
                        #####################################################################################
                        mongoItem.compAsserts.pop(j)
                        break
                    else:
                        ##############################
                        # Skip this line and proceed #
                        ##############################
                        next(iter(self.fileObj.sotrtedAssertArr))

            self.raceObjects.append(raceObj)
        #####################################
        # Confirm that issue has been found #
        #####################################
        self.confirm_issue()




        print "Suspected APARs", len(self.raceObjects)
        for item in self.raceObjects:
            if item.found:
                print "\n---- Analysys DONE ----"
                return item
    ################################################################

        return

    def __del__(self):
        print "---- Deleting folder ----"
        shutil.rmtree('/home/support/Desktop/TEST123')