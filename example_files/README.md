# Admixture Pipeline: A Method for Parsing and Filtering VCF Files for Admixture Analysis
A pipeline that accepts a VCF file to run through Admixture

## Example Files in this Directory
1) **example.vcf.tar.gz**: compressed vcf file for input to admixturePipeline.py
2) **example_map.txt**: example population map that corresponds to samples in example.vcf. Used as input to admixturePipeline.py
3) **exampleDir.tar.gz**: This compressed folder holds the expected contents of the exampleDir directory described in the tutorial below **prior to running distructRerun.py**. You can use this in the tutorial below if you want to jump into the tutorial at the 'distructRerun.py' step.
4) **1659307908.zip**: This zipped folder is the output of the CLUMPAK pipeline for the steps described below. You can use this in the tutorial below if you want to jump into the tutorial at the 'distructRerun.py' step, or if the CLUMPAK website is down.

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

You can run the program to validate that it works by running the following command. This will run the pipeline for 8 iterations each on K=1 through K=8. The command will also subsample one SNP per locus (-t 120). This value was selected because the data were assembled via de novo assembly, and each locus has a maximum length of around 120bp. Eight processor cores (-n 8) were also used. 

```
admixturePipeline.py -m example_map.txt -v example.vcf -k 1 -K 8 -R 8 -t 120 -n 8
```

When this command finishes running, submit your results.zip and example_pops.txt files to the CLUMPAK server: http://clumpak.tau.ac.il/. This can be done manually using the following instructions:
1) Click the first 'Browse...' button and navigate to your results.zip file.
2) Select the 'ADMIXTURE' radio button.
3) Click the second 'Browse...' button and navigate to the example_pops.txt file.
4) Click the 'Advanced Options' button.
5) Under the 'MCL' threshold, select 'User Defined' and enter 0.9
6) Enter your email address.
7) Click the 'Submit Form' button.

Alternatively, **if you have configured the optional submitClumpak.py module outside of the Docker container**, you can submit the proper files by navigating to the data/exampleDir directory and entering the following command:
```
submitClumpak.py -p example -e smussmann@gmail.com -m 0.9
```

Return to your Docker container. When CLUMPAK finishes processing your data, download the resulting zip file. The proper file will be a 10-digit number zip file (such as 1659307908.zip). You can either download manually and move the file to the /app/data folder of your Docker container, or wget this file directly to the /app/data folder of your Docker container. **The following command is an example. The URL to your data file will be different than the one shown here.**

```
cd /app/data
wget http://clumpak.tau.ac.il/CLUMPAK_results/1659307908/1659307908.zip
```

Once your file is downloaded, unzip the zip file.
```
unzip 1659307908.zip
```

Next, run distructRerun.py to process the output. You must run distructRerun.py before executing any of the following commands. As of v3.0, AdmixPipe uses the distructRerun.py module to record paths to CLUMPAK outputs and admixture results in various json files. These paths are used by the cvSum.py and runEvalAdmix.py modules. Likewise, if you move your results folder or CLUMPAK output folder after running distructRerun.py, then you will have to run this step again before proceeding. 
```
distructRerun.py -d 1659307908/ -a exampleDir/ -k 1 -K 8
```

You can now get the cv value and log likelihood summary stats and plots for your major and minor clusters by running cvSum.py
```
cvSum.py
```

Finally, you can run EvalAdmix on your run. Change back to the /app/data/exampleDir directory and run it with the following command:
```
cd exampleDir/
runEvalAdmix.py -p example -k 1 -K 8 -m example_map.txt -n 8
```
