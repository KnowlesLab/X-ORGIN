#arp2snapp
import sys
import numpy as np

infile = open(sys.argv[1],'r')
map = "GenSamples.sam"
mapInfo = np.genfromtxt(map,dtype='float',skip_header = 1,usecols = (3,4))

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

outfile1 = open("temprun.snapp","w")
outfile2 = open("temprun_loc.txt","w")
outfile2.write("id,latitude,longitude,pop\n")

for p in SampleDict:
	for sn in SampleDict[p]:
		outfile2.write("%s,%f,%f,REGION_1\n"%(sn,mapInfo[p,0],mapInfo[p,1]))
		outfile1.write("%s,%s\n"%(sn,",".join([str(x) for x in SampleDict[p][sn]])))

outfile1.close()
outfile2.close()