#!/usr/bin/env python

'''
Python-Tail - Unix tail follow implementation in Python. 

python-tail can be used to monitor changes to a file.

Example:
    import tail

    # Create a tail instance
    t = tail.Tail('file-to-be-followed')

    # Register a callback function to be called when a new line is found in the followed file. 
    # If no callback function is registerd, new lines would be printed to standard out.
    t.register_callback(callback_function)

    # Follow the file
    t.follow() '''

# Author - Kasun Herath <kasunh01 at gmail.com>
# Source - https://github.com/kasun/python-tail

import os
import sys
import time
import pyinotify

class IOHandler(pyinotify.ProcessEvent):
    def __init__(self, full_path):
        self.file_name = os.path.basename(full_path)
        self.dir_name = os.path.dirname(full_path)
        self.create = False
    def process_IN_CREATE(self, event):
        #print ('Action',"create file:", event.path, event.name, self.file_name)
        if event.name != self.file_name:
            return
        self.create = True
    def process_IN_MODIFY(self, event):
        #print ('Action',"modify file:", event.path, event.name, self.file_name)
        if event.name != self.file_name:
            return

class Tail(object):
    ''' Represents a tail command. '''
    def __init__(self, tailed_file):
        ''' Initiate a Tail instance.
            Check for file validity, assigns callback function to standard out.
            
            Arguments:
                tailed_file - File to be followed. '''

        self.tailed_file = tailed_file
        self.callback = sys.stdout.write
        ####
        self.watch_path = os.path.dirname(tailed_file)
        if not os.path.exists(self.watch_path):
            raise Exception("Path Not Exist")

        self.io_handler = IOHandler(tailed_file)

        self.wm = pyinotify.WatchManager()
        mask = pyinotify.IN_CREATE | pyinotify.IN_MODIFY
        self.notifier = pyinotify.Notifier(self.wm, self.io_handler)
        self.wm.add_watch(self.watch_path, mask)


    def follow(self):
        ''' Do a tail follow. If a callback function is registered it is called with every new line. 
        Else printed to standard out.
    
        Arguments:
            s - Number of seconds to wait between each iteration; Defaults to 1. '''

        file_ = None
        if os.path.exists(self.tailed_file):
            file_ = open(self.tailed_file)
            # Go to the end of file
            file_.seek(0,2)
        while True:
            self.notifier.process_events()

            if self.io_handler.create:
                file_ = open(self.tailed_file)
            
            if file_ != None:
                while True:
                    curr_position = file_.tell()
                    line = file_.readline()
                    if not line:
                        file_.seek(curr_position)
                        break
                    else:
                        self.callback(line)

            if self.notifier.check_events():
                self.notifier.read_events()


    def register_callback(self, func):
        ''' Overrides default callback function to provided function. '''
        self.callback = func


class TailError(Exception):
    def __init__(self, msg):
        self.message = msg
    def __str__(self):
        return self.message

