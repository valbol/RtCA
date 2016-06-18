#!/usr/bin/python

####################################
# RTCS - Made by Valery Boltavsky  #
####################################

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import MongoDB
import datetime

import random

LOCAL_DIR_PATH = '/home/support/Desktop/'


class Stats():

    """ The Statistics class, which pull current information
        from MongoDB and create statistical charts
        save png file for the operation """

    #####################################
    # Constructor creates mongo instance #
    #####################################
    def __init__(self):

        self.mongo = MongoDB.MongoDB()

        pass

    #######################
    # Creates Grid chart #
    #########3############
    def grid_chart(self):

        #####################
        # Pull Info from DB #
        #####################
        id, avgTime, accure, counter = self.mongo.stat_by_time()

        ############################################
        # Build the grid chart with provided info  #
        ############################################
        N = counter
        analTimeAvg = avgTime
        ind = np.arange(N)  # the x locations for the groups
        width = 0.35       # the width of the bars
        fig, ax = plt.subplots()
        ################################
        # Build representing rectangles #
        ################################
        rects1 = ax.bar(ind, analTimeAvg, width, color='lightskyblue')
        accureCount=accure
        rects2 = ax.bar(ind + width, accureCount, width, color='yellowgreen' )
        #############################################
        # add some text for labels, title and axes  #
        #############################################
        ax.set_ylabel("Time (sec)/Occurrences #")
        ax.set_title('Analysis time  & Occurrences amount')
        ax.set_xticks(ind + width)
        ax.set_xticklabels(id)
        ax.legend((rects1[0], rects2[0]), ('Avg. analysis time', 'Occurrences'))
        def chartLabl(rects):
        ########################
        # attach text labels   #
        ########################
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height), ha='center', va='bottom')

        chartLabl(rects1)
        chartLabl(rects2)
        date =datetime.datetime.utcnow()
        ##################
        ## SAVE figure  ##
        ##################
        plt.savefig(LOCAL_DIR_PATH + "Stats_Pie-" + str(date) + '.png')

        return

    #######################
    # Creates Pie chart #
    #########3############
    def pie_chart(self):

        #####################
        # Pull Info from DB #
        #####################
        labels, sizes = self.mongo.stat_by_counter()

        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
        #################################################################
        # Set aspect ratio to be equal so that pie is drawn as a circle #
        #################################################################
        plt.axis('equal')
        date =datetime.datetime.utcnow()
        ##################
        ## SAVE figure  ##
        ##################
        plt.title('Bugs occurred ', bbox={'facecolor':'0.9', 'pad':1})
        plt.savefig(LOCAL_DIR_PATH + "Stats_Pie-" + str(date) + '.png')

        return