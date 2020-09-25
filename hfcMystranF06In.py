import FreeCAD,FreeCADGui
import FreeCAD,FreeCADGui
import Fem
import os
import subprocess

import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *

class hfcMystranF06In:
	"Mystran result object"
	def GetResources(self):
		return {"MenuText": "Edit F06",
				"Accel": "Ctrl+t",
				"ToolTip": "Edit F06",
				"Pixmap": os.path.dirname(__file__)+"./resources/f06.svg"
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
				filename = QFileDialog.getOpenFileName(None,QString.fromLocal8Bit("Read a Mystarn's F06 file"),path, "*.F06") # PyQt4
			except Exception:
				filename, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Read a Mystran's F06 file", path, "*.F06") #PySide
				
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
			filename=filenameDat[:len(filenameDat)-3]+'F06'
		
		process=subprocess.Popen(["notepad",filename])

		
		

FreeCADGui.addCommand('hfcMystranF06In',hfcMystranF06In())