import FreeCAD,FreeCADGui
import FreeCAD,FreeCADGui
import Fem
import os
import subprocess

import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *

class hfcMystranLogIn:
	"Mystran result object"
	def GetResources(self):
		return {"MenuText": "Log In",
				"Accel": "Ctrl+t",
				"ToolTip": "Input log file",
				"Pixmap": os.path.dirname(__file__)+"./resources/log.svg"
		}

	def IsActive(self):

		#if FreeCAD.ActiveDocument == None:
		#	return False
		#else:
		#	return True
        
		return True

	def Activated(self):
		import FreeCADGui

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
				filename = QFileDialog.getOpenFileName(None,QString.fromLocal8Bit("Read a Mystarn's log file"),path, "*.log") # PyQt4
			except Exception:
				filename, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Read a Mystran's log file", path, "*.log") #PySide
				
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
			filename=filenameDat[:len(filenameDat)-3]+'log'
		
		process=subprocess.Popen(["notepad",filename])

		
		

FreeCADGui.addCommand('hfcMystranLogIn',hfcMystranLogIn())