args<- commandArgs(TRUE);
directory<-getwd();

filename<-args[1]; #file with all the generated data
pcaEigenVector<-args[2]; #file of how to transform all the stats to pc vectors
skiplines<-as.integer(args[3]); #skip how many lines to read data as pods from filenmae
totalPodNumber<-as.integer(args[4]); #total number pods

#regenerate mean and sd
a<-read.table(paste(directory, filename, sep="/"),nrows=200000, header=T,skip=0);
stats<-a[,c(31:86)];
head<-colnames(a);

#read in all the data, and copy the lines of pods
b<-read.table(paste(directory, filename, sep="/"),nrows=totalPodNumber*10, header=T,
                skip=skiplines);
a<-c();
countMat<-matrix(0,25,20)
for (i in 1:nrow(b)) {
	if (countMat[b[i,6],b[i,7]]<10){
		countMat[b[i,6],b[i,7]] = countMat[b[i,6],b[i,7]] + 1
		a<-rbind(a,b[i,])
	}
}
combStats<-b[,c(31:86)]; params<-b[,c(2:7)];
colnames(combStats)<-head[31:86];
colnames(params)<-head[2:7];

#write out untransformed SS
write.table(combStats,paste(directory, "/PodsOriginalSS_",
            filename, sep=""), 
            row.names=F, sep="\t", quote=F);


#standardize
for(i in 1:length(combStats))
  {combStats[,i]<-(combStats[,i]-mean(stats[,i]))/sd(stats[,i]);}
#read in pca eigenvectors
ev<-read.table(paste(directory, pcaEigenVector, sep="/"), header=F, sep = "\t");
ev<-as.matrix(ev)

#transform pods data to pca

outComb<-as.matrix(combStats)%*%ev



#write transformed pca and parameters to data
write.table(outComb,paste(directory, "/PodsSS_",
            filename, sep=""), col.names=paste("Axis", 1:ncol(outComb),sep=""), 
            row.names=F, sep="\t", quote=F);
write.table(params,paste(directory, "/PodsParam_", filename, sep=""), 
            col.names=T, row.names=F, sep="\t", quote=F);


