'''
Created on Feb 13, 2017

@author: chris
'''
from guiUtil.scroller import scroller
from guiUtil import guidata as gdat

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os

class scroll_control( QWidget ):
    '''
    classdocs
    '''


    def __init__( self, **kwargs ):
        '''
        Constructor
        '''
        
        idd= { "onStartUp": True,
              "processCommand": "/home/chris/h5Sim.py", 
              "closeOnFinish": False
            }
        guiData= gdat.guiData( persistentDir= os.environ[ "HOME" ]+ "/.scroll_control", \
                               persistentFile= 'jpePref.h5', \
                               prefGroup= "/scroll_control", \
                               initDefaultDict= idd )
        
        self.guiData= guiData
        
        """
        Do these
        # add load method to guidata?
        # the process command will be sent in, so how do we not double it here
        """ 
        scrObj= scroller( **kwargs, **self.guiData.defDict )
        scrObj.blah()
        
if __name__ == "__main__":
    inputdict= {
                "processRect": QRect( 0, 0, 798, 50 ), \
                "editRect": QRect( 0, 60, 798, 320 ), \
                 }
    scroll_control( **inputdict )
        