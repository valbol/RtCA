#! /usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################

import pymongo
from pymongo import *
import MongoObj
import datetime

MAYHAVE_ASSERT = "MAYHAVE_ASSERT"
MAIN_ASSERT = "MAIN_ASSERT"
LOG = "log"

class MongoDB:

    def __init__(self):
    # Connection to Mongo-DB
        try:
            self.client = MongoClient()  # Default path to local host
            print "MongoDB connected successfully!!!"
        except pymongo.errors.ConnectionFailure as e:
            print "Could not connect to MongoDB: %s", e

        db = self.client.AnalyzerDB  #Choosing our DB


        self.apars = db.APARS  #Choosing our COLLECTION
        self.mongoObjects = []
        self.statistics = db.STATS
        self.archive = db.ARCH
        return

    #################################################
    # Find suspected issues in the APAR collection #
    ################################################
    def find_apar(self, svc_error_no, vers):



        #############################################
        # Pull documents which fit the requirements #
        #############################################
        cursor = self.apars.find({"platform_errors.errorID": svc_error_no,
                                  "affected_versions.major_vers": vers,
                                  "compression_errors.file_type": LOG})


        for apar in cursor:
            mongoObj = MongoObj.MongoObj()
            for counter, i in enumerate(range(int(apar['errors_no']))):

                mongoObj.aparId = apar["id"]
                mongoObj.aparURL = apar["apar_url"]
                mongoObj.compAsserts.append(apar["compression_errors"][i]['assert'])
                mongoObj.severity.append(apar["compression_errors"][i]['severity'])

                if mongoObj.severity[i] == MAIN_ASSERT:
                    mongoObj.mainAssertCounter += 1
                mongoObj.noOfCompAsserts = i+1

            ## Add object to the list ##
            self.mongoObjects.append(mongoObj)


        return

    #################################
    # Check if already exist in DB #
    ################################

    def check_exist(self, raceNo):

        check = self.archive.find_one({"race_no": raceNo})
        if str(check) =="None":
            return False
        else:
            return True


    #############################################
    # Insert the current analysis that was done #
    #############################################
    def insert_statistics(self, apar_id, time, raceNo):

        ###########################################################
        # Save last analysis  documentation in Archive collection #
        ###########################################################
        current = {"race_no" : raceNo,
                    "id" : apar_id,
                    "analysis_time": time,
                    "date" : datetime.datetime.utcnow()
            }
        document = self.archive.insert_one(current)

        #################################################
        # check if document exist with the specified ID #
        #################################################
        cursor = self.statistics.find({"id": apar_id})
        if cursor.count() > 0:

            for doc in cursor:
                tmpCoun = doc["counter"]
                tmpTime = doc["avg_analysis_time"]
            ###################################
            # Calculate average analysis time #
            ###################################
            analTime = (tmpTime * tmpCoun) + time
            tmpCoun += 1
            avgTime = analTime/tmpCoun
            print "avgTime", avgTime
            ######################################################
            # Update document with Counter ++ and new avg. time  #
            #####################################################
            document = self.statistics.find_one_and_update({"id": apar_id}, {'$inc': {'counter': 1}, '$set': { "avg_analysis_time": avgTime }})
        else:
            ###############################################
            # Add new statistic entry to STATS collection #
            ###############################################
            print "ELSE"
            newEntry = {"id": apar_id,
                        "counter": 1,
                        "avg_analysis_time": time
            }
            document = self.statistics.insert_one(newEntry)
        return

    ##################################
    # Pull APAR vs Accurences info'  #
    ##################################
    def stat_by_counter(self):

        tmpId = []
        tmpTime = []
        print "COUNTER=", self.statistics.count()
        cursor = self.statistics.find().sort("id")
        for doc in cursor:

            tmpId.append(doc["id"])
            tmpTime.append(doc["counter"])


        return tmpId, tmpTime
    #######################################
    # Pull avgAnalysis & accurences info' #
    #######################################
    def stat_by_time(self):

        tmpId = []
        tmpTime = []
        tmpAccure = []
        counter = self.statistics.count()
        print "COUNTER=", counter
        cursor = self.statistics.find().sort("id")


        for doc in cursor:

            tmpId.append(doc["id"])
            tmpTime.append(doc["avg_analysis_time"])
            tmpAccure.append(doc["counter"])


        return tmpId, tmpTime, tmpAccure, counter

    #################################################
    # Finds all compression error in given APAR ID  #
    ################################################
    def find_error_by_apar_id(self,apar_id):

        self.aparID = apar_id

         #For specific APAR print all Errors
        for apar in self.apars.find({"id": self.aparID}):
            print "Compression Errors : ", apar["compression_errors"]

        return

    ##############################################
    # Object destructor - disconnect from the DB #
    ##############################################
    def __del__(self):

        self.client.close()
        print "close: ", self.client



