import FreeCAD,FreeCADGui
import Fem
import os
import shutil

import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *

class hfc:
    def __init__(self, obj):
        '''"two properties" '''
        obj.addProperty("App::PropertyString","DatPath","hfc","Dat file path")
        obj.addProperty("App::PropertyString","DatFile","hfc","Dat file name")

        obj.Proxy = self


class Node:
    def __init__(self, id, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.id = str(id)

# elmnt n1     n2    Ax     Asy     Asz     Jx     Iy     Iz     E     G     roll  density
class Member:
    def __init__(self, id, n1, n2):
        self.n1 = n1
        self.n2 = n2
        self.id = str(id)

class MemberCROD:
    def __init__(self, id, n1, n2, mtype):
        self.n1 = n1
        self.n2 = n2
        #self. = 
        self.mtype=mtype
        self.id = str(id)
		
class MemberCBAR:
    def __init__(self, id, n1, n2, mtype):
        self.n1 = n1
        self.n2 = n2
        #self. = 
        self.mtype=mtype
        self.id = str(id)
		
class MemberCBEAM:
    def __init__(self, id, n1, n2, mtype):
        self.n1 = n1
        self.n2 = n2
        #self. = 
        self.mtype=mtype
        self.id = str(id)
		
		
class MemberCTRIA3:
    def __init__(self, id, n1, n2, n3, mtype):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.mtype = mtype
        self.id = str(id)
        
class MemberCQUAD4:
    def __init__(self, id, n1, n2, n3, n4, mtype):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        #self. = 
        self.mtype=mtype
        self.id = str(id)
		
class MemberCQUAD8:
    def __init__(self, id, n1, n2, n3, n4, mtype):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        #self. = 
        self.mtype=mtype
        self.id = str(id)

class MemberCTETRA:
    def __init__(self, id, n1, n2, n3, n4, mtype):
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.mtype = mtype
        self.id = str(id)

class MemberCHEXA:
    def __init__(self, sid, n1, n2, n3, n4, n5, n6, n7, n8, mtype):
        self.sid = str(sid)
        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.n4 = n4
        self.n5 = n5
        self.n6 = n6
        self.n7 = n7
        self.n8 = n8
        self.mtype = mtype
        
		
#  Node    X-dsp       Y-dsp       Z-dsp       X-rot       Y-rot       Z-rot
class Displacement:
    def __init__(self, id, xdsp, ydsp, zdsp, xrot, yrot, zrot):
        self.xdsp = xdsp
        self.ydsp = ydsp
        self.zdsp = zdsp
        self.xrot = xrot
        self.yrot = yrot
        self.zrot = zrot
        self.id = str(id)

		
		
		
def SeekNextSec(fp, tStr):	
	while 1:
		line = fp.readline().strip()
		if line==tStr:
			return line
		else:
			#print (line)
			continue

def SeekOne(fp):	
	while 1:
		line = fp.readline().strip()
		data = line.split()

		if data[0]=="1":
			return line
		else:
			#print (line)
			continue
			
def moveon(fp):	
	while 1:
		line = fp.readline().strip()
		if len(line)==0 or line[0]=='#':
			continue
		else:
			return line
			
class hfcMystranDatInFemWire:
	"hfcMystranDatInFemWire object"
	def GetResources(self):
		return {"MenuText": "neu In",
				"Accel": "Ctrl+t",
				"ToolTip": "Input result neu file",
				"Pixmap": os.path.dirname(__file__)+"./resources/folderIconDatW.svg"
		}

	def IsActive(self):

		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		import ObjectsFem
		isMystran=1
		
		ininame="Mod/hfcMystran/hfcMystran.ini"
        
		inifile = FreeCAD.getHomePath()+ininame
		if os.path.exists(inifile):	
			iniF = open(inifile,"r")
			path=iniF.readline()
			iniF.close()
		else:
			inipath=FreeCAD.getHomePath()
                
		try:
			fName = QFileDialog.getOpenFileName(None,QString.fromLocal8Bit("Read a Mystarn's Dat/bdf file"),path, "*.Dat *.bdf") # PyQt4
		except Exception:
			fName, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Read a Mystran's Dat/bdf file", path, "*.Dat *.bdf") #PySide
            
		print ("src: "+fName)
		DesName = FreeCAD.getHomePath()+"bin/hfcMystran.Dat"	
		print ("Des: "+DesName)	
		shutil.copyfile(fName,DesName)	
        
		data=fName.split("/")
		n=len(data)
		path=""
		for i in range(n-1):
			path=path+data[i]+"/"

		inifileOut = FreeCAD.getHomePath()+ininame
		iniFout = open(inifileOut,"w")
		iniFout.writelines(path)
		iniFout.close()
		
		#print (path)
		iHfc =FreeCAD.ActiveDocument.getObject('hfc')
		if iHfc==None:
			iHfc = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",'hfc')
			hfc(iHfc)
			#iHfc.ViewObject.Proxy=0
			#ViewProviderCFG(iHfc.ViewObject)

		iHfc.DatPath = path
		iHfc.DatFile = fName
		
		
		numNode=0
		numMember=0
		
		nodes_x=[]
		nodes_y=[]
		nodes_z=[]

		NodeList = {}
		MemberList = {}                                  

		DisplacementList = {}  
		
		NodeEndList = {}
		MemberEndList = {}                                  

		ProjectDescription = ''
		
		nodes = {}
		results = []
		mode_results = {}
		mode_disp = {}
		iFilled=[]
        
		mode_disp_x=[]
		mode_disp_y=[]
		mode_disp_z=[]


		nDisp=0
		mDisp=0
		isDebug=1
		
		#factor = 25.42
		factor = 1
		
		factorZoom = 100

		#000000000000000000000000000000000000000000000000000000000000000000
		
		fpDat = open(fName)
		tline=[]
		for line in fpDat:
			aline=line.strip()	
			if len(aline)==0 or aline[0]=='$':
				continue
			else:		
				tline.append(line.strip())
		fpDat.close()
			
		for id in range(len(tline)):
        
			aline=tline[id].strip()	
			data = aline.split()
			data1 = aline.split(",")
			#print (data)
			
			# Node 22222222222222222222222222222222222222222222222222222222222222222222	
			if data[0]=='GRID':
				#           gid         cp  x1
                #GRID       10101       0   0.000   0.000   0.000       0
				gid=aline[8:16].strip()
				#cid1=aline[16:24].strip()
				x=aline[24:32].strip()
				y=aline[32:40].strip()
				z=aline[40:48].strip()
				
				NodeList[gid] = Node(gid, float(x), float(y), float(z))
				numNode=numNode+1                
                
			if data[0]=='GRID*':
				#GRID*    1                               0.00000E+00     0.00000E+00
				gid=aline[8:24].strip()
				#cid1=aline[24:40].strip()
				x=aline[40:56].strip()
				y=aline[56:72].strip()
				bline=tline[id+1].strip()	
				z=bline[8:24].strip()
				NodeList[gid] =  Node(gid, float(x), float(y), float(z))
				numNode=numNode+1                

           
			# Member 33333333333333333333333333333333333333333333333333333333333333333333333333333333333333	
            #CBAR    201     2       11      21      0.0     0.0     1.0                
			if data[0]=='CBAR':
				MemberList[data[1].strip()] =  MemberCBAR(data[1].strip(), data[3], data[4], data[0].strip())  
				numMember+=1

            #CBEAM   9400    9401    9401    9402    0.      0.      1.
			if data[0]=='CBEAM':
				MemberList[data[1].strip()] =  MemberCBEAM(data[1].strip(), data[3], data[4], data[0].strip())  
				numMember+=1

            #CROD, 418,418,8,3
			if data[0]=='CROD':
				MemberList[data[1].strip()] =  MemberCROD(data[1].strip(), data[3] ,data[4], data[0].strip())  
				numMember+=1



            #CROD, 418,418,8,3
			if data1[0]=='CROD':
				MemberList[data1[1].strip()] =  MemberCROD(data1[1].strip(), data1[3] ,data1[4], data1[0].strip())  
				numMember+=1
	

	
            #CTRIA3  24      91      1033    1032    1023
			if data[0]=='CTRIA3':
				MemberList[data[1].strip()] =  MemberCTRIA3(data[1].strip(), data[3] ,data[4] , data[5] ,data[0].strip())  
				numMember+=1

			#CQUAD4      1001       1    1001    1002    2002    2001
			if data[0]=='CQUAD4':
				MemberList[data[1].strip()] =  MemberCQUAD4(data[1].strip(), data[3], data[4], data[5], data[6], data[0].strip())  
				numMember+=1
            
			#CQUAD8     16004       1   16007   16009   18009   18007   16008   17009
            #18008   17007
			if data[0]=='CQUAD8':
				MemberList[data[1].strip()] =  MemberCQUAD8(data[1].strip(), data[3] ,data[4] , data[5] , data[6],data[0].strip())  
				numMember+=1

			#CTETRA   1       1       8       13      67      33
			if data[0]=='CTETRA':
				MemberList[data[1].strip()] =  MemberCQUAD4(data[1].strip(), data[3] ,data[4] , data[5] , data[6],data[0].strip())  
				numMember+=1
				
			#
			#CHEXA      10101     100   10101   10103   10303   10301   30101   30103+E     1
			#+E     1   30303   30301
			if data[0]=='CHEXA':
				bline=tline[id+1].strip()	
				if len(aline)==80:
					eid=aline[9:16].strip()
					pid=aline[17:24].strip()
					g1=aline[25:32].strip()
					g2=aline[33:40].strip()
					g3=aline[41:48].strip()
					g4=aline[49:56].strip()
					g5=aline[57:64].strip()
					g6=aline[65:72].strip()
				if aline[73:80]==bline[1:8]:
					g7=bline[9:16].strip()
					g8=bline[17:24].strip()
				
				#print (eid+" "+g1+" "+g2+" "+g3+" "+g4+" "+g5+" "+g6+" "+g7+" "+g8)
				MemberList[eid] =  MemberCHEXA(eid, g1, g2, g3, g4, g5, g6, g7, g8, data[0].strip())  
				numMember+=1

		#print (NodeList)
		#print (MemberList)
		
		print ('numNode = '+str(numNode))		
		print ('numMember = '+str(numMember))	
		
		#for id in NodeList:
		#	print (NodeList[id].id+" "+str(NodeList[id].x)+" "+str(NodeList[id].y)+" "+str(NodeList[id].z))
		
		femmesh = Fem.FemMesh()
		# nodes
		#print ("Add nodes")
		for id in NodeList: # node
			#femmesh.addNode(NodeList[id].x,NodeList[id].y,NodeList[id].z, int(id)+1 )
			femmesh.addNode(NodeList[id].x,NodeList[id].y,NodeList[id].z, int(id) )
				
		for id in MemberList:
        
			mtype = MemberList[id].mtype
				
			if mtype == 'CROD':
            
				n1 = int(MemberList[id].n1)
				n2 = int(MemberList[id].n2)
				femmesh.addEdge([n1, n2])
				
			elif mtype == 'CBAR':
            
				n1 = int(MemberList[id].n1)
				n2 = int(MemberList[id].n2)
				femmesh.addEdge([n1, n2])
				
			elif mtype == 'CBEAM':
            
				n1 = int(MemberList[id].n1)
				n2 = int(MemberList[id].n2)
				femmesh.addEdge([n1, n2])
				

			
			elif mtype =='CTRIA3':
				n1=int(MemberList[id].n1)
				n2=int(MemberList[id].n2)
				n3=int(MemberList[id].n3)
				
				femmesh.addEdge([n1, n2])
				femmesh.addEdge([n2, n3])
				femmesh.addEdge([n3, n1])

				#femmesh.addFace([n1,n2,n3])
				
			elif mtype == 'CQUAD4':
				n1 = int(MemberList[id].n1)
				n2 = int(MemberList[id].n2)
				n3 = int(MemberList[id].n3)
				n4 = int(MemberList[id].n4)
				
				#print (str(n1)+" "+str(n2)+" "+str(n3)+" "+str(n4))
                
				femmesh.addEdge([n1, n2])
				femmesh.addEdge([n2, n3])
				femmesh.addEdge([n3, n4])
				femmesh.addEdge([n4, n1])

				#femmesh.addFace([n1,n2,n3,n4])
                
			elif mtype == 'CQUAD8':
				n1 = int(MemberList[id].n1)
				n2 = int(MemberList[id].n2)
				n3 = int(MemberList[id].n3)
				n4 = int(MemberList[id].n4)
                
				femmesh.addEdge([n1, n2])
				femmesh.addEdge([n2, n3])
				femmesh.addEdge([n3, n4])
				femmesh.addEdge([n4, n1])
				
				#femmesh.addFace([n1,n2,n3,n4])
				
			elif mtype =='CTETRA':
				n1=int(MemberList[id].n1)
				n2=int(MemberList[id].n2)
				n3=int(MemberList[id].n3)
				n4=int(MemberList[id].n4)
				
				femmesh.addEdge([n1, n2])
				femmesh.addEdge([n2, n3])
				femmesh.addEdge([n3, n4])
				femmesh.addEdge([n4, n1])

				#femmesh.addVolume([n1,n2,n3,n4])

			elif mtype =='CHEXA':
				n1=int(MemberList[id].n1)
				n2=int(MemberList[id].n2)
				n3=int(MemberList[id].n3)
				n4=int(MemberList[id].n4)

				n5=int(MemberList[id].n5)
				n6=int(MemberList[id].n6)
				n7=int(MemberList[id].n7)
				n8=int(MemberList[id].n8)
				
				femmesh.addEdge([n1, n2])
				femmesh.addEdge([n2, n3])
				femmesh.addEdge([n3, n4])
				femmesh.addEdge([n4, n1])

				femmesh.addEdge([n5, n6])
				femmesh.addEdge([n6, n7])
				femmesh.addEdge([n7, n8])
				femmesh.addEdge([n8, n5])
				
				femmesh.addEdge([n1, n5])
				femmesh.addEdge([n2, n6])
				femmesh.addEdge([n3, n7])
				femmesh.addEdge([n4, n8])

				#femmesh.addVolume([n1,n2,n3,n4,n5,n6,n7,n8])
				
			else:
				print (mtype+' Not supported yet')
					
					
		result_mesh_object = None
		result_mesh_object = ObjectsFem.makeMeshResult(
			FreeCAD.ActiveDocument,
			"hfcMesh"
		)
		result_mesh_object.FemMesh = femmesh

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.activeDocument().activeView().viewAxonometric()
		FreeCADGui.SendMsgToActiveView("ViewFit")
		
		print ('Input done.')
		print ('')
		

FreeCADGui.addCommand('hfcMystranDatInFemWire',hfcMystranDatInFemWire())