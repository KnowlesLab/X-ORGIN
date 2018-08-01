#generate genetic_data_SEQ.par from two inputs
#python writeGeneSeqFile.py totalNumOfSNP NumberOfSample
import sys
NumSNP = int(sys.argv[1])
TTNumSample = float(sys.argv[2])
maf = 1/(TTNumSample*2)
header = "%d //Num chromosomes\n"
block = '''#chromosome %d, //per Block:data type, number of SNP, per generation recombination, Minimum frequency for the derived allele)
1
SNP    1  0  %f
'''

outfile = open("genetic_data_SEQ.par","w")
outfile.write(header%NumSNP)
for i in xrange(NumSNP):
	outfile.write(block%(i+1,maf))
outfile.close()
