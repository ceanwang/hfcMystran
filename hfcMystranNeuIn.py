import FreeCAD,FreeCADGui
import FreeCAD,FreeCADGui
import Fem
import os

import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *

class Node:
    def __init__(self, id , x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.id = str(id)

# elmnt n1     n2    Ax     Asy     Asz     Jx     Iy     Iz     E     G     roll  density
class Member:
    def __init__(self, id , n1,n2):
        self.n1 = n1
        self.n2 = n2
        self.id = str(id)
       
        
class MemberCROD:
    def __init__(self, id , n1,n2,mtype):
        self.n1 = n1
        self.n2 = n2
        #self. = 
        self.mtype=mtype
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
    def __init__(self, id , xdsp,ydsp,zdsp,xrot,yrot,zrot):
        self.xdsp = xdsp
        self.ydsp = ydsp
        self.zdsp = zdsp
        self.xrot = xrot
        self.yrot = yrot
        self.zrot = zrot
        self.id = str(id)

def SeekNextSec(fp,tStr):	
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
			
class hfcMystranNeuIn:
	"Mystran result object"
	def GetResources(self):
		return {"MenuText": "neu In",
				"Accel": "Ctrl+t",
				"ToolTip": "Input result neu file",
				"Pixmap": os.path.dirname(__file__)+"./resources/neu.svg"
		}

	def IsActive(self):

		if FreeCAD.ActiveDocument == None:
			return False
		else:
			return True

	def Activated(self):
		import feminout.importToolsFem as toolsFem
		import ObjectsFem
		
		numNode=0
		numMember=0
        
		analysis=None

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
				filename = QFileDialog.getOpenFileName(None,QString.fromLocal8Bit("Read a Mystarn's neu file"),path, "*.neu") # PyQt4
			except Exception:
				filename, Filter = PySide.QtGui.QFileDialog.getOpenFileName(None, "Read a Mystran's neu file", path, "*.neu") #PySide
				
			data=filename.split("/")
			n=len(data)
			path=""
			for i in range(n-1):
				path=path+data[i]+"/"

			fn=data[n-1].split('.')
			filenameDat=path+fn[0]+'.dat'
			
			inifileOut = FreeCAD.getHomePath()+ininame
			iniFout = open(inifileOut,"w")
			iniFout.writelines(path)
			iniFout.close()

		else:	
			path=iHfc.DatPath
			filenameDat=iHfc.DatFile
			filename=filenameDat[:len(filenameDat)-3]+'neu'
			

		print ("Result: "+filename)
		#print (path)
		
		#fNameDat = path+'hfcMystran.dat'
		
		
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
        
		mode_disp_id=[]
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
		
		fpDat = open(filenameDat)
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
            
            #GRID        3004           0.750   0.500   0.000             126
			if data[0]=='GRID':
				#Fixed format  
				#           id          cp  x1
                #GRID       10101       0   0.000   0.000   0.000       0
				is8Byte=1
				if is8Byte==1:
					tid=aline[8:16].strip()
					#cp=aline[17:24].strip()
					x=aline[24:32].strip()
					y=aline[32:40].strip()
					z=aline[40:48].strip()
					
					NodeList[tid] = Node(tid, float(x), float(y), float(z))
				
				elif len(aline)==48:              
					tid=aline[6:24].strip()              
					#print (tid)  
                    
                    #x        
					datax=aline[25:32].strip()      #56-41=15 
					if len(datax)==15:
						dataf=datax[1:12]
						datab=datax[13:15]
						x=dataf+'E'+datab      #56-41=15 
					else:
						x=datax      #56-41=15 
					#print (x)  
                    
                    #y
					datay=aline[33:40].strip()      #56-41=15 
					if len(datay)==15:
						dataf=datay[1:12]
						datab=datay[13:15]
						y=dataf+'E'+datab      #56-41=15 
					else:
						y=datax      #56-41=15 

					#print (y) 
					
					#z
					dataz=aline[40:48].strip()      #56-41=15 
					#print (dataz)
					tsign=dataz[len(dataz)-2]
					#print (tsign) 					
					if tsign=='-': 
						dataf=dataz[:len(dataz)-1-1]
						datab=dataz[len(dataz)-1-1:]
						z=dataf+'E'+datab      #56-41=15 
					else:
						z=dataz      #56-41=15 
                    
					#print (str(id)+" "+str(x)+" "+str(y)+" "+str(z))
					NodeList[tid] =  Node(tid, float(x) ,float(y) , float( z) )
				else:	
					#NodeList[data[1].strip()] =  Node(data[1].strip(), float(data[2].strip()), float(data[3].strip()), float(data[4].strip()))
					print ('Grid')
				numNode=numNode+1                
                
			#GRID*    1                               0.00000E+00     0.00000E+00
			if data[0]=='GRID*':
				NodeList[data[1]] =  Node(data[1], float(data[2]) ,float( data[3]) , 0.0 )
				numNode=numNode+1                



			# Member 333333333333333333333333333333333333333	
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
			
		femmesh = Fem.FemMesh()
		# nodes
		#print ("Add nodes")
		for id in NodeList: # node
			#femmesh.addNode(NodeList[id].x,NodeList[id].y,NodeList[id].z, int(id)+1 )
			femmesh.addNode(NodeList[id].x,NodeList[id].y,NodeList[id].z, int(id) )
				
		# elements
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
				
				femmesh.addFace([n1,n2,n3])
				
			elif mtype == 'CQUAD4':
				n1 = int(MemberList[id].n1)
				n2 = int(MemberList[id].n2)
				n3 = int(MemberList[id].n3)
				n4 = int(MemberList[id].n4)
				
				#print (str(n1)+" "+str(n2)+" "+str(n3)+" "+str(n4))
                
				femmesh.addFace([n1,n2,n3,n4])
                
			elif mtype == 'CQUAD8':
				n1 = int(MemberList[id].n1)
				n2 = int(MemberList[id].n2)
				n3 = int(MemberList[id].n3)
				n4 = int(MemberList[id].n4)
                
				femmesh.addFace([n1,n2,n3,n4])
				
			elif mtype =='CTETRA':
				n1=int(MemberList[id].n1)
				n2=int(MemberList[id].n2)
				n3=int(MemberList[id].n3)
				n4=int(MemberList[id].n4)

				femmesh.addVolume([n1,n2,n3,n4])

			elif mtype =='CHEXA':
				n1=int(MemberList[id].n1)
				n2=int(MemberList[id].n2)
				n3=int(MemberList[id].n3)
				n4=int(MemberList[id].n4)

				n5=int(MemberList[id].n5)
				n6=int(MemberList[id].n6)
				n7=int(MemberList[id].n7)
				n8=int(MemberList[id].n8)
				
				femmesh.addVolume([n1,n2,n3,n4,n5,n6,n7,n8])
				
			else:
				print (mtype+' Not supported yet')
					
					
		result_mesh_object = None
		result_mesh_object = ObjectsFem.makeMeshResult(
			FreeCAD.ActiveDocument,
			"ResultMesh"
		)
		result_mesh_object.FemMesh = femmesh
		res_mesh_is_compacted = False
		nodenumbers_for_compacted_mesh = []
		
		#femResult = Fem.FemResultObject()
        #--------------------------------------		
		fp = open(filename)
		tline=[]
		for line in fp:
			aline=line.strip()	
			if len(aline)==0 or aline[0]=='$':
				continue
			else:		
				tline.append(line.strip())
		fp.close()

		tStrDis1="T1  translation"
		tStrDis2="T2  translation"
		tStrDis3="T3  translation"
		for i in range(len(tline)):
			if tline[i].strip() == tStrDis1:
                #T1  translation        
                #     0.000000E+00,     1.800000E-04,     1.800000E-04,
                #   10002,       0,       0,       0,       0,       0,       0,       0,       0,       0,
                #       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,
                #       1,       7,       1,       7,
                #       1,       1,       1
				i=i+6
				for id in range(numNode): # node
                
					#print (tline[i])
                    #1,     0.000000E+00,
					dataNode = tline[i].split(",")
					#print (dataNode[0]+" "+str(numNode))
					mode_disp_id.append( int(dataNode[0]))
					mode_disp_x.append( float(dataNode[1]))
					i=i+1

			if tline[i].strip() == tStrDis2:
                #T1  translation        
                #     0.000000E+00,     1.800000E-04,     1.800000E-04,
                #   10002,       0,       0,       0,       0,       0,       0,       0,       0,       0,
                #       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,
                #       1,       7,       1,       7,
                #       1,       1,       1
				i=i+6
				for id in range(numNode): # node
                
					#print (tline[i])
                    #1,     0.000000E+00,
					dataNode = tline[i].split(",")
					#print (dataNode[0]+" "+str(numNode))
					mode_disp_y.append(float(dataNode[1]))
					i=i+1

			if tline[i].strip() == tStrDis3:
                #T1  translation        
                #     0.000000E+00,     1.800000E-04,     1.800000E-04,
                #   10002,       0,       0,       0,       0,       0,       0,       0,       0,       0,
                #       0,       0,       0,       0,       0,       0,       0,       0,       0,       0,
                #       1,       7,       1,       7,
                #       1,       1,       1
				i=i+6
				for id in range(numNode): # node
                
					#print (tline[i])
                    #1,     0.000000E+00,
					dataNode = tline[i].split(",")
					#print (dataNode[0]+" "+str(numNode))
					mode_disp_z.append( float(dataNode[1]))
					i=i+1

		for id in range(numNode): # node
			#print (str(id)+" "+str(mode_disp_x[id])+" "+ str(mode_disp_y[id])+" "+str(mode_disp_z[id]))
			mode_disp[mode_disp_id[id]] = FreeCAD.Vector(mode_disp_x[id], mode_disp_y[id], mode_disp_z[id])
					
		#mode_results["disp"+str(nDisp)] = mode_disp
		mode_results["disp"] = mode_disp
		mode_disp = {}

		#nDisp+=1	
					
		res_obj=[]		
		iLC=0
		results_name="Displacement"
		# append mode_results to results and reset mode_result
		results.append(mode_results)
		mode_results = {}
        
        
		for result_set in results:
			res_obj.append(ObjectsFem.makeResultMechanical(FreeCAD.ActiveDocument, results_name+str(iLC)))
						
			res_obj[iLC].Mesh = result_mesh_object
			#res_obj[iLC] = importToolsFem.fill_femresult_mechanical(res_obj[iLC], result_set)
			res_obj[iLC] = toolsFem.fill_femresult_mechanical(res_obj[iLC], result_set)

			# complementary result object calculations
			import femresult.resulttools as restools
			import femtools.femutils as femutils

			# fill DisplacementLengths
			res_obj[iLC] = restools.add_disp_apps(res_obj[iLC])
			# fill StressValues
			res_obj[iLC] = restools.add_von_mises(res_obj[iLC])
			if res_obj[iLC].getParentGroup():
				has_reinforced_mat = False
				for obj in res_obj[iLC].getParentGroup().Group:
					if obj.isDerivedFrom("App::MaterialObjectPython") \
							and femutils.is_of_type(obj, "Fem::MaterialReinforced"):
						has_reinforced_mat = True
						restools.add_principal_stress_reinforced(res_obj[iLC])
						break
				if has_reinforced_mat is False:
					# fill PrincipalMax, PrincipalMed, PrincipalMin, MaxShear
					res_obj[iLC] = restools.add_principal_stress_std(res_obj[iLC])
			else:
				# if a pure Frame3DD file was opened no analysis and thus no parent group
				# fill PrincipalMax, PrincipalMed, PrincipalMin, MaxShear
				res_obj[iLC] = restools.add_principal_stress_std(res_obj[iLC])
			# fill Stats
			res_obj[iLC] = restools.fill_femresult_stats(res_obj[iLC])
			#res_obj[iLC].ViewObject.DisplayMode = 'Uabs'
			

		FreeCAD.ActiveDocument.recompute()
		FreeCADGui.activeDocument().activeView().viewAxonometric()
		FreeCADGui.SendMsgToActiveView("ViewFit")
		
		

FreeCADGui.addCommand('hfcMystranNeuIn',hfcMystranNeuIn())