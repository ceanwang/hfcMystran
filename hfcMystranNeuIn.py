# ***************************************************************************
# *                                                                         *
# *   Copyright (c) 2024 - <ceanwang@gmail.com>                             *
# *                                                                         *
# *   License: GPL3.0 + Not for commercial use                              *
# *                                                                         *
# ***************************************************************************

__Title__ = "hfcMystran"
__Author__ = "CeanWang"
__Url__ = "https://github.com/ceanwang/hfcMystran"
__Version__ = "0.1.0"
__Date__ = "2024/04/12"
__Comment__ = "Added stress input"
__Forum__ = ""
__Status__ = "initial development"
__Requires__ = "freecad version 0.2 or higher"
__Communication__ = ""

import FreeCAD,FreeCADGui
import Fem
import os
import sys

import ObjectsFem
import feminout.importToolsFem as toolsFem

import PySide
from PySide import QtGui ,QtCore
from PySide.QtGui import *
from PySide.QtCore import *
from femtaskpanels import task_result_mechanical as trm
#import hfc_task_result_mechanical as trm

if open.__module__ == "io":
    # because we'll redefine open below (Python3)
    pyopen = open


def open(filename):
    "called when freecad opens a file"
    docname = os.path.splitext(os.path.basename(filename))[0]
    insert(filename, docname)


def insert(filename, docname):
    "called when freecad wants to import a file"
    try:
        doc = FreeCAD.getDocument(docname)
    except NameError:
        doc = FreeCAD.newDocument(docname)
    FreeCAD.ActiveDocument = doc
    import_neu(filename)


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
    #def __init__(self):
    #    import hfc_task_result_mechanical
    #    sys.modules["femtaskpanels.task_result_mechanical"] = sys.modules[hfc_task_result_mechanical.__name__]
    
    
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
        iHfc =FreeCAD.ActiveDocument.getObject('hfc')
        if iHfc==None:
            ininame="Mod/hfcMystran/hfcMystran.ini"
            
            inifile = FreeCAD.getHomePath()+ininame
            if os.path.exists(inifile): 
                iniF = pyopen(inifile,"r")
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
            iniFout = pyopen(inifileOut,"w")
            iniFout.writelines(path)
            iniFout.close()

        else:   
            path=iHfc.DatPath
            isWireframe=int(iHfc.isWireframe)
            isTop=int(iHfc.isTop)
            filenameDat=iHfc.DatFile
            filename=filenameDat[:len(filenameDat)-3]+'neu'
            
            import_neu(filename, filenameDat)


def import_neu(filename, filenameDat=None):

        isWireframe=0
        isTop=1
        
        iHfc =FreeCAD.ActiveDocument.getObject('hfc')
        if iHfc!=None:
            isWireframe=int(iHfc.isWireframe)
            isTop=int(iHfc.isTop)
        
        if filenameDat is None:
            filenameDat=filename[:len(filename)-3]+'bdf'
        print ("Result: "+filename)
        print ("Result: "+filenameDat)

        analysis=None

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
        
        #rb_vm_stress
        mode_stress = {}
        
        #rb_max_shear_stress
        mode_strain = {}
        
        
        
        #rb_peeq
        #mode_peeq = {}
        #rb_temperature
        #mode_temp = {}
        #rb_massflowrate
        #mode_massflow = {}
        #rb_networkpressure
        #mode_networkpressure = {}
        
        
        mstress = []
        prinstress1 = []
        prinstress2 = []
        prinstress3 = []
        shearstress = []

        nodeCount={}
        mstressNode = {}
        prinstress1Node = {}
        prinstress2Node = {}
        prinstress3Node = {}
        shearstressNode = {}
        
        iFilled=[]
        
        mode_disp_id=[]
        
        mode_disp_x=[]
        mode_disp_y=[]
        mode_disp_z=[]
        
        mode_disp_R = []
        mode_disp_Rx=[]
        mode_disp_Ry=[]
        mode_disp_Rz=[]


        nDisp=0
        mDisp=0

        gidL=0
        
        #factor = 25.42
        factor = 1
        
        factorZoom = 100

        isDebug=1
        #000000000000000000000000000000000000000000000000000000000000000000
        
        fpDat = pyopen(filenameDat)
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
                numMember+=1
                if numMember==1 and float(data[1])!=1: 
                    gidL=1
                if gidL==1:    
                    MemberList[str(numMember).strip()] =  MemberCTRIA3(data[1].strip(), data[3] ,data[4] , data[5] ,data[0].strip())  
                else:
                    MemberList[data[1].strip()] =  MemberCTRIA3(data[1].strip(), data[3] ,data[4] , data[5] ,data[0].strip())  

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
                
                if isWireframe==0:
                    femmesh.addFace([n1,n2,n3])
                else:
                    femmesh.addEdge([n1, n2])
                    femmesh.addEdge([n2, n3])
                    femmesh.addEdge([n3, n1])
                
            elif mtype == 'CQUAD4':
                n1 = int(MemberList[id].n1)
                n2 = int(MemberList[id].n2)
                n3 = int(MemberList[id].n3)
                n4 = int(MemberList[id].n4)
                
                #print (str(n1)+" "+str(n2)+" "+str(n3)+" "+str(n4))
                
                if isWireframe==0:
                    femmesh.addFace([n1,n2,n3,n4])
                else:
                    femmesh.addEdge([n1, n2])
                    femmesh.addEdge([n2, n3])
                    femmesh.addEdge([n3, n4])
                    femmesh.addEdge([n4, n1])
                
            elif mtype == 'CQUAD8':
                n1 = int(MemberList[id].n1)
                n2 = int(MemberList[id].n2)
                n3 = int(MemberList[id].n3)
                n4 = int(MemberList[id].n4)
                
                if isWireframe==0:
                    femmesh.addFace([n1,n2,n3,n4])
                else:
                    femmesh.addEdge([n1, n2])
                    femmesh.addEdge([n2, n3])
                    femmesh.addEdge([n3, n4])
                    femmesh.addEdge([n4, n1])
                
            elif mtype =='CTETRA':
                n1=int(MemberList[id].n1)
                n2=int(MemberList[id].n2)
                n3=int(MemberList[id].n3)
                n4=int(MemberList[id].n4)

                if isWireframe==0:
                    femmesh.addVolume([n1,n2,n3,n4])
                else:
                    femmesh.addEdge([n1, n2])
                    femmesh.addEdge([n2, n3])
                    femmesh.addEdge([n3, n4])
                    femmesh.addEdge([n4, n1])

            elif mtype =='CHEXA':
                n1=int(MemberList[id].n1)
                n2=int(MemberList[id].n2)
                n3=int(MemberList[id].n3)
                n4=int(MemberList[id].n4)

                n5=int(MemberList[id].n5)
                n6=int(MemberList[id].n6)
                n7=int(MemberList[id].n7)
                n8=int(MemberList[id].n8)
                
                if isWireframe==0:
                    femmesh.addVolume([n1,n2,n3,n4,n5,n6,n7,n8])
                else:
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
        fp = pyopen(filename)
        tline=[]
        for line in fp:
            aline=line.strip()  
            if len(aline)==0 or aline[0]=='$':
                continue
            else:       
                tline.append(line.strip())
        fp.close()

        #RSS SPC force
        #T1  SPC force
        #RSS SPC moment 
        #R1  SPC moment

        tStrDisT="RSS translation"        
        tStrDisT1="T1  translation"
        tStrDisT2="T2  translation"
        tStrDisT3="T3  translation"
        tStrDisR="RSS rotation"           
        tStrDisR1="R1  rotation"
        tStrDisR2="R2  rotation"
        tStrDisR3="R3  rotation"
        #--------------------------
        #TRIA3
        #--------------------------
        #TRIA3 Top X Direct Stress 
        #TRIA3 Top Y Direct Stress 
        #TRIA3 Top XY Shear Stress
        
        #TRIA3 Top Maj Prn Stress  
        tTRIA3TMajPrn="TRIA3 Top Maj Prn Stress"        
        tTRIA3BMajPrn="TRIA3 Bot Maj Prn Stress"        

        #TRIA3 Top Min Prn Stress   
        tTRIA3TMinPrn="TRIA3 Top Min Prn Stress"
        tTRIA3BMinPrn="TRIA3 Bot Min Prn Stress"
        
        #TRIA3 Top Prn Str Angle     
        
        #TRIA3 Top Mean Stress  
        tTRIA3TMean="TRIA3 Top Mean Stress"
        tTRIA3BMean="TRIA3 Bot Mean Stress"
        
        #TRIA3 Top Max Shear Stress  
        tTRIA3TMaxShear="TRIA3 Top Max Shear Stress"
        tTRIA3BMaxShear="TRIA3 Bot Max Shear Stress"
        
        #TRIA3 Top Von Mises Stress
        tTRIA3TVonMises="TRIA3 Top Von Mises Stress"
        tTRIA3BVonMises="TRIA3 Bot Von Mises Stress"
        
        #TRIA3 Top XZ Shear Stress      
        #TRIA3 Top YZ Shear Stress      
        
        #--------------------------
        #QUAD4
        #--------------------------
        #QUAD4 Top X Direct Stress 
        #QUAD4 Top Y Direct Stress 
        #QUAD4 Top XY Shear Stress 
        
        tQUAD4TMajPrn="QUAD4 Top Maj Prn Stress"
        tQUAD4BMajPrn="QUAD4 Bot Maj Prn Stress"

        tQUAD4TMinPrn="QUAD4 Top Min Prn Stress"  
        tQUAD4BMinPrn="QUAD4 Bot Min Prn Stress"  

        #QUAD4 Top Prn Str Angle         

        tQUAD4TMean="QUAD4 Top Mean Stress"  
        tQUAD4BMean="QUAD4 Bot Mean Stress"  
        
        tQUAD4TMaxShear="QUAD4 Top Max Shear Stress"     
        tQUAD4BMaxShear="QUAD4 Bot Max Shear Stress"     
        
        tQUAD4TVonMises="QUAD4 Top Von Mises Stress"  
        tQUAD4BVonMises="QUAD4 Bot Von Mises Stress"  

        #QUAD4 Top XZ Shear Stress    
        #QUAD4 Top YZ Shear Stress       

        #--------------------------
        #TETRA4 
        #--------------------------
        #TETRA4 X Direct Stress          
        #TETRA4 Y Direct Stress          
        #TETRA4 Z Direct Stress          
        
        #TETRA4 XY Shear Stress          
        tTETRA4XY="TETRA4 XY Shear Stress"
        #TETRA4 YZ Shear Stress          
        tTETRA4YZ="TETRA4 YZ Shear Stress"
        #TETRA4 ZX Shear Stress          
        tTETRA4ZX="TETRA4 ZX Shear Stress"
        
        #TETRA4 Prin Stress-1            
        tTETRA4Prn1="TETRA4 Prin Stress-1"
        
        #TETRA4 Prin Stress-2            
        tTETRA4Prn2="TETRA4 Prin Stress-2"
        
        #TETRA4 Prin Stress-3            
        tTETRA4Prn3="TETRA4 Prin Stress-3"
        
        #TETRA4 Mean Stress     
        tTETRA4Mean="TETRA4 Mean Stress"
        
        #TETRA4 von Mises Stress      
        tTETRA4VonMises="TETRA4 von Mises Stress"
        #TETRA4   (null field)           

        
        for i in range(len(tline)):
            #print (tline[i].strip())
            if tline[i].strip() == tStrDisT1:
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

            if tline[i].strip() == tStrDisT2:
                #T1  translation        
                i=i+6
                for id in range(numNode): # node
                
                    #print (tline[i])
                    #1,     0.000000E+00,
                    dataNode = tline[i].split(",")
                    #print (dataNode[0]+" "+str(numNode))
                    mode_disp_y.append(float(dataNode[1]))
                    i=i+1

            if tline[i].strip() == tStrDisT3:
                #T1  translation        
                i=i+6
                for id in range(numNode): # node
                    dataNode = tline[i].split(",")
                    #print (dataNode[0]+" "+str(numNode))
                    mode_disp_z.append( float(dataNode[1]))
                    i=i+1

            if tline[i].strip() == tStrDisR:
                #RSS  rotation           
                i=i+6
                for id in range(numNode): # node
                    dataNode = tline[i].split(",")
                    #print (dataNode[0]+" "+str(numNode))
                    mode_disp_R.append( float(dataNode[1]))
                    i=i+1
                    
            if tline[i].strip() == tStrDisR1:
                #R1  rotation           
                i=i+6
                for id in range(numNode): # node
                    dataNode = tline[i].split(",")
                    #print (dataNode[0]+" "+str(numNode))
                    mode_disp_Rx.append( float(dataNode[1]))
                    i=i+1
                    
            if tline[i].strip() == tStrDisR2:
                #R2  rotation           
                i=i+6
                for id in range(numNode): # node
                    dataNode = tline[i].split(",")
                    #print (dataNode[0]+" "+str(numNode))
                    mode_disp_Ry.append( float(dataNode[1]))
                    i=i+1
                    
            if tline[i].strip() == tStrDisR3:
                #R3  rotation           
                i=i+6
                for id in range(numNode): # node
                    dataNode = tline[i].split(",")
                    #print (dataNode[0]+" "+str(numNode))
                    mode_disp_Rz.append( float(dataNode[1]))
                    i=i+1
            #--------------------------
            #QUAD4 & TRIA3
            #--------------------------
            #Top 
            #
            if isTop==1: 
                if tline[i].strip() == tTRIA3TMajPrn or tline[i].strip() == tQUAD4TMajPrn:
                    #"Top Maj Prn Stress"
                    print ("Top Maj Prn Stress") 
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        #print (dataNode[0]+" "+str(numMember))
                        #print (dataNode[1])
                        prinstress1.append( float(dataNode[1]))
                        i=i+1
                        
                if tline[i].strip() == tTRIA3TMean or tline[i].strip() == tQUAD4TMean :
                    #QUAD4 Top Mean Stress"
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        prinstress2.append( float(dataNode[1]))
                        i=i+1
                        
                if tline[i].strip() == tTRIA3TMinPrn or tline[i].strip() == tQUAD4TMinPrn:
                    #QUAD4 Top Min Prn Stress"
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        prinstress3.append( float(dataNode[1]))
                        i=i+1
                        
                if tline[i].strip() == tTRIA3TVonMises or tline[i].strip() == tQUAD4TVonMises:
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        mstress.append( float(dataNode[1]))
                        i=i+1

                if tline[i].strip() == tTRIA3TMaxShear or tline[i].strip() == tQUAD4TMaxShear:
                    #QUAD4 Top Max Shear Stress"
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        shearstress.append( float(dataNode[1]))
                        i=i+1
            #       
            #Bottom       
            #              
            else: 
                if tline[i].strip() == tTRIA3BMajPrn or tline[i].strip() == tQUAD4BMajPrn:
                    #QUAD4 Bot Maj Prn Stress"
                    print ("QUAD4 Bot Maj Prn Stress")
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        #print (dataNode[0]+" "+str(numMember))
                        #print (dataNode[1])
                        prinstress1.append( float(dataNode[1]))
                        i=i+1
                        
                if tline[i].strip() == tTRIA3BMean or tline[i].strip() == tQUAD4BMean:
                    #QUAD4 Top Mean Stress"
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        prinstress2.append( float(dataNode[1]))
                        i=i+1
                        
                if tline[i].strip() == tTRIA3BMinPrn or tline[i].strip() == tQUAD4BMinPrn:
                    #QUAD4 Top Min Prn Stress"
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        prinstress3.append( float(dataNode[1]))
                        i=i+1
                        
                if tline[i].strip() == tTRIA3BVonMises or tline[i].strip() == tQUAD4BVonMises:
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        mstress.append( float(dataNode[1]))
                        i=i+1

                if tline[i].strip() == tTRIA3BMaxShear or tline[i].strip() == tQUAD4BMaxShear:
                    #QUAD4 Top Max Shear Stress"
                    i=i+6
                    for id in range(numMember): # node
                        dataNode = tline[i].split(",")
                        shearstress.append( float(dataNode[1]))
                        i=i+1
                    
            #--------------------------
            #TETRA4
            #--------------------------
            #tTETRA4XY="TETRA4 XY Shear Stress"
            #tTETRA4Prn1="TETRA4 Prin Stress-1"
            #tTETRA4Prn2="TETRA4 Prin Stress-2"
            #tTETRA4Prn3="TETRA4 Prin Stress-3"
            #tTETRA4Mean="TETRA4 Mean Stress"
            #tTETRA4VonMises="TETRA4 von Mises Stress"
            
            if tline[i].strip() == tTETRA4Prn1:
                i=i+6
                print (tTETRA4Prn1)
                for id in range(numMember): # node
                    dataNode = tline[i].split(",")
                    #print (dataNode[0]+" "+str(numMember))
                    #print (dataNode[1])
                    prinstress1.append( float(dataNode[1]))
                    i=i+1
                    
            if tline[i].strip() == tTETRA4Prn3:
                i=i+6
                print (tTETRA4Prn3)
                for id in range(numMember): # node
                    dataNode = tline[i].split(",")
                    #print (dataNode[0]+" "+str(numMember))
                    #print (dataNode[1])
                    prinstress3.append( float(dataNode[1]))
                    i=i+1
                    
            if tline[i].strip() == tTETRA4Mean:
                i=i+6
                print (tTETRA4Mean)
                for id in range(numMember): # node
                    dataNode = tline[i].split(",")
                    prinstress2.append( float(dataNode[1]))
                    i=i+1
                    
            if tline[i].strip() == tTETRA4VonMises:
                i=i+6
                print (tTETRA4VonMises)
                for id in range(numMember): # node
                    dataNode = tline[i].split(",")
                    mstress.append( float(dataNode[1]))
                    #mstress.append(calculate_von_mises((Sxx, Syy, Szz, Sxy, Sxz, Syz)))
                    i=i+1
                    
            if tline[i].strip() == tTETRA4XY:
                i=i+6
                print (tTETRA4XY)
                for id in range(numMember): # node
                    dataNode = tline[i].split(",")
                    shearstress.append( float(dataNode[1]))
                    i=i+1


        isOne=2
        #init
        for id in range(numNode): # node
            tN=int(id)
            #print (tN)
            nodeCount[tN]=0
            shearstressNode[tN]=0
            mstressNode[tN]=0
            prinstress1Node[tN]=0
            prinstress2Node[tN]=0
            prinstress3Node[tN]=0
            
        #find node stress
        for id in MemberList: # node
            tN=int(id)-1
            #print (tN)
            if MemberList[id].mtype =='CTRIA3':
                #MemberCQUAD4(data[1].strip(), data[3], data[4], data[5], data[6], data[0].strip())  
                n1=int(MemberList[id].n1)-1
                n2=int(MemberList[id].n2)-1
                n3=int(MemberList[id].n3)-1
                #print (str(tN)+' '+str(n1)+' '+str(n2)+' '+str(n3))
                
                if isOne==1: 
                    shearstressNode[n1]=shearstress[tN]
                    shearstressNode[n2]=shearstress[tN]
                    shearstressNode[n3]=shearstress[tN]
                    
                    mstressNode[n1]=mstress[tN]
                    mstressNode[n2]=mstress[tN]
                    mstressNode[n3]=mstress[tN]
                    
                    prinstress1Node[n1]=prinstress1[tN]
                    prinstress1Node[n2]=prinstress1[tN]
                    prinstress1Node[n3]=prinstress1[tN]
                    
                    prinstress2Node[n1]=prinstress2[tN]
                    prinstress2Node[n2]=prinstress2[tN]
                    prinstress2Node[n3]=prinstress2[tN]
                    
                    prinstress3Node[n1]=prinstress3[tN]
                    prinstress3Node[n2]=prinstress3[tN]
                    prinstress3Node[n3]=prinstress3[tN]
                else:
                    nodeCount[n1]=nodeCount[n1]+1
                    nodeCount[n2]=nodeCount[n2]+1
                    nodeCount[n3]=nodeCount[n3]+1
                    
                    #print (shearstress[tN])
                    shearstressNode[n1]=shearstressNode[n1]+shearstress[tN]
                    shearstressNode[n2]=shearstressNode[n2]+shearstress[tN]
                    shearstressNode[n3]=shearstressNode[n3]+shearstress[tN]
                    
                    mstressNode[n1]=mstressNode[n1]+mstress[tN]
                    mstressNode[n2]=mstressNode[n2]+mstress[tN]
                    mstressNode[n3]=mstressNode[n3]+mstress[tN]
                    
                    prinstress1Node[n1]=prinstress1Node[n1]+prinstress1[tN]
                    prinstress1Node[n2]=prinstress1Node[n2]+prinstress1[tN]
                    prinstress1Node[n3]=prinstress1Node[n3]+prinstress1[tN]
                    
                    prinstress2Node[n1]=prinstress2Node[n1]+prinstress2[tN]
                    prinstress2Node[n2]=prinstress2Node[n2]+prinstress2[tN]
                    prinstress2Node[n3]=prinstress2Node[n3]+prinstress2[tN]
                    
                    prinstress3Node[n1]=prinstress3Node[n1]+prinstress3[tN]
                    prinstress3Node[n2]=prinstress3Node[n2]+prinstress3[tN]
                    prinstress3Node[n3]=prinstress3Node[n3]+prinstress3[tN]
                    
            elif MemberList[id].mtype =='CQUAD4':
            
                #MemberCQUAD4(data[1].strip(), data[3], data[4], data[5], data[6], data[0].strip())  
                n1=int(MemberList[id].n1)-1
                n2=int(MemberList[id].n2)-1
                n3=int(MemberList[id].n3)-1
                n4=int(MemberList[id].n4)-1
                #print (str(tN)+' '+str(n1)+' '+str(n2)+' '+str(n3)+' '+str(n4))
                
                if isOne==1: 
                    shearstressNode[n1]=shearstress[tN]
                    shearstressNode[n2]=shearstress[tN]
                    shearstressNode[n3]=shearstress[tN]
                    shearstressNode[n4]=shearstress[tN]
                    
                    mstressNode[n1]=mstress[tN]
                    mstressNode[n2]=mstress[tN]
                    mstressNode[n3]=mstress[tN]
                    mstressNode[n4]=mstress[tN]
                    
                    prinstress1Node[n1]=prinstress1[tN]
                    prinstress1Node[n2]=prinstress1[tN]
                    prinstress1Node[n3]=prinstress1[tN]
                    prinstress1Node[n4]=prinstress1[tN]
                    
                    prinstress2Node[n1]=prinstress2[tN]
                    prinstress2Node[n2]=prinstress2[tN]
                    prinstress2Node[n3]=prinstress2[tN]
                    prinstress2Node[n4]=prinstress2[tN]
                    
                    prinstress3Node[n1]=prinstress3[tN]
                    prinstress3Node[n2]=prinstress3[tN]
                    prinstress3Node[n3]=prinstress3[tN]
                    prinstress3Node[n4]=prinstress3[tN]
                else:
                    nodeCount[n1]=nodeCount[n1]+1
                    nodeCount[n2]=nodeCount[n2]+1
                    nodeCount[n3]=nodeCount[n3]+1
                    nodeCount[n4]=nodeCount[n4]+1
                    
                    #print (shearstress[tN])
                    shearstressNode[n1]=shearstressNode[n1]+shearstress[tN]
                    shearstressNode[n2]=shearstressNode[n2]+shearstress[tN]
                    shearstressNode[n3]=shearstressNode[n3]+shearstress[tN]
                    shearstressNode[n4]=shearstressNode[n4]+shearstress[tN]
                    
                    mstressNode[n1]=mstressNode[n1]+mstress[tN]
                    mstressNode[n2]=mstressNode[n2]+mstress[tN]
                    mstressNode[n3]=mstressNode[n3]+mstress[tN]
                    mstressNode[n4]=mstressNode[n4]+mstress[tN]
                    
                    prinstress1Node[n1]=prinstress1Node[n1]+prinstress1[tN]
                    prinstress1Node[n2]=prinstress1Node[n2]+prinstress1[tN]
                    prinstress1Node[n3]=prinstress1Node[n3]+prinstress1[tN]
                    prinstress1Node[n4]=prinstress1Node[n4]+prinstress1[tN]
                    
                    prinstress2Node[n1]=prinstress2Node[n1]+prinstress2[tN]
                    prinstress2Node[n2]=prinstress2Node[n2]+prinstress2[tN]
                    prinstress2Node[n3]=prinstress2Node[n3]+prinstress2[tN]
                    prinstress2Node[n4]=prinstress2Node[n4]+prinstress2[tN]
                    
                    prinstress3Node[n1]=prinstress3Node[n1]+prinstress3[tN]
                    prinstress3Node[n2]=prinstress3Node[n2]+prinstress3[tN]
                    prinstress3Node[n3]=prinstress3Node[n3]+prinstress3[tN]
                    prinstress3Node[n4]=prinstress3Node[n4]+prinstress3[tN]
                    
            elif MemberList[id].mtype =='CTETRA':
            
                n1=int(MemberList[id].n1)-1
                n2=int(MemberList[id].n2)-1
                n3=int(MemberList[id].n3)-1
                n4=int(MemberList[id].n4)-1
                #print (str(tN)+' '+str(n1)+' '+str(n2)+' '+str(n3)+' '+str(n4))
                
                if isOne==1: 
                    shearstressNode[n1]=shearstress[tN]
                    shearstressNode[n2]=shearstress[tN]
                    shearstressNode[n3]=shearstress[tN]
                    shearstressNode[n4]=shearstress[tN]
                    
                    mstressNode[n1]=mstress[tN]
                    mstressNode[n2]=mstress[tN]
                    mstressNode[n3]=mstress[tN]
                    mstressNode[n4]=mstress[tN]
                    
                    prinstress1Node[n1]=prinstress1[tN]
                    prinstress1Node[n2]=prinstress1[tN]
                    prinstress1Node[n3]=prinstress1[tN]
                    prinstress1Node[n4]=prinstress1[tN]
                    
                    prinstress2Node[n1]=prinstress2[tN]
                    prinstress2Node[n2]=prinstress2[tN]
                    prinstress2Node[n3]=prinstress2[tN]
                    prinstress2Node[n4]=prinstress2[tN]
                    
                    prinstress3Node[n1]=prinstress3[tN]
                    prinstress3Node[n2]=prinstress3[tN]
                    prinstress3Node[n3]=prinstress3[tN]
                    prinstress3Node[n4]=prinstress3[tN]
                else:
                    nodeCount[n1]=nodeCount[n1]+1
                    nodeCount[n2]=nodeCount[n2]+1
                    nodeCount[n3]=nodeCount[n3]+1
                    nodeCount[n4]=nodeCount[n4]+1
                    
                    #print (shearstress[tN])
                    shearstressNode[n1]=shearstressNode[n1]+shearstress[tN]
                    shearstressNode[n2]=shearstressNode[n2]+shearstress[tN]
                    shearstressNode[n3]=shearstressNode[n3]+shearstress[tN]
                    shearstressNode[n4]=shearstressNode[n4]+shearstress[tN]
                    
                    mstressNode[n1]=mstressNode[n1]+mstress[tN]
                    mstressNode[n2]=mstressNode[n2]+mstress[tN]
                    mstressNode[n3]=mstressNode[n3]+mstress[tN]
                    mstressNode[n4]=mstressNode[n4]+mstress[tN]
                    
                    prinstress1Node[n1]=prinstress1Node[n1]+prinstress1[tN]
                    prinstress1Node[n2]=prinstress1Node[n2]+prinstress1[tN]
                    prinstress1Node[n3]=prinstress1Node[n3]+prinstress1[tN]
                    prinstress1Node[n4]=prinstress1Node[n4]+prinstress1[tN]
                    
                    prinstress2Node[n1]=prinstress2Node[n1]+prinstress2[tN]
                    prinstress2Node[n2]=prinstress2Node[n2]+prinstress2[tN]
                    prinstress2Node[n3]=prinstress2Node[n3]+prinstress2[tN]
                    prinstress2Node[n4]=prinstress2Node[n4]+prinstress2[tN]
                    
                    prinstress3Node[n1]=prinstress3Node[n1]+prinstress3[tN]
                    prinstress3Node[n2]=prinstress3Node[n2]+prinstress3[tN]
                    prinstress3Node[n3]=prinstress3Node[n3]+prinstress3[tN]
                    prinstress3Node[n4]=prinstress3Node[n4]+prinstress3[tN]
                    
        if MemberList[id].mtype =='CTRIA3':
            for id in range(numNode): # node
                tn=int(id)
                #print (nodeCount[tn])
                shearstressNode[tn]=shearstressNode[tn]/nodeCount[tn]
                mstressNode[tn]=mstressNode[tn]/nodeCount[tn]
                prinstress1Node[tn]=prinstress1Node[tn]/nodeCount[tn]
                prinstress2Node[tn]=prinstress2Node[tn]/nodeCount[tn]
                prinstress3Node[tn]=prinstress3Node[tn]/nodeCount[tn]
                
        elif MemberList[id].mtype =='CQUAD4':
            for id in range(numNode): # node
                tn=int(id)
                #print (nodeCount[tn])
                shearstressNode[tn]=shearstressNode[tn]/nodeCount[tn]
                mstressNode[tn]=mstressNode[tn]/nodeCount[tn]
                prinstress1Node[tn]=prinstress1Node[tn]/nodeCount[tn]
                prinstress2Node[tn]=prinstress2Node[tn]/nodeCount[tn]
                prinstress3Node[tn]=prinstress3Node[tn]/nodeCount[tn]
                
        elif MemberList[id].mtype =='CTETRA':
            for id in range(numNode): # node
                tn=int(id)
                #print (nodeCount[tn])
                shearstressNode[tn]=shearstressNode[tn]/nodeCount[tn]
                mstressNode[tn]=mstressNode[tn]/nodeCount[tn]
                prinstress1Node[tn]=prinstress1Node[tn]/nodeCount[tn]
                prinstress2Node[tn]=prinstress2Node[tn]/nodeCount[tn]
                prinstress3Node[tn]=prinstress3Node[tn]/nodeCount[tn]
                
        mstressF = []
        prinstress1F = []
        prinstress2F = []
        prinstress3F = []
        shearstressF = []
        for id in range(numNode): # node
            tn=int(id)
            #print (tn)
            #print (mstressNode[tn])
            mstressF.append(mstressNode[tn])
            shearstressF.append(shearstressNode[tn])
            prinstress1F.append(prinstress1Node[tn])
            prinstress2F.append(prinstress2Node[tn])
            prinstress3F.append(prinstress3Node[tn])
            
        for id in range(numNode): # node
            #print (str(id)+" "+str(mode_disp_x[id])+" "+ str(mode_disp_y[id])+" "+str(mode_disp_z[id]))
            mode_disp[mode_disp_id[id]] = FreeCAD.Vector(mode_disp_x[id], mode_disp_y[id], mode_disp_z[id])

        #mode_results["disp"+str(nDisp)] = mode_disp
        mode_results["disp"] = mode_disp
        #mode_results.disp_R = mode_disp_R

        mode_disp = {}

        #nDisp+=1   
                    
        res_obj=[]      
        iLC=0
        results_name="MystranResult"
        # append mode_results to results and reset mode_result
        results.append(mode_results)
        mode_results = {}

        
        for result_set in results:
            res_obj.append(ObjectsFem.makeResultMechanical(FreeCAD.ActiveDocument, results_name+str(iLC)))
                        
            res_obj[iLC].Mesh = result_mesh_object
            
            #res_obj[iLC] = importToolsFem.fill_femresult_mechanical(res_obj[iLC], result_set)
            res_obj[iLC] = toolsFem.fill_femresult_mechanical(res_obj[iLC], result_set)

            import femresult.resulttools as restools
            #import femtools.femutils as femutils

            # fill DisplacementLengths
            res_obj[iLC] = restools.add_disp_apps(res_obj[iLC])

            # fill StressValues
            res_obj[iLC].vonMises = mstressF
            res_obj[iLC].PrincipalMax = prinstress1F
            res_obj[iLC].PrincipalMed = prinstress2F
            res_obj[iLC].PrincipalMin = prinstress3F

            res_obj[iLC].MaxShear = shearstressF
            
            #borrow to show
            #res_obj[iLC].Peeq=mode_disp_R
            #res_obj[iLC].Temperature=mode_disp_Rx
            #res_obj[iLC].NetworkPressure=mode_disp_Ry
            #res_obj[iLC].MassFlowRate=mode_disp_Rz
            
            # fill Stats
            res_obj[iLC] = restools.fill_femresult_stats(res_obj[iLC])
            #res_obj[iLC].ViewObject.DisplayMode = 'Uabs'
            
            #trm._TaskPanel.result_obj = res_obj[iLC]
            #trm._TaskPanel.mesh_obj = res_obj[iLC].Mesh

        FreeCAD.ActiveDocument.recompute()
        FreeCADGui.activeDocument().activeView().viewAxonometric()
        FreeCADGui.SendMsgToActiveView("ViewFit")
        

FreeCADGui.addCommand('hfcMystranNeuIn',hfcMystranNeuIn())
