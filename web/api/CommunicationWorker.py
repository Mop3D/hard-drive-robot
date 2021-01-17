#!/usr/bin/python
# coding: utf8

"""
RobotWorker.py

date: 01.03.2021
author: oliver Klepach, Martin Weichselbaumer
"""

from StatusObject import StatusObjectBase

#
# StatusObject
# simple implementation
#
class CommunicationWorker(StatusObjectBase):
    # init
    def __init__(self, socketHandler):
        # set the communication status modul name
        self.StatusModulName = "CommunicationWorkerModul"
        self.StatusInfo("Init Object")

    def CommCommand(self, messageFrom, action, json):
        self.StatusInfoFrom(messageFrom, "Action: {0}, {1}".format(action, json))
        #self.WriteJsonToSocket(messageFrom, action, json, True):

    #def StatusInfo(self, messageFrom, message):
    #    self.WriteStatus(messageFrom, "Info", message, True)
