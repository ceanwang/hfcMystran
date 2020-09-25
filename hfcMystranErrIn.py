import FreeCAD,FreeCADGui
import FreeCAD,FreeCADGui
import Fem
import os
import subprocess

import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *

class hfcMystranErrIn:
	"Mystran result object"
	def GetResources(self):
		return {"MenuText": "Log In",
				"Accel": "Ctrl+t",
				"ToolTip": "Input log file",
				"Pixmap": os.path.dirname(__file__)+"./resources/err.svg"
		}

	def IsActive(self):

		#if FreeCAD.ActiveDocument == None:
		#	return False
		#else:
		#	return True
        
		return True

	def Activated(self):
		import FreeCADGui

		#path = FreeCAD.getHomePath()+"bin/"
		#print (path)
		#fName = "D:\\MystranTest\\Plate\\PLATE.log"
		#print (fName)
		#FreeCAD.openDocument(fName)
		#doc=FreeCADGui.newDocument()
		#doc.setEdit(fName)
		
		iHfc =FreeCAD.ActiveDocument.getObject('hfc')
		if iHfc==None:
			ininame="Mod/hfcMystran/hfcMystran.ini"
			
			inifile = FreeCAD.getHomePath()+ininame
			if os.path.exists(inifile):	
				iniF = open(inifile,"r")
				path=iniF.readline()
				iniF.close()
			else:
				inipath=FreeCAD.getHomePath()
					
			try:
				filename = QFileDialog.getOpenFileName(None,QString.fromLocal8Bit("Read a Mystarn's Err file"),path, "*.Err") # PyQt4
			except Exception:
				filename, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Read a Mystran's Err file", path, "*.Err") #PySide
				
			data=filename.split("/")
			n=len(data)
			path=""
			for i in range(n-1):
				path=path+data[i]+"/"

			inifileOut = FreeCAD.getHomePath()+ininame
			iniFout = open(inifileOut,"w")
			iniFout.writelines(path)
			iniFout.close()

		else:	
			path=iHfc.DatPath
			filenameDat=iHfc.DatFile
			filename=filenameDat[:len(filenameDat)-3]+'err'
		
		process=subprocess.Popen(["notepad",filename])

		#guidoc = FreeCADGui.ActiveDocument
		#guidoc.open(filename)
		
		# check if another VP is in edit mode
		# https://forum.freecadweb.org/viewtopic.php?t=13077#p104702
		#if not FreeCADGui.ActiveDocument.getInEdit():
		#	FreeCADGui.ActiveDocument.setEdit(fName)
		#else:
		#	from PySide.QtGui import QMessageBox
		#	message = "Active Task Dialog found! Please close this one before opening  a new one!"
		#	QMessageBox.critical(None, "Error in tree view", message)
		#	FreeCAD.Console.PrintError(message + "\n")

		
		

FreeCADGui.addCommand('hfcMystranErrIn',hfcMystranErrIn())