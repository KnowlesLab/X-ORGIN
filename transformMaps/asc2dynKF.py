#!/usr/bin/python
'''
This script makes an initial world, and generates dynamic conversion table for carrying capacities
based on ancestral and current asc files.
Qixin He
'''
import numpy as np
from optparse import OptionParser

usage = "usage: %prog [options] arg"
parser = OptionParser(usage=usage)
parser.add_option("-l",dest="layers",default = "21k_class.asc,mid_class.asc, current_class.asc", help="list of suitability (integer bins) map files to be used in the simulation, separated by comma")
parser.add_option("-n",dest="totalCat",default = 10,type = "int", help="number of categories of carry capacity, default is 10 (K_0 to K_10) ")
parser.add_option("-g",dest="gui",action="store_true",default = False, help="whether to generate files with actual carrying capacities (instead of parameters) for gui testing or if K is not varied in the simulation")
parser.add_option("-K",dest="maxK",default = 1000.0, type="float",help="max K value used if generating the actual files when -g is set to True")
(options,args) = parser.parse_args()

if __name__ == '__main__':
	mapList = options.layers.split(",")
	print(mapList)
	#load in all the maps
	mapMatrix = []
	maxSuit = 0.0
	options.totalCat = float(options.totalCat)
	for m in mapList:
		temp = np.loadtxt(m,float,skiprows=6)
		temp[temp==-9999]=0
		maxSuit = max(maxSuit, np.max(temp))
		mapMatrix.append(temp)
	numEle = temp.size
	
	#read in header
	with open(m) as myfile:
		head = [next(myfile) for x in range(6)]
	print(head)
	
	#read in suitability combinations
	dynamicKF = np.zeros((numEle,2+len(mapList)),float)
	#print(dynamicKF[0:2,:])
	#column name is:
	#0	      1	     2	      3	     4	    ...          
	#rowNum columnNum layer1 layer2  layer3 ...
	oriworld = np.zeros(np.shape(mapMatrix[0]),int)-9999
	IdCount = 0
	findingList = ['']*numEle
	for index, x in np.ndenumerate(mapMatrix[0]):
		tempId = np.array([index[0],index[1],round(x/maxSuit*options.totalCat)])
		for i in range(1,len(mapList)):
			#print(i)
			tempId = np.append(tempId, round(mapMatrix[i][index]/maxSuit*options.totalCat))
		#print(tempId)
		if np.any(tempId[2:]>0):
			dynamicKF[IdCount] = tempId
			findingList[IdCount] = "_".join([str(y) for y in tempId[2:]])
			IdCount+=1
	
	dynamicKF = dynamicKF[0:IdCount]
	findingList = findingList[0:IdCount]	
	uniqueList=set(findingList)
	print("number of unique classes is ", len(uniqueList))
	
	uniqueDict={}
	FinalID=1
	outFile = []
	for m in mapList:
		outFile.append(open("veg2K_"+m.split(".")[0]+".txt","w"))
	
	for comb in uniqueList:
		#print(comb)
		uniqueDict[comb]=FinalID
		xList=[int(float(x)) for x in comb.split("_")]
		#print(xList)
		for i in range(len(xList)):
			if options.gui:
				outFile[i].write("%d\t%d\t%d\n"%(FinalID,round(float(xList[i])/options.totalCat*options.maxK),FinalID))
			else:
				outFile[i].write("%d\tk_%d\t%d\n"%(FinalID,xList[i],FinalID))
		FinalID+=1
	
	for f in outFile:
		f.close()
	
	for x in range(len(dynamicKF)):
		oriworld[int(dynamicKF[x,0]),int(dynamicKF[x,1])] = uniqueDict[findingList[x]]
	
	oriworldf=open("oriworld.asc","w")
	oriworldf.write(''.join(head))
	for line in oriworld:
		oriworldf.write(" ".join([str(x) for x in line]) + "\n")
	oriworldf.close()
	
	
	
	
	