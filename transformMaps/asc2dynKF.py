#!/usr/bin/python
'''
This script make an initial world, and generate dynamic conversion table for carrying capacities
based on ancestral and current asc files.
Qixin He
'''
import numpy as np
from optparse import OptionParser

usage = "usage: %prog [options] arg"
parser = OptionParser(usage=usage)
parser.add_option("-a",dest="lgmFileName",default = "21k_class.asc", help="name of the lgm suitability (integer bins) map file")
parser.add_option("-c",dest="curFileName",default = "current_class.asc", help="name of the current suitability (integer bins) map file")
parser.add_option("-g",dest="gui",action="store_true",default = False, help="name of the current suitability (integer bins) map file")
parser.add_option("-K",dest="maxK",default = 1000.0, type="float",help="maximum K value")
(options,args) = parser.parse_args()

LGMWorld=np.loadtxt(options.lgmFileName,float,skiprows=6)
#print LGMWorld[0,100:105]
numEle = np.sum(LGMWorld!=-9999)
print "suitable cell number in LGM is ",numEle
dynamicKF = np.zeros((numEle,6),float)
#column name is:
#0	      1	     2	      3	     4	          5              
#FinalID rowNum columnNum LGM intermediate Current
curWorld=np.loadtxt(options.curFileName,float,skiprows=6)
maxSuit = max(np.max(LGMWorld),np.max(curWorld))
#print np.max(LGMWorld)
LGM = file(options.lgmFileName)
row=1
header=''
for line in LGM:
	if row <7:
		header+=line
	else:
		break
	row+=1
LGM.close()			
oriworld = np.zeros(np.shape(LGMWorld),int)
IdCount = 0
findingList = ['']*numEle
for index, x in np.ndenumerate(LGMWorld):
	if x == -9999:
		oriworld[index] = -9999
	else:
		if curWorld[index]==-9999:
			curWorld[index]=0
		xr = int(round(x/maxSuit*10))
		intr = int(round(np.mean([x,curWorld[index]])/maxSuit*10))
		cr = int(round(curWorld[index]/maxSuit*10))
		dynamicKF[IdCount] = [-1,index[0],index[1],xr,intr,cr]
		findingList[IdCount] = "%d_%d"%(xr,cr)
		IdCount+=1
uniqueList=set(findingList)
print "number of unique classes is ", len(uniqueList)
uniqueDict={}
FinalID=1

vegcur = open("veg2K_cur.txt","w")
vegint = open("veg2K_int.txt","w")
veglgm = open("veg2K_lgm.txt","w")
for x in uniqueList:
	#print x
	uniqueDict[x]=FinalID
	(lgm,current)=x.split("_")
	if options.gui:
		vegcur.write("%d\t%d\t%d\n"%(FinalID,round(float(current)/10.0*options.maxK),FinalID))
		veglgm.write("%d\t%d\t%d\n"%(FinalID,round(float(lgm)/10.0*options.maxK),FinalID))
		vegint.write("%d\t%d\t%d\n"%(FinalID,round((float(lgm)+float(current))/20.0*options.maxK),FinalID))
	else:
		vegcur.write("%d\tk_%s\t%d\n"%(FinalID,current,FinalID))
		veglgm.write("%d\tk_%s\t%d\n"%(FinalID,lgm,FinalID))
		intv = (float(lgm) + float(current))/2
		if intv-int(intv) == 0.5:
			vegint.write("%d\tk_%d-5\t%d\n"%(FinalID,int(intv),FinalID))
		else:
			vegint.write("%d\tk_%d\t%d\n"%(FinalID,int(intv),FinalID))

	FinalID+=1

for x in range(len(dynamicKF)):
	oriworld[int(dynamicKF[x,1]),int(dynamicKF[x,2])] = uniqueDict[findingList[x]]

oriworldf=open("oriworld.asc","w")
oriworldf.write(header)
for line in oriworld:
	oriworldf.write(" ".join([str(x) for x in line]) + "\n")
oriworldf.close()