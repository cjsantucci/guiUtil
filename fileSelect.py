'''
Created on Feb 4, 2017

@author: chris
'''

import guiUtil.guidata as gdat
import os
from PyQt4.Qt import *

class pb_combo_selector( object ):
    '''
    create a group of buttons to aid in selecting files
    Keeps a history around
    '''


    def __init__( self, selectDir= False, historyLength= 10, \
                  persistentDir= None, persistentFile= None, prefGroup= None, \
                  caption= "", buttonstr= "", guiDataObj= None, \
                  defaultFileList= None, groupSubCat= None ):
        '''
        Constructor
        '''
        
        self.historyLength= historyLength
        self.caption= caption
        self.selectDir= selectDir

        self.guiData= self._createGuiData( guiDataObj, groupSubCat, defaultFileList, \
                                           prefGroup, persistentDir, persistentFile )
        
        self._initStartDir()
                
        self._setupComboBox()
        self._setupPushButton( buttonstr )
    
    def _setupPushButton( self, buttonstr ):
#         self.ComboBox.setEditable( True )
        self.PushButton= QPushButton( buttonstr )
        self.PushButton.clicked.connect( self._buttonPushed )
    
    def _setupComboBox( self ):
        self.ComboBox= QComboBox()
        p= self.ComboBox.palette()
        self.ComboBox.setAutoFillBackground( True );
        p.setColor( self.ComboBox.backgroundRole(), Qt.black )    
        self.ComboBox.setPalette( p )
        
        self.guiData.fileList= [ anElement for anElement in self.guiData.fileList if not anElement.replace(" ","") == "" ]
        self.ComboBox.addItems( self.guiData.fileList )
        
        # leave this last so that it will not grab the item data and save un-necessarily on init
        self.ComboBox.currentIndexChanged.connect( self._selectionchange )
    
    def _createGuiData( self, guiDataObj, groupSubCat, defaultFileList, \
                        prefGroup, persistentDir, persistentFile ):
        
        if defaultFileList is None:
            defaultFileList= " "
        
        if guiDataObj is not None:
            guiData= gdat.guiData( guiDataObj= guiDataObj, groupSubCat= groupSubCat, \
                                   initDefaultDict= { "fileList": defaultFileList } )
        else:
            guiData= gdat.guiData( persistentDir= persistentDir, \
                                   persistentFile= persistentFile, \
                                   prefGroup= prefGroup, \
                                   groupSubCat= groupSubCat, \
                                   initDefaultDict= { "fileList": defaultFileList }  )

        if type( guiData.fileList ) != type( list() ):
            guiData.fileList= [ guiData.fileList ]
        
        return guiData
    
    def getComboItems( self ):
        return [ self.ComboBox.itemText(i) 
                for i in range( self.ComboBox.count() ) ]
    
    def _initStartDir( self ):
        """
        start directory for file selection dialog
        """
        self.startDir= ""
        if not self.selectDir and len( self.guiData.fileList ) > 0:
            if os.path.isdir( os.path.dirname( self.guiData.fileList[0] ) ):
                self.startDir= os.path.dirname( self.guiData.fileList[0] )
                              
        elif  len( self.guiDaata.fileList ) > 0:
            if os.path.isdir( self.guiData.fileList[0] ):
                self.startDir= self.guiData.fileList[ 0 ]
    
    def _selectionchange( self ):
        """
        needed to resave the most recent order based on click
        """
        
        # needed for weird state changes
        if self.ComboBox.count() == 0:
            return 
        
        fileList= [ self.ComboBox.itemText( i ) for i in range( self.ComboBox.count() ) ]        

        tmp= fileList[ 0 ]
        fileList[ 0 ]= self.ComboBox.currentText()
        fileList[ self.ComboBox.currentIndex() ]= tmp
        
        self.guiData.fileList= fileList
        self.guiData.save( "fileList" )
    
    def _buttonPushed( self ):
        """
        saves the list if a new file was selected.
        """
        
        qfd= QFileDialog()
        
        passDir= ""
        if len( self.guiData.fileList ) > 0 and self.guiData.fileList[0] != "":
            if not self.selectDir:
                passDir= os.path.dirname( self.guiData.fileList[0] )
            else:
                passDir= self.guiData.fileList[ 0 ]
            
        if self.selectDir:
            fileName= qfd.getExistingDirectory( caption= self.caption, directory= self.startDir )
        else:
            fileName= qfd.getOpenFileName( caption= self.caption, directory= self.startDir )
        
        if fileName == "":
            return
        
        while fileName in self.guiData.fileList:
            self.guiData.fileList.remove( fileName )
        
        if type( self.guiData.fileList ) != type( list() ):
            self.guiData.fileList= []
            
        self.guiData.fileList.insert( 0, fileName )
        self.guiData.fileList= self.guiData.fileList[ :self.historyLength ]
        self.guiData.save( "fileList" )
        if fileName != "":
            self.ComboBox.clear()
            self.ComboBox.addItems( self.guiData.fileList )
#             self.ComboBox.
    
        
        