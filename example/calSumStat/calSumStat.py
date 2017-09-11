###calculate Summary Statistics
import subprocess as sp
import sys,os
import numpy as np

def runArlsumstat(arlSumStat, input):
	cmd = "./%s %s out1.txt 0 1"%(arlSumStat, input)
	p = sp.Popen(cmd, shell=True) 
	p.communicate()

def Arp2snapp(f):
	infile = file(f)
	outfile1 = open("temprun.snapp","w")
	outfile2 = open("temprun_loc.txt","w")

	for line in infile:
		if line.startswith("[Data]"):
			break

	flag = 0
	SampleDict = {}

	p = 0
	for line in infile:
		if flag == 0:
			if "SampleSize" in line:
				sampleSize = int(line.split("=")[1][:-1])
				SampleDict[p] = {}
				continue
			elif "SampleData" in line:
				flag = 1
				continue
		else:
			nline = line.split()
			if len(nline)>0:
				if flag==1:
					sn = nline[0]
					SampleDict[p][sn] = np.array([int(x) for x in nline[2:]])
					flag = 2
					continue
				elif flag == 2:
					SampleDict[p][sn] += np.array([int(x) for x in nline])
					flag = 1
					continue
			else:
				flag = 0
				p += 1

	infile.close()

	outfile2.write("id,latitude,longitude,pop\n")

	for p in SampleDict:
		for sn in SampleDict[p]:
			outfile2.write("%s,%f,%f,REGION_1\n"%(sn,mapInfo[p,0],mapInfo[p,1]))
			outfile1.write("%s,%s\n"%(sn,",".join([str(x) for x in SampleDict[p][sn]])))

	outfile1.close()
	outfile2.close()

def runPsi():
	cmd = "Rscript calPsi.r temprun.snapp temprun_loc.txt out2.txt"
	p = sp.Popen(cmd, shell=True) 
	p.communicate()

wkDir=os.getcwd()
splatcheRunningFolder = sys.argv[1]
arrivalCol = wkDir+ "/" + splatcheRunningFolder + "/" + sys.argv[2]
arpFile = wkDir+ "/" + splatcheRunningFolder + "/GeneticsOutput/" + sys.argv[3]
map = wkDir+ "/" + splatcheRunningFolder + "/" + sys.argv[4]
calSSFolder = sys.argv[5]

mapInfo = np.genfromtxt(map,dtype='float',skip_header = 1,usecols = (3,4))
arrivalTime = [int(x.split(" : ")[1]) for x in file(arrivalCol).readlines()[1:]]

#run python in the calSS folder
#print os.getcwd()
os.chdir(calSSFolder)


out = open("../summary_stats_temp.txt","w")

if sum(n<0 for n in arrivalTime)>0:
	##write sumstat with NAs
	head=file("empiricalSS.obs").readline().split()
	out.write("\t".join(head)+"\n-9999"+"\t-9999"*(len(head)-1)+"\n")
	out.close()
else:
	runArlsumstat("arlsumstat", arpFile)
	Arp2snapp(arpFile)
	out1=file("out1.txt").readlines()
	runPsi()
	out2=file("out2.txt").readlines()
	out.write("%s\t%s\n%s\t%s\n"%(out1[0][:-1],out2[0][:-1],out1[1][:-1],out2[1][:-1]))
	out.close()
	
	
