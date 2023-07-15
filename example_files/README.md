# AdmixPipe v3.1 Tutorial: 

A pipeline for parsing and filtering VCF and PLINK files to conduct Admixture analysis

## Example Files in this Directory
The tutorial primarily relies upon the following two files:
1) **example.vcf.tar.gz**: compressed vcf file for input to admixturePipeline.py
2) **example_map.txt**: example population map that corresponds to samples in example.vcf. Used as input to admixturePipeline.py

If you want to jump into the tutorial at certain points, the next two files can be helpful if you want to skip the admixturePipeline.py step or submitClumpak.py step.
3) **exampleDir.tar.gz**: This compressed folder holds the expected contents of the exampleDir directory described in the tutorial below **prior to running distructRerun.py**. You can use this in the tutorial below if you want to jump into the tutorial at the 'distructRerun.py' step.
4) **1659307908.zip**: This zipped folder is the output of the CLUMPAK pipeline for the steps described below. You can use this in the tutorial below if you want to jump into the tutorial at the 'distructRerun.py' step, or if the CLUMPAK website is down.

Finally, these two files can be used for testing the direct input of PLINK files.
5) **bed_example.tar.gz**: Example .bed formatted files (and associated popmap.txt) that can be used to run admixturePipeline.py from the -b/--bed option.
6) **ped_example.tar.gz**: Example .ped formatted files (and associated popmap.txt) that can be used to run admixturePipeline.py from the -p/--ped option.

## Tutorial Using Example Files

This tutorial will demonstrate how to run the program using the Docker container. First, download and configure Docker on your system: https://docs.docker.com/get-docker/

Once that is completed, pull the Docker container to your system using the following command:
```
docker pull mussmann/admixpipe:3.1
```

If you are using a Mac, launch the 'Docker Desktop' application.

