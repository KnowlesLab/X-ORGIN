library(MASS)
library(plyr)
directory<-getwd()


podParam<-read.table(paste(directory, "/PodsParam_toy_allParams.txt",sep = ""),header=T)
podParam$inferLat = -1
podParam$inferLon = -1
podParam$error = -1
TTpods<-nrow(podParam)

originDist<-function(x1,y1, x2,y2) {
  return(sqrt((x1-x2)^2+(y1-y2)^2))
}

calOriginFunction<-function(a, rown = 25, coln = 21, xlim = c(1,21), ylim = c(1,25), h = 1){
  outC<-kde2d(rep(a$oriLon,round(max(a$Dist)/a$Dist)*10), 
              rep(a$oriLat,round(max(a$Dist)/a$Dist)*10),h=h,n=c(coln,rown), 
              lims = c(xlim, ylim))
  indx<-arrayInd(which.max(outC$z),dim(outC$z))
  return(c(outC$x[indx[1]],outC$y[indx[2]]))
}


for (i in 0:(TTpods-1)) {
    a<-read.table(paste(directory,"/pod/toyPodsEvalBestSimsParamStats_Obs",i,".txt",sep = ""), header=T)
  outInd<-calOriginFunction(a)
  podParam$inferLon[i+1]<-outInd[1]
  podParam$inferLat[i+1]<-outInd[2]
  podParam$error<-originDist(podParam$oriLat[i+1], podParam$oriLon[i+1], podParam$inferLat[i+1], podParam$inferLon[i+1])
  write.table(podParam[i+1,],paste(directory, "/XoriginPerformance.txt",sep=""), col.names=F,row.names=F, sep="\t", quote=F, append =T)

}


