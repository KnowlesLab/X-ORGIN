library(MASS)
library(plyr)
directory<-getwd()
args<- commandArgs(TRUE);
distanceFile<-args[1]; #file with distance calculated fro all retained simulations


calOriginFunction<-function(a, rown = 25, coln = 21, xlim = c(1,21), ylim = c(1,25), h = 1){
  outC<-kde2d(rep(a$oriLon,round(max(a$Dist)/a$Dist)*10), 
              rep(a$oriLat,round(max(a$Dist)/a$Dist)*10),h=h,n=c(coln,rown), 
              lims = c(xlim, ylim))
  indx<-arrayInd(which.max(outC$z),dim(outC$z))
  return(c(outC$x[indx[1]],outC$y[indx[2]]))
}


a<-read.table(distanceFile, header=T)
outInd<-calOriginFunction(a)
write.table(outInd,paste(directory, "/EstimatedOrigin.txt",sep=""), col.names=c("Longitude","Latitude"),row.names=F, sep="\t", quote=F)