Launch the container by placing the [runDocker.sh](https://github.com/stevemussmann/admixturePipeline/blob/master/Docker/runDocker.sh) script in the directory on your computer from which you want to run the container, then executing it as shown below. You can pull the runDocker.sh script to the directory of your choosing using the wget command as shown below.
```
wget https://raw.githubusercontent.com/stevemussmann/admixturePipeline/master/Docker/runDocker.sh
./runDocker.sh
```
The `runDocker.sh` script creates a folder named `data/` in the directory on your machine from which you launched the Docker container. This folder is shared from your machine to the Docker container, meaning you can put any input files for AdmixPipe v3.1 into this folder and they will be accessible inside the container (in `/app/data/`). Any outputs written to this folder and any of its subdirectories will remain accessible after you exit the container. Anything written to other locations inside the container will be lost upon exit. All AdmixPipe modules have been setup within the container and will function with the commands provided throughout the remainder of this tutorial.

When the container launches, you will be placed in the `/app/data` directory by default. Create a folder in which you will place the example files and change directories into it. Then pull in the example files using the wget command.
```
mkdir exampleDir
cd exampleDir
wget https://raw.githubusercontent.com/stevemussmann/admixturePipeline/master/example_files/example.vcf.tar.gz
wget https://raw.githubusercontent.com/stevemussmann/admixturePipeline/master/example_files/example_map.txt
```

The example VCF file has been compressed because its uncompressed size exceeds the maximum file size limit of github (50MB). You can uncompress it with the following command:

```
tar -zxvf example.vcf.tar.gz
```

This will produce a new file named `example.vcf` with a size of approximately 57MB. The example popmap file is presented here as `example_map.txt`

## Running the pipeline with the example files:

### admixturePipeline.py

You can run the program to validate that it works by running the following command. This will run the pipeline for 8 iterations (`-R`) each on K=1 (`-k 1`) through K=8 (`-K`). The command will also subsample one SNP per locus (`-t 120`). This value was selected because the data were assembled via de novo assembly, and each locus has a maximum length of around 120bp. If you are using reference aligned data, you will likely want to set a higher `-t` value since your VCF file might contain many SNPs located close to one another in the genome. Eight processor cores (`-n 8`) were used for computation during each repetition of Admixture. 

```
admixturePipeline.py -m example_map.txt -v example.vcf -k 1 -K 8 -R 8 -t 120 -n 8
```

While the command is running, you will see the system calls to individual programs (vcftools, plink, admixture) printed to stdout. This provides an approximate indicator of progress. 

When this command finishes running, several files are present in `data/exampleDir`. The most important of these are `results.zip` (contains output of each Admixture replicate) and `example_pops.txt` (contains population data for plotting in CLUMPAK). Proceed to the next module to run CLUMPAK.

### submitClumpak.py

This tutorial describes using the submitClumpak.py module as it is configured in the Docker container. If you are not using the Docker container, or have done an alternate configuration of this module as described in the manual installation instructions, then you might want to consider [alternatives for running CLUMPAK](#alternatives) as described at the end of this tutorial.

To run CLUMPAK on the example data in the Docker container, execute the following command:

```
submitClumpak.py -p example -M
```

At first, CLUMPAK does not give much indication that it is running, and this pipeline can potentially run for minutes to hours depending upon the number of K values tested, the number of repetitions per K, and your computer's CPU speed. 

Once the pipeline finishes your output should be in `data/exampleDir/clumpakOutput/`. This folder will contain all CLUMPAK output that is contained within the zip folder you would download from the CLUMPAK webserver. It also contains a zipped folder that archives all of the CLUMPAK outputs from this run. The zip archive is named using a 13-digit Unix epoch timestamp (e.g., 1688937470966.zip). If you want to rerun CLUMPAK with different settings but retain this job output, you can simply backup this zip archive somewhere outside of the `clumpakOutput/` directory, delete `clumpakOutput/`, and rerun submitClumpak.py with new settings.

For example, CLUMPAK's default settings may have done a poor job of clustering similar replicates into major and minor clusters, so you want to increase the MCL threshold. To do this, delete the clumpakOutput/ directory and rerun submitClumpak.py with the following settings. The `-m 0.9` option fixes the MCL cluster similarity threshold at 0.9.

```
submitClumpak.py -p example -m 0.9 -M
```

Once you are happy with the results (you can view the preliminary outputs in the `.pdf` file in your `clumpakOutput/` directory) then proceed to running distructRerun.py.

### distructRerun.py

Next, run distructRerun.py to process the CLUMPAK output. As of v3.1, AdmixPipe uses the distructRerun.py module to record paths to CLUMPAK outputs and admixture results in various `.json` files. These paths are used downstream by the cvSum.py and runEvalAdmix.py modules. This means that if you move your results folder and/or CLUMPAK output folder after running distructRerun.py, then you will have to execute distructRerun.py again before proceeding with other modules. 

The following command prepares your CLUMPAK outputs so that you can modify properties of your admixture plots for publication. The basic command is the following, where `-d` and `-a` specify the locations of your CLUMPAK and admixturePipeline.py outputs, respectively. These required parameters can handle relative paths, but will determine and write the full path of the outputs to `.json` files. The parameters `-k 1 -K 8` provide the range of K values that you tested. From the `/app/data/exampleDir/` directory, run the following:

```
distructRerun.py -d clumpakOutput/ -a ./ -k 1 -K 8
```

If you want to automatically run distruct on each plot for each K value, you can append the `-r` option to this command as shown below. However, I must warn that distruct does not yield exit codes signifying successful execution of the program (even when it runs correctly), so the distructRerun.py module cannot adequately check if distruct ran successfully and will continue to try running distruct even if errors are encountered.

```
distructRerun.py -d clumpakOutput/ -a ./ -k 1 -K 8 -r
```

If you do not want to automatically run distruct on all K values, you can alternatively execute it on individual draparams files produced by distructRerun.py. Switch directories to `/app/data/exampleDir/clumpakOutput/best_results/` and run distruct on any drawparams files for which you want to view the output. For example, if you want to view the plot for the K=6 major cluster, execute the following:

```
distruct -d drawparams.6
```

The above code would produce a postscript file named `K6.ps`. You can view it by navigating to the file's location through your computers OS (i.e., not through the Docker container). If your OS cannot view `.ps` files as images natively, you can convert it to `.pdf` using ghostscript which is installed in the Docker container. You can do this with the following command:

```
ps2pdf K6.ps
```

The distructRerun.py module should run quickly, and will produce several files that will be inputs for cvSum.py in the directory from which it was executed. You may find that you would like to modify the look of your admixture plots (change bar widths, color palette, order of populations, etc.) and this is where it can be done using tools that are supplied to you in the Docker container. 

You can use distructRerun.py to customize the admixture plot appearance. For example, the `-w` option can change the width of individual sample bars in the structure plot. The default value for this parameter is 2, so setting a lower value will make the plot smaller (this may be necessary to fit all individuals into the plot when you have several hundred or thousands of individuals), and setting a higher number will cause the admixture plot to take up more space on the page. Additionally, you can change the color palette for all plots using the palettes listed in the [distruct user manual](https://rosenberglab.stanford.edu/software/distructManual.pdf). By default, distructRerun.py applies the BrBG color palette, but if you want to change it to another palette this can be specified with the `-c` option. For example, `-c RdBu` would apply the Red-Blue color scheme. This is all that needs to be specified, and distructRerun.py will figure out the rest based upon K values tested, etc. However, please note that if the color palette you select does not exist for some of the K values you tested, then these will output the default color scheme when `distruct` is run on your file.

For example, I can apply the above described changes with the following command:

```
distructRerun.py -d clumpakOutput/ -a ./ -k 1 -K 8 -w 3 -c RdBu
```

You may also want to group populations together in your admixture plot based upon their population assignments. You can accomplish this by editing the order of lines in the `AdmixturePopIdToPopName` file which is located in `/app/data/exampleDir/clumpakOutput/best_results`. By default, the file contains the following information. The top to bottom order in which lines appear in the plot indicate the order in which they will be printed, from bottom to top, in the admixture plots. For example, the population `groupA` is on line 1 and should appear at the bottom of your plot in your `K6.ps` or `K6.pdf` file. 

```
1 groupA
2 groupB
3 groupC
4 groupD
5 groupE
6 groupF
7 groupG
8 groupH
9 groupI
10 groupJ
11 groupK
12 groupL
13 groupM
14 groupN
15 groupO
16 groupP
17 groupQ
18 groupR
19 groupS
20 groupT
21 groupU
22 groupV
23 groupW
24 groupX
25 groupY
26 groupZ
27 groupAA
```

In my K=6 major cluster plot, the poplations groupD, groupF, and groupO were assigned shared ancestry. If I want them to appear together at the bottom of the plot, I can modify the `AdmixturePopIdToPopName` file to appear like below. The program `vim` is installed in the Docker container so it can be used as a text editor to facilitate these changes. Note that you only want to change the order of the lines in the file. You do not want to alter the numbers in the file because these map population names to sample groups in your outputs.

```
1 groupA
2 groupB
3 groupC
5 groupE
7 groupG
8 groupH
9 groupI
10 groupJ
11 groupK
12 groupL
13 groupM
14 groupN
16 groupP
17 groupQ
18 groupR
19 groupS
20 groupT
21 groupU
22 groupV
23 groupW
24 groupX
25 groupY
26 groupZ
27 groupAA
15 groupO
6 groupF
4 groupD
```

Now if you rerun the command `distruct -d drawparams.6` you should see groupO, groupF, and groupD grouped together at the bottom of the plot.

If you want additional control over plot appearance, you can also directly modify any of the draparams files produced by distructRerun.py. You may want to return to some of the options in this module after running cvSum.py.

### cvSum.py

After executing distructRerun.py, you can get the cv value and log likelihood summary stats/plots for your major/minor clusters by running cvSum.py. Make sure you are in the directory from which you ran distructRerun.py (which should be `/app/data/exampleDir/` if you have been following the tutorial) and execute the following command. No special options are necessary if you have not changed the names of any outputs.

```
cvSum.py
```

This creates several outputs, the most important of which are boxplots of the CV values for each major and minor cluster found by CLUMPAK (`cv_file.MajClust.png`). Here, it looks like the K=7 major cluster was a good explanation of population structure, as indicated by its lowest CV values. However, there was some variability and the K=8 major cluster and K=8 minor cluster 3 also produced low CV values. It may be worth exploring those as well.
![cv_file MajClust](https://github.com/stevemussmann/admixturePipeline/assets/17727337/6c01693b-d1b8-4e4f-a3ce-e9cd0ba5eace)

A similar plot is output for -loglikelihood values. We can see that the -loglikelihood values increased until approximately the K=8 major cluster.
![loglikelihood_file MajClust](https://github.com/stevemussmann/admixturePipeline/assets/17727337/5fb2c607-006e-428c-ab67-35c4ed41a6a5)

After running cvSum.py you can also explore the BestK pipeline outputs from CLUMPAK. For example, execute the following command from the `/app/data/exampleDir` directory.

```
submitClumpak.py -p example -b
```

This will produce output in a new subfolder named `clumpakBestK/`, and will contain the same outputs you would receive from running this function on the webserver. However, it is important to note that this BestK pipeline will sometimes fail if you tested a K value for which the resulting standard deviation of -loglikelihood values was zero. This can happen sometimes with K=1, especially.

### runEvalAdmix.py

Finally, you can run EvalAdmix on your admixture analysis. Change back to the `/app/data/exampleDir` directory and run it with the following command. Again, `-p example` represents the prefix of your orignal input `.vcf` file, `-m example_map.txt` is your population map file, and `-k 1 -K 8` is the range of K values that you tested. The `-n 8` options provides the number of processor cores to be used by evalAdmix. This command may take several minutes to run depending upon your CPU speed, number of processor cores, replicates, range of K values, etc. However, it prints outputs regularly so you can track its progress.

```
runEvalAdmix.py -p example -k 1 -K 8 -m example_map.txt -n 8
```

This module runs evalAdmix on each replicate that you performed, and calculates a pairwise correlation of residuals matrix between individuals for each replicate. It then averages those results based upon the major and minor clusters identified by clumpak, and plots those results. This results in a single plot for reach major or minor cluster. Interpretations of the plots can be found at the [evalAdmix site (and links provided therein)](http://www.popgen.dk/software/index.php/EvalAdmix#Run_command_example). 

That completes the tutorial for the AdmixPipe pipeline. Below you will also find a couple of additional special use cases for the pipeline (i.e., directly inputting PLINK files and using a manual configuration of the submitClumpak.py module).

## Running the pipeline directly from PLINK example Files

You can run admixturePipeline.py directly from pre-filtered PLINK files (both .bed and .ped formats). Example files are provided here as reference in case you have trouble running the pipeline on your own .bed or .ped files. You can test the pipeline on these files using the following commands.

For running on the .ped example files:
```
admixturePipeline.py -m popmap.txt -p dx2003.filt2 -k 2 -K 4 -R 3 -n 8
```

The command for the .bed example is very similar:
```
admixturePipeline.py -m popmap.txt -b dx2003.filt2 -k 2 -K 4 -R 3 -n 8
```

Commands for most of the rest of the pipeline are unaffected by the file type input to admixturePipeline.py. The one exception is the runEvalAdmix.py module. The program evalAdmix requires .bed as input. If you run admixturePipeline.py from a .ped file, no changes are necessary to how the pipeline is run because it will automatically convert your .ped to .bed. However, if you ran admixturePipeline.py from a .bed file you will have to let runEvalAdmix.py know that a .bed already exists. This is accomplished with the -b/--bed switch in runEvalAdmix.py. For example:

```
runEvalAdmix.py -m popmap.txt -p dx2003.filt2 -k 2 -K 4 -n 8 -b
```

## CLUMPAK Alternatives

If you are not using the Docker container and did not set up CLUMPAK on your local machine, then you can submit your results.zip and example_pops.txt files to the [CLUMPAK server](http://clumpak.tau.ac.il/). This can be done manually using the following instructions:
1) Click the first 'Browse...' button and navigate to your results.zip file.
2) Select the 'ADMIXTURE' radio button.
3) Click the second 'Browse...' button and navigate to the example_pops.txt file.
4) Click the 'Advanced Options' button.
5) Under the 'MCL' threshold, select 'User Defined' and enter 0.9
6) Enter your email address.
7) Click the 'Submit Form' button.

Alternatively, **if you configured your computer so that the submitClumpak.py module will access the CLUMPAK server**, you can submit the proper files by navigating to the `data/exampleDir` directory and entering the following command:
```
submitClumpak.py -p example -e smussmann@gmail.com -m 0.9
```

When CLUMPAK finishes processing your data, download the resulting zip file. The proper file will be a 10-digit number zip file (such as 1659307908.zip). You can either download manually and move the file to the /app/data folder of your Docker container, or wget this file directly to the /app/data folder of your Docker container. **The following command is an example. The URL to your data file will be different than the one shown here.**

```
cd /app/data
wget http://clumpak.tau.ac.il/CLUMPAK_results/1659307908/1659307908.zip
```

Once your file is downloaded, unzip the zip file.
```
unzip 1659307908.zip
```
