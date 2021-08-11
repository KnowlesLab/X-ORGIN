#the name of the input file, 
args <- commandArgs(trailingOnly = T)
snp_file <- args[1]
coords_file <- args[2] #replaced by cmdline arg 2
#regions_to_analyze <- list("REGION_1")
psi_name<-args[3]
ploidy <- 2  #set ploidy of individuals. 1=haploid, 2 =diploid
subSample <- 0 #Value of number of individual subsample down to, if no subsample is required, put 0
outgroup_columns <- NULL 
nsnp <- NULL
out_file_id = sprintf( "out_%s", basename( snp_file ) )

source("re_functions_resistance.r")
#free some names
if(!is.data.frame(data))data <- c()

read_data_snapp(snp_file=snp_file,
                    coords_file=coords_file, nsnp=nsnp,
                    outgroup_columns=outgroup_columns
                   )
print(c("file id is", out_file_id))


pops <- make_pops_snapp( coords,n=subSample)
pop_data <- make_pop_data_from_pops( pops, data )
pop_coords <- make_pop_coords_from_pops( pops, coords)
pop_ss <- make_pop_ss_from_pops( pops, data, ploidy=ploidy)
pop_coords <- cbind( pop_coords, hets=get_heterozygosity(pop_data,pop_ss))

all_psi <- get_all_psi(pop_data, pop_ss ,n=subSample)
psiVec<-c()
k = 1
for (i in 1: (nrow(all_psi)-1)) {
	for (j in (i+1): nrow(all_psi)) {
		psiVec<-cbind(psiVec, all_psi[i,j])
		colnames(psiVec)[k]<-paste("psi",i,"_",j,sep = "")
		k = k+1
	}
}

write.table(psiVec,psi_name,col.names=T,row.names=F,sep="\t",quote=F)
print( "finished calculating Psi")