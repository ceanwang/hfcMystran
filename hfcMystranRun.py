import FreeCAD,FreeCADGui
import os
import subprocess

class hfcMystranRun:
	"hfcMystranRun object"
	def GetResources(self):
        # return {'Pixmap': 'path_to_icon.svg', 'MenuText': 'my command', 'ToolTip': 'very short description'}
		return {"MenuText": "Solver Run",
				"Accel": "Ctrl+R",
				"ToolTip": "Run mystran to solve the case",
				"Pixmap": os.path.dirname(__file__)+"./resources/My.svg"
		}

	def IsActive(self):

		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
        
		iHfc =FreeCAD.ActiveDocument.getObject('hfc')
		if iHfc==None:
			#iHfc = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",'hfc')
			#CFG(iHfc)
			print ('Please open a dat file first.')
		else:	
			path=iHfc.DatPath
			filename=iHfc.DatFile

		#filename=FreeCAD.getHomePath()+"bin/hfcMystran.Dat"
		#print (filename)

		#process=subprocess.Popen(["mystran",filename])
		
		os.chdir(path)
		process=subprocess.Popen(["mystran",filename],stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf8")
		stdout,stderr=process.communicate()
		print(stdout)
		print(stderr)

		#out,err=process.communicate()
		#print(out)
		#print(err)


FreeCADGui.addCommand('hfcMystranRun',hfcMystranRun())