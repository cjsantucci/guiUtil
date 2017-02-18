'''
Created on Feb 12, 2017

@author: chris
'''

import functools
import traceback

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import os
import subprocess as subp
import sys
import time

class scroller( QWidget ):
    '''
    classdocs
    '''


    def __init__( self, parent= None, 
                  processCommand= "",
                  app= None, onStartup= False, \
                  closeOnFinish= False, \
                  statusRect= None, \
                  processRect= None, \
                  qmw= None, **kwargs ):
        
        assert statusRect is not None and processRect is not None, \
        "editRect and processRect must be passed"
        
        self.onStartup= onStartup
        self.closeOnFinish= closeOnFinish
        
        if type( processCommand ) == type( list() ):
            processCommand= " ".join( processCommand )
        self.processCommand= processCommand
        
        if app is None:
            app= QApplication([])
        
        self.app= app        
        super( scroller, self ).__init__( parent )
        
        self.layout= QGridLayout()
        
        if qmw is None:
            self.qmw= QMainWindow()
        else:
            self.qmw= qmw
            
        self.qmw.setObjectName( "Window for: " + self.processCommand )
        
        self.processScrollArea= self._setupEdit( processRect )
        self.processEdit.setText( self.processCommand )
        
        self.statusScrollArea= self._setupEdit( statusRect )
        
        
        self._setupMainWindow()
            
        if self.onStartup:
            self.execute( onStartup= self.onStartup )
#         self.sysCommand( processCommand )
        
        sys.exit( app.exec_() )
    
    def _setupEdit( self, rect ):
        edit = QTextEdit()
        edit.setGeometry( rect )
        
        scrollArea = QScrollArea( self.qmw )
        scrollArea.setWidget( edit ) 
        scrollArea.setGeometry( QRect( rect.left(), rect.top(),\
                                   rect.width()+2, rect.height()+2 )       
                               )
        return scrollArea
    
    def _setupMainWindow( self ):
#         pass
        centerPoint= self.centerOfScreenForCurrentMouse() 
        
        #process Rect
        pR= self.processScrollArea.geometry()
        # status Rect
        sR= self.statusScrollArea.geometry()
        
        wMaxX= max( [ pR.left()+ pR.width(), sR.left()+ sR.width() ] )
        wMaxY= max( [ pR.top()+ pR.height(), sR.top()+ sR.height() ] )
        
        self.qmw.setGeometry( \
                            QRect( centerPoint.x()-wMaxX/2, \
                            centerPoint.y()-wMaxY/2,\
                            wMaxX,\
                            wMaxY ) )
        self.layout.addWidget( self.statusScrollArea, 0, 0 )
        self.layout.addWidget( self.processScrollArea, 1, 0 )
        
        self.qmw.show()
        
    def execute( self, onStartup= False ):
        if self.onStartup:
            QTimer.singleShot( 500, functools.partial( self.sysCommand, self.processCommand ) )
        else:
            self.sysCommand( self.processCommand )
            
    def sysCommand( self, processCommand ):
        proc = subp.Popen( processCommand, stdout=subp.PIPE, stdin=subp.PIPE, stderr=subp.STDOUT )
        """
        enable push button here
        """
        self.proc= proc
        while proc.poll() is None :
            self._processProc()
           
        self._processProc( readlines= True ) 
    
        if self.closeOnFinish:
            self.qmw.close()
    
    def _processProc( self, readlines= False  ):
        """
        read data from stdo out and update the scroller
        if data was provided
        """
        try:
            data= self._processProcHelper( "stdout", readlines )
            if data != "":
                self.statusEdit.append( data )
                self._updateScroller()
        except:
            traceback.print_exc()
        """
        I Killed this code and piped it to stdout
        In order to color the errors red one would 
        need to put a timer on .readline() or .readlines()
        because it would wait for stderr to output that stuff...
        didn't feel like writing that code.
        # print std error
#         try:
#             data= self._processProcHelper( "stderr", readlines )
#             if data != "":
#                 self.textEdit.setTextColor( QColor( "red" ) )    
#                 self.textEdit.append( data )
#                 self._updateScroller()
#                 self.textEdit.setTextColor( QColor( "black" ) )    
        except:
            traceback.print_exc()
        
        time.sleep( 0.1 )
        """
    
    def _updateScroller( self ):
        c =  self.processEdit.textCursor();
        c.movePosition(QTextCursor.End);
        self.processEdit.setTextCursor(c);
        self.app.processEvents()
    
    def _processProcHelper( self, caseField, readlines ):
        """
        when proc is no longer present do a readlines to get the rest
        otherwise just look for one line at a time to continue to update the output.
        reading from readlines will wait for the program to finish.
        """
        proc= self.proc
        data= ""
        if not readlines:
            io= getattr( proc, caseField )
            if io is not None:
                data= io.readline().decode()
        else:
            io = getattr( proc, caseField )
            if io is not None:
                data= io.readlines()
                if data != "":
                    data= [ aLine.decode() for aLine in data ]
                    data= "".join( data )
            
        return data
        
    def kill( self ):
        if self.proc.poll() is None:
            try:
                os.kill( self.proc.pid )
            except:
                pass
            
    
    def centerOfScreenForCurrentMouse( self ):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber( QApplication.desktop().cursor().pos() )
        centerPoint = QApplication.desktop().screenGeometry( screen ).center()
        return centerPoint
    
    def getStatusEdit( self ):
        return self.statusScrollArea.widget()
    
    def getProcessEdit( self ):
        return self.processScrollArea.widget()
    
    def setProcessEdit( self, inWidget ):
        self.processScrollArea.setWidget( inWidget )
    
    def setStatusEdit( self, inWidget ):
        self.statusScrollArea.setWidget( inWidget )
        
    statusEdit= property( getStatusEdit, setStatusEdit )
    processEdit= property( getProcessEdit, setProcessEdit ) 
    
if __name__ == "__main__": 
    scroller( processRect= QRect( 0, 50, 798, 80 ), \
             statusRect= QRect( 0, 131, 798, 320 ), \
             processCommand="/home/chris/h5Sim.pydfgggalssssssssssssasssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggggg")

    
    
    