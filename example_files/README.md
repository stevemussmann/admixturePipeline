# Admixture Pipeline: A Method for Parsing and Filtering VCF Files for Admixture Analysis
A pipeline that accepts a VCF file to run through Admixture

## Tutorial Using Example Files

This tutorial will demonstrate how to run the program using the Docker container. First, download and configure Docker on your system: https://docs.docker.com/get-docker/

Once that is completed, pull the Docker container to your system using the following command:
```
docker pull mussmann/admixpipe:3.0
```

Launch the container by placing the "runDocker.sh" script in the folder from which you want to run the container, then executing it as shown below. This script can be found in the "Docker" folder of this github repository. You can pull the runDocker.sh script to the directory of your choosing using the wget command as shown below.
```
wget https://github.com/stevemussmann/admixturePipeline/blob/master/Docker/runDocker.sh
./runDocker.sh
```
The runDocker.sh script creates a folder named "data" in the directory on your machine from which you launched the Docker container. You can put any input files for AdmixPipe v3.0 into this folder and they will be accessible inside the container (in /app/data/). Any outputs written to this folder and any of its subdirectories will still be accessible after you exit the container. Anything written to other locations inside the container will be lost upon exit. All required AdmixPipe modules (i.e., all except the optional submitClumpak.py module) have been setup within the container and will function with the commands provided throughout the remainder of this tutorial.

When the container launches, you will be placed in the /app/data directory by default. Create a folder in which you will place the example files and change directories into it. Then pull in the example files using the wget command.
```
mkdir exampleDir
cd exampleDir
wget https://github.com/stevemussmann/admixturePipeline/blob/master/example_files/example.vcf.tar.gz
wget https://github.com/stevemussmann/admixturePipeline/blob/master/example_files/example_map.txt
```

The example VCF file has been compressed because its uncompressed size exceeds the maximum file size limit of github (50MB). You can uncompress it with the following command:

```
tar -zxvf example.vcf.tar.gz
```

This should produce a new file named **example.vcf** with a size of approximately 57MB. The example popmap file is presented here as **example_map.txt**

## Running the pipeline with the example files:

You can run the program to validate that it works by running the following command. This will run the pipeline for 8 iterations each on K=1 through K=8. The command will also subsample one SNP per locus (-t 120). This value was selected because the data were assembled via de novo assembly, and each locus has a maximum length of around 120bp. 

```
admixturePipeline.py -m example_map.txt -v example.vcf -k 1 -K 8 -R 8 -t 120
```
