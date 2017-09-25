args<- commandArgs(TRUE);
directory<-getwd();
#file with simulated summary statistics
filename<-args[1]
#file with empirical summary statistics
empiricalFile<-args[2]

library(adegenet)
#read file
###copy first 10000 lines from all cases into one file for pbs
a<-read.table(paste(directory, filename, sep="/"),nrows=200000, header=T,skip=0);
print(names(a));

#specify summary statistics columns
stats<-a[,c(30:85)]; 
#specify parameter columns
params<-a[,c(3,5:6)]; 

params[,2]<-params[,2]+runif(nrow(params))-0.5 #parameter column of latitude/longitude
params[,3]<-params[,3]+runif(nrow(params))-0.5 #parameter column of latitude/longitude
#rm(a);
empStats<-read.table(paste(directory,empiricalFile,sep="/"),header=T)
#specify summary statistics columns in the empirical SS file
empStats<-empStats[,24:length(empStats)] 

#add empStats to the first row before all the simulated rows,
#for centering and standardizing process
combStats<-rbind(empStats,stats)

#standardize the stats, the standadization only includes the simulated case
for(i in 1:length(combStats))
  {combStats[,i]<-(combStats[,i]-mean(stats[,i]))/sd(stats[,i]);}


#perform pca
library(adegenet)
numComp<-20; #number of principal components
apca<-dudi.pca(combStats, scale=F,center=F,scannf=FALSE,nf=numComp)

#write pca to a file
write.table(apca$c1, file=paste(directory, "/PCAEigenVector_", filename, sep=""), 
            col.names=F, row.names=F, sep="\t", quote=F);
#write empirical data and transformed pca to data
write.table(apca$li[1,],paste(directory, "/PCACo_", empiricalFile, sep=""), 
            col.names=T, row.names=F, sep="\t", quote=F);
write.table(cbind(params,apca$li[2:nrow(combStats),]),paste(directory, "/PCACo_",
            filename, sep=""), col.names=T, row.names=F, sep="\t", quote=F,
            append = T);

for (j in 1:4) {
  a<-read.table(paste(directory, filename, sep="/"),nrows=200000, header=T,
                skip=j*200000);
  combStats<-a[,c(30:85)]; params<-a[,c(3,5:6)];
params[,2]<-params[,2]+runif(nrow(params))-0.5
params[,3]<-params[,3]+runif(nrow(params))-0.5
	
  for(i in 1:length(combStats))
  {combStats[,i]<-(combStats[,i]-mean(stats[,i]))/sd(stats[,i]);}
  outComb<-as.matrix(combStats)%*%as.matrix(apca$c1)
  write.table(cbind(params,outComb),paste(directory, "/PCACo_",
  filename, sep=""), col.names=F, row.names=F, sep="\t", quote=F,append = T);
}

