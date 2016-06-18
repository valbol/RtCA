#!/usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################

import paramiko
from scp import SCPClient


HOST_PATH = '/mnt/bugs/RACE-'
HOST = '9.151.189.30'   # AKA - MegaStore
USER_NAME = 'root'
PASS = 'a1b2c3'


class ClientOps:

    def __init__(self, race_num):

        ############################################
        # building the path to the directory       #
        # User input race_unm                      #
        # Absolute path is: '/mnt/bugs/RACE-XXXX'  #
        ############################################
        self.racePath = HOST_PATH + str(race_num)

        ##########################################
        # Creating secure connection to IBM host #
        # with SSH protocol                      #
        ##########################################
        print "Creating connection......."
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(HOST, username=USER_NAME, password=PASS)
            print "Connected  successfully to %s!!!" % HOST
        except paramiko.AuthenticationException:
            print "Authentication failed when connecting to %s !!!" % HOST

        print "=" * 30
        print "path is: %s" % self.racePath
        print "=" * 30

        ##################################################
        # Copy the required directory from Remote host   #
        # to local host with SCP (secured Copy) protocol #
        ##################################################

        try:
            scp = SCPClient(ssh.get_transport())

            print "Copying Directory..."
        except Exception as e:
                print "Other exception: " + e.message + str(e.__class__)      #+ "SCP=" + str( scp)
        scp.get(self.racePath, '/home/support/Desktop', True, False)

        ###########################################
        # Close SCP and SSH concetion when done   #
        ###########################################
        scp.close()
        print "SCP Connection closed %s" % scp
        ssh.close()
        print "SSH Connection closed %s" % ssh






