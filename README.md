[![DOI](https://zenodo.org/badge/96546673.svg)](https://zenodo.org/badge/latestdoi/96546673)

# AdmixPipe v3: A Method for Parsing and Filtering VCF and PLINK Files for Admixture Analysis
A pipeline that accepts VCF and PLINK files to run through Admixture

## Citing AdmixPipe
AdmixPipe v2.0 is published in BMC Bioinformatics. A manuscript is currently in preparation for v3.1. For now, please cite the 2020 publication if you use any part of this pipeline:

S.M. Mussmann, M.R. Douglas, T.K. Chafin, M.E. Douglas 2020. AdmixPipe: population analyses in ADMIXTURE for non-model organisms. BMC Bioinformatics 21:337. DOI: 10.1186/s12859-020-03701-4

## IMPORTANT CHANGES IN v3.1 (updated 8-July-2023)

This README.md file is for AdmixPipe v3.1, which has several changes, bug fixes, and enhancements to existing modules. Two new modules were also developed for the following purposes: 
1) submission of admixturePipeline.py output to the CLUMPAK pipeline.
2) assessment of the best K using the evalAdmix package (http://www.popgen.dk/software/index.php/EvalAdmix). 

Some outputs from AdmixPipe v2.0 are not compatible with v3.1 because json files are now utilized to record data and file names from early parts of the pipeline that are needed for later modules. If you require the v2.0 scripts for any reason, they are still available from the prior releases on this page (v2.0.2 was the final release of AdmixPipe v2.0).

Other important notes for v3.1: 
1) AdmixPipe v3.1 requires Python 3.
2) Some command line options have changed slightly (especially long form commands - you can retrieve the current list of commands from any module by executing it with the --help option).
3) A Docker container is now the preferred method for installation.
4) CLUMPAK is now installed in the Docker container.
5) The submitClumpak.py module will submit admixturePipeline.py outputs to the Docker container installation of CLUMPAK ('Main pipeline' and 'BestK' pipeline).
7) The data processing and plotting functions of the cvSum.py module underwent a complete rewrite for v3.1.
8) PLINK .bed and .ped files are now accepted as direct input. Minor allele frequency and missing data filtering options are enabled for loci. Individual-based missing data filtering is not enabled for PLINK files.
9) The '-r / --remove' option was removed from admixturePipeline.py. This option's behavior became unnecessary because individuals not listed in your popmap are now automatically filtered by both VCFtools and PLINK. 

## Installation & Setup for AdmixPipe v3:

### Docker Setup
This pipeline was written for Unix based operating systems, such as the various Linux distributions and Mac OS X. As of v3.1, we have achieved greater platform independence and ease of installation through development of a Docker container. This is the preferred method for running AdmixPipe. To get started, install [Docker](https://www.docker.com/) on your machine and pull the Docker image using the following command:

```
docker pull mussmann/admixpipe:3.1
```

Launch the container by first placing the [runDocker.sh script](https://github.com/stevemussmann/admixturePipeline/blob/master/Docker/runDocker.sh) in the folder from which you want to run the container. Then execute the script as shown below.

```
./runDocker.sh
```
This script creates a folder named "data" in the directory on your machine from which you launched the Docker container. You can put any input files for AdmixPipe v3.1 into this folder and they will be accessible inside the container (in /app/data/). Any outputs written to this folder and any of its subdirectories will still be accessible after you exit the container. If you write any output to other locations inside the container, they will be lost upon exit. All required AdmixPipe modules and dependency programs have been configured within the container and, unless noted otherwise, will function with the commands provided throughout the remainder of this documentation. 

If running the runDocker.sh script on your machine requires sudo permission, you can create a docker users group and add your username to that group. This can be accomplished with the following, if you are running the command from your own user account. If you are running the command for another user, replace `${USER}` with their username:

```
sudo groupadd docker
sudo usermod -aG docker ${USER}
```

If you add a docker users group you may need to restart your computer before the changes take effect.

### Manual Setup
Manual installation of AdmixPipe v3.1 is not advised due to the many required dependencies. However, if you insist upon installing the pipeline manually, I have provided detailed instructions [at the end of this guide](#manualinstall). 

# Running AdmixPipe v3

AdmixPipe v3 is composed of five different modules. Follow the links below in the table of contents to find specific instructions for running each module. More detailed manual installation instructions are also provided if you cannot / do not want to use Docker container.

### Table of Contents:
1. [admixturePipeline.py](#admixturepipeline)
    * [Usage](#admixusage)
    * [Options](#admixoptions)
    * [Outputs](#admixoutputs)
2. [submitClumpak.py](#submitclumpak)
    * [Usage](#clumpakusage)
    * [Options](#clumpakoptions)
    * [Outputs](#clumpakoutputs)
3. [distructRerun.py](#distructrerun)
    * [Usage](#distructusage)
    * [Options](#distructoptions)
    * [Outputs](#distructoutputs)
4. [cvSum.py](#cvsum)
    * [Usage](#cvusage)
    * [Options](#cvoptions)
    * [Outputs](#cvoutputs)
5. [runEvalAdmix.py](#runevaladmix)
    * [Usage](#evalusage)
    * [Options](#evaloptions)
    * [Outputs](#evaloutputs)

For a full tutorial see the [example_files directory](https://github.com/stevemussmann/admixturePipeline/tree/master/example_files) in this repository. The remainder of this README file describes basic functions of AdmixPipe.

# 1. admixturePipeline.py: <a name="admixturepipeline"></a>
This module takes standard genotype data files (VCF or BED/PED) as input, conducts filtering according to user-specified parameters, performs all necessary file conversions, and finally executes Admixture on the filtered dataset according to user-specified parameters. 

**New feature in AdmixPipe v3.1:** This module now filters individuals that are absent from your popmap file. For example, if you want to exclude an individual sample from your analysis, just leave it out of your popmap file and it will be removed from your vcf file before admixture is executed. 

## Usage: <a name="admixusage"></a>

You can run the program to print help options with the following command:

```
./admixturePipeline.py -h
```

Required options:<a name="admixoptions"></a>
* **-m / --popmap:** Specify a tab-delimited population map (sample --> population).  Click [here](https://github.com/stevemussmann/admixturePipeline/blob/master/example_files/example_map.txt) for an example. This will be converted to a population list that can be input into a pipeline such as CLUMPAK (http://clumpak.tau.ac.il/) for visualization of data

One of the following three options is also required:
* **-b / --bed:** Specify a binary plink file (.bed) for input. This option disables some individual sample-based filtering options in the program.
* **-p / --ped:** Specify a text-based plink file (.ped) for input. File should have been produced using the --recode12 option in plink. This option disables some individual sample-based filtering options in the program.
* **-v / --vcf:** Specify a VCF file for input.

Optional arguments:
* **-n / --np:** Specify the number of processors.  Currently the only multithreaded program is Admixture.

Admixture optional arguments:
* **-c / --cv:** Specify the cross-validation number for the admixture program.  See the admixture program manual for more information (default = 20)
* **-k / --minK:** Specify the minimum K value to be tested (default = 1).
* **-K / --maxK:** Specify the maximum K value to be tested (default = 20).
* **-R / --rep:** Specify the number of replicates for each K value (default = 20)

General filtering options (enabled for both VCFtools and PLINK):
* **-a / --maf:** Enter a minimum frequency for the minor allele frequency filter. (default = off, specify a value between 0.0 and 1.0 to turn it on).
* **-M / --mac:** Enter the minimum count for the minor allele filter. (default = off, specify a positive integer to turn it on).
* **-S / --snpcov:** Filter SNPs based on proportion of allowable missing data. Feature added by tkchafin. (default = 0.1; defined to be between 0 and 1, where 0 allows sites that are completely missing and 1 indicates no missing data allowed; input = float).

VCFtools filtering options:
* **-B / --bi:** Turns biallelic filter off. (default = on, **we do not recommend turning this setting off because ADMIXTURE only processes biallelic SNPs**)
* **-C / --indcov:** Filter samples based on maximum allowable missing data. Feature added by tkchafin. (default = 0.9, input = float).
* **-t / --thin:** Filter loci by thinning out any loci falling within the specified proximity to one another, measured in basepairs.  (default = off, specify an integer greater than 0 to turn it on).

## Example:

The preferred usage of the program is to provide a .vcf file as input. The following command will run the program from K values 1 through 10, conducting 10 repetitions at each K value.  Admixture will use 16 processors for execution during each repetition, VCFtools will filter SNPs at an interval of 100bp, and the minor allele frequency filter in VCFtools will drop any loci with a minor allele frequency less than 0.05. Any individuals not present in popmap.txt will also be removed before Admixture is executed:
```
admixturePipeline.py -m popmap.txt -v input.vcf -k 1 -K 10 -n 16 -t 100 -a 0.05
```

Alternatively, you can provide PLINK files as input. Text-based PLINK files (.ped and .map) should be equivalent to those output using the --recode12 option in PLINK. Specify the PLINK file prefix to use this option, as shown in the example below.
```
admixturePipeline.py -m popmap.txt -p input -k 1 -K 10 -n 16
```

A similar command is used to provide a pre-filtered binary PLINK file (.bed, .fam, and .bim). 
```
admixturePipeline.py -m popmap.txt -b input -k 1 -K 10 -n 16
```

## Outputs:<a name="admixoutputs"></a>

For the example code above, the following outputs will be produced:
* **input.ped**, **input.map**: text-based PLINK files in --recode12 format (produced only if you input a VCF file)
* **results.zip**: a compressed results file (**CLUMPAK input**)
* **input.{k}\_{r}.P** and **input.{k}\_{r}.Q**: Admixture output files for each iteration {r} of each K value {k}
* **input\_pops.txt**: a list of population data (**CLUMPAK input**)
* **input.recode.strct_in**: a structure-formatted file of filtered SNPs
* **input.qfiles.json**: a json file containing all .Q file names per K value that were produced by this pipeline (new in AdmixPipe v3.1; utilized by runEvalAdmix.py module)

Once you have finished running this stage of the pipeline, you can submit the two above files designated as **CLUMPAK input** to the online resource CLUMPAK (http://clumpak.tau.ac.il/), or use the submitClumpak.py module in the Docker container.

# 2. submitClumpak.py <a name="submitclumpak"></a>

This module was developed to automate the process of submitting admixturePipeline.py results to the CLUMPAK pipeline. As of AdmixPipe v3.1, this module now interacts with the CLUMPAK installation within the Docker container. If you cannot or do not want to use the Docker container, you can [manually configure](#clumpakinstall) a Linux computer to make this module interact with the CLUMPAK webserver. If you do not want to use this module at all, manual submission to the CLUMPAK webserver remains a viable and easy option that will not significantly disrupt the pipeline flow.

## Usage:<a name="clumpakusage"></a>

### Docker or local execution
**The -M and -b options are utilized to run locally on your machine or in the Docker container.**
If running locally or in Docker, you do not need to submit an email address. Executing the CLUMPAK main pipeline in the Docker container can be accomplished as follows:

```
submitClumpak.py -p prefix -M
```

**The input necessary for the BestK pipeline (-b option) is written by cvSum.py. If you want to use this function, return here after running [distructRerun.py](#distructrerun) and [cvSum.py](#cvsum)** You can execute this part of CLUMPAK locally through the Docker container with the following command. It should be issued from the directory where you executed cvSum.py. 

```
submitClumpak.py -b
```

### Webserver
**A friendly reminder: the webserver submission function does not work in the Docker container.** 
Change directories into the folder where the admixturePipeline.py module wrote all output. Execute submitClumpak.py from this directory. The only things you must specify are the prefix of your VCF file (i.e., the VCF file name without the .vcf extension), an email address which is submitted to the online CLUMPAK server, and the boolean option to submit to the server (-w). For example:

```
submitClumpak.py -p prefix -e email@domain.com -w
```

List of current options:<a name="clumpakoptions"></a>
* **-b / --bestk:** Run the CLUMPAK BestK pipeline locally in the Docker container (or on your computer if you performed a manual install of CLUMPAK). 
* **-d / --DISTRUCT:** \[optional\] Provide user-defined DISTRUCT threshold for minimal distruct cluster threshold. Must be >=0 and <=0.95.
* **-e / --email:** Specify your email address for submission to the CLUMPAK web server.
* **-m / --MCL:** \[optional\] Provide user-defined MCL threshold for similarity scores. Must be >=0 and <=0.99.
* **-M / --mainpipeline:** Run the CLUMPAK main pipeline locally in the Docker container (or on your computer).
* **-p / --prefix:** Specify the prefix from your admixpipe run. This will either be the prefix of your plink file (i.e., without .bed or .map extension), or same name as your VCF file without the .vcf file extension.
* **-r / --results:** Provide the results.zip file from your admixpipe run. Specifying the name is only necessary if you have changed it from the default of 'results.zip'.
* **-w / --web:** Submit your results to the main pipeline of the CLUMPAK web server (option not available in the Docker container).

## Outputs:<a name="clumpakoutputs"></a>

The -w option of the module does not write any output to your computer. You must retrieve the zipped CLUMPAK output from their webserver after your job completes running. The `wget` command is available from within the Docker container for this purpose.

The -b or -M options will write output to your computer. Output from -M will be written to a `clumpakOutput/` subdirectory in the folder from which you executed submitClumpak.py. Output of -b will be written to the `clumpakBestK/` subdirectory. When run locally, CLUMPAK will produce zip archives similar to those that you download from the webserver. In other words, the zip archives will be named as a 13 digit number (i.e., a Unix milliseconds timestamp based upon the time of pipeline execution). 

# 3. distructRerun.py <a name="distructrerun"></a>

This module is designed to streamline the process of re-running distruct on the major and minor clusters found by CLUMPAK. 

## Usage:<a name="distructusage"></a>

If necessary, download your results from the CLUMPAK server. This should give you a zipped folder of your results, named something like "1516030453.zip". If you are using the Docker container, obtain the result of the submitClumpak.py module from your `clumpakOutput/` subdirectory. You should put this file into the "data" folder created on your computer when you launched Docker through the runDocker.sh script. First, unzip this folder:

```
unzip 1516030453.zip
```

This should produce a folder in your current directory named 1516030453.  Now, run distructRerun.py on your folder.  The command will be something like the below command.  In this example, -a is used to provide the path to the directory of results produced by admixturePipeline.py, -d is used to give the name of the directory that the program will use as input, -k (lower case) specifies the lowest clustering value that you tested in Admixture, and -K (upper case) specifies the highest clustering value you tested.

```
distructRerun.py -a example_admixturePipeline_result/ -d 1516030453/ -k 1 -K 12
```

This should have produced a file named MajorClusterRuns.txt in the directory from which you executed distructRerun.py.  This file contains all of the names of the .stdout files produced by my admixturePipeline repository that correspond to each of the major clusters recovered by CLUMPAK. AdmixPipe v3.1 also produces a similar file for each Minor Cluster detected by CLUMPAK (if any were present). These will be named 'MinorClusterRuns.K{i}.{j}, where '{i}' is the associated K value, and '{j}' represents sequentially numbered minor clusters. You should also have a file named cv_file.MajClust.txt that contains all of the CV values for your major cluster runs, and a separate file for each minor cluster (e.g., cv_file.MinClust.K{i}.{j}.  Finally, if you have chosen to run distruct itself (by invoking the -r option), then distruct will return a postscript file (.ps) for each major and minor cluster of each K value that you evaluated. These .ps files will appear in a 'best_results' subdirectory within your CLUMPAK output folder (e.g., '1516030453/best_results/' for the above example). The rest of the processing can be accomplished through cvSum.py and runEvalAdmix.py.

If you did not have the pipeline automatically execute distruct, you can do it manually using the drawparams files output by distructRerun.py. For example:

```
distruct -d drawparams.8
```

As of AdmixPipe v3.1, ghostscript is now installed in the Docker container. Any .ps files can be converted to .pdf with the `ps2pdf` command. For example:

```
ps2pdf K8.ps
```

List of current options:<a name="distructoptions"></a>
* **-a / --ad:** Specify the directory containing the output of your admixturePipeline.py run (required).
* **-c / --colorbrew:** Specify a color palette from the colorbrewer options in distruct 1.1. Enter the prefix of the color palette you want (for example, BrBG) and the pipeline will take care of adding the appropriate K value and palette suffix. If a palette is not available at a particular K value, then distruct will revert to the default palette. (optional, default = BrBG)
* **-d / --directory:** Specify the directory containing the output of your CLUMPAK run (required).
* **-k / --minK:** Specify the minimum K value to be tested (required).
* **-K / --maxK:** Specify the maximum K value to be tested (required).
* **-m / --majc:** Provide the name of the output file that will hold the names of runs corresponding to the major clusters (optional; default = MajorClusterRuns.txt)
* **-p / --pathtocolorbrew:** Specify the full path to the location of distruct1.1's colorbrewer files on your computer (not necessary if you are using the Docker container). 
* **-r / --run:** Boolean switch. Using this option will run distruct for each drawparams file. (optional, default = off)
* **-w / --width:** Provide the width of each individual bar in the distruct output (optional; default = 2).

Experimental options:
* **-l / --otl:** Specify a custom toplabels file. This option may allow you to utilize the distructRerun.py segment of this pipeline on STRUCTURE data processed by CLUMPAK. This has not been robustly tested. Use at your own risk.

## Outputs:<a name="distructoutputs"></a>

The following outputs will be produced in the directory where distructRerun.py was executed:
* **MajorClusterRuns.txt**: contains all of the names of the .stdout files produced by admixturePipeline.py that correspond to each of the major clusters recovered by CLUMPAK.
* **MinorClusterRuns.K{i}.{j}**: contains the names of the .stdout files associated with the jth minor cluster for K=i. These files will not appear if there were no minor clusters detected by CLUMPAK.
* **cv_file.MajClust.txt**: CV values for all of the major clusters
* **cv_file.MinClust.K{i}.{j}**: CV values for the jth minor cluster for K=i. These files will not appear if there were no minor clusters detected by CLUMPAK.
* **loglikelihood_file.MajClust.txt**: Loglikelihood values for all of the major clusters
* **loglikelihood_file.MinClust.K{i}.{j}**: Loglikelihood values for the jth minor cluster for K=i. These files will not appear if there were no minor clusters detected by CLUMPAK.
* **cvRuns.json**: Run names associated with each major and minor cluster, stored in JSON format. This file is stored in your admixturePipeline.py output directory, and will be utilized by runEvalAdmix.py.
* **qfilePaths.json**: CLUMPP output .Q files associated with each major and minor cluster, stored in JSON format. This file is stored in your admixturePipeline.py output directory, and will be utilized by runEvalAdmix.py.

# 4. cvSum.py <a name="cvsum"></a>

This code was written to graphically summarize the variability of cross-validation values and log likelihood scores across multiple runs of admixture.

## Usage:<a name="cvusage"></a>
Execute the cvSum.py script in the directory containing your cv_file.MajClust.txt and loglikelihood_file.MajClust.txt outputs from distructRerun.py to generate the summary information for your major and minor cluster runs identified by CLUMPAK. Generally no command line options are required unless you have changed names of files output by prior modules of this pipeline. For example:

```
cvSum.py
```

The first output of this program is a plot of boxplots representing the variation in the CV values found by different runs of ADMIXTURE.  The X axis of the plot corresponds to K values, while the Y axis corresponds to the CV values.  Lower CV values are preferred.  The plot file name will be same as your input file, but with a .png extension (i.e., "cv_file.MajClust.png"). Boxplots for minor clusters, if present, are plotted alongside the major cluster CV value distributions in this same plot. The summary statistics are saved in a file named "cv_output.txt" unless you use the -o option to specify a custom file name.  As of version 3.1, the same summary statistics and boxplots are presented for loglikelihood values.

List of current options:<a name="cvoptions"></a>
* **-c / --cv:** Specify the name of your file with cross-validation values for your admixture runs (optional, default = cv_file.MajClust.txt).
* **-l / --ll:** Specify the name of your file with loglikelihood values for your admixture runs (optional, default = loglikelihood.MajClust.txt).
* **-o / --out:** Specify the name of your cv value output file (optional, default = cv_output.txt).
* **-L / --llout:** Specify the name of your loglikelihood output file (optional, default = loglikelihood_output.txt).

## Outputs:<a name="cvoutputs"></a>

The following outputs will be produced in the directory where cvSum.py was executed:
* **cv_file.MajClust.png**: Boxplot chart providing a visual summary of your your CV values for both major and minor cluster runs.
* **cv_output.txt**: Text file containing summary statistics of CV values for each K.
* **loglikelihood_file.MajClust.png**: Boxplot chart providing a visual summary of your your loglikelihood values for both major and minor cluster runs.
* **loglikelihood_output.txt**: Text file containing summary statistics of loglikelihood values for each K.
* **ll_all.txt**: Text file containing log likelihood values for each replicate. This output is compatible with the BestK pipeline in CLUMPAK.

# 5. runEvalAdmix.py <a name="runevaladmix"></a>

This module aids in evaluating appropriateness of K values by running the evalAdmix program on each Admixture replicate, as well as the summarized .Q outputs from CLUMPAK for all major and minor clusters. 

## Usage:<a name="evalusage"></a>
Change directories to the folder containing the output from admixturePipeline.py. You must be in this folder to execute commands for runEvalAdmix.py because it requires JSON files that were written in this location by other pipeline modules (specifically, admixturePipeline.py and distructRerun.py). These are new outputs as of AdmixPipe v3.1, so you cannot execute the runEvalAdmix.py module on outputs from earlier AdmixPipe versions. The following is an example command for this module:

```
runEvalAdmix.py -p prefix -k 1 -K 12 -m popmap.txt -n 8
```

The above command will first execute PLINK to convert your .ped file to a .bed file. Then it will run evalAdmix on all original .Q files produced by admixturePipeline.py before finally running evalAdmix on the .Q outputs for major and minor clusters identified by CLUMPAK. The plots for the major and minor clusters are produced by averaging across the .corres files produced for each run corresponding to a particular major or minor cluster, then input into evalAdmix using the .Q scores file for that cluster which was output by CLUMPP when the CLUMPAK pipeline was run.

If you ran admixturePipeline.py by directly inputting a pre-filtered .bed file, then you must indicate this with the -b/--bed option as shown below. This allows evalAdmix to use your original .bed file rather than perform unnecessary file conversions:
```
runEvalAdmix.py -p prefix -k 1 -K 12 -m popmap.txt -n 8 -b
```

List of current options:<a name="evaloptions"></a>
* **-b / --bed:** Boolean switch to indicate that you originally ran admixturePipeline.py by directly inputting a pre-filtered .bed file (default = off/False).
* **-p / --prefix:** Specify your .ped or .bed file prefix from your initial admixturePipeline.py run. If you input a VCF file, this will be the name of that VCF file, except without the .vcf extension (required).
* **-k / --minK:** Specify the minimum K value (required).
* **-K / --maxK:** Specify the maximum K value (required).
* **-m / --popmap:** Specify a tab-delimited population map (sample --> population) (required).
* **-M / --mc:** Provide path to the file that will hold names of runs corresponding to the major clusters (optional; should not be necessary unless you have renamed files or specified custom names).
* **-R / --evalAdmixRcode:** Provide the path to where visualization functions for evalAdmix are stored on your machine. (Not necessary if using the Docker container)
* **-n / --np:** Provide the number of processors to use for evalAdmix (optional; default=1).

## Outputs:<a name="evaloutputs"></a>

The following outputs will be produced in the directory where runEvalAdmix.py was executed:
* **prefix.{i}\_{j}.corres**: Matrix produced by R code in visFuns.R for the jth run at K=i.
* **prefix.{i}\_{j}.corres.png**: Plot produced by R code in visFuns.R from the prefix.{i}\_{j}.corres file for the jth run at K=i
* **{i}.png**: Plot produced by R code in visFuns.R summarizing the major cluster at K=i. 
* **{i}.MinClust.{j}.png**: Plot produced by R code in visFuns.R summarizing the jth minor cluster at K=i.


# Manual Installation <a name="manualinstall"></a>
Manual installation is possible, but not advised. If you must install manually, you should get started by cloning this repository and making sure that Python 3.8 or higher is installed. Under Ubuntu, I install the following packages to ensure everything necessary is installed for Python:

```
apt-get install python3.8 python3-pip python3-setuptools python3-dev
```

Then install the program dependencies listed below. Having administrator privileges will make manual configuration easier. Many installation commands are provided assuming you are using Ubuntu, or some other Debian-based distribution. You might need to independently determine equivalent commands or package names on your operating system if you are not using Ubuntu.

## Program Dependencies
The complete pipeline has six external program dependencies that must be installed. The modules from which they are called are listed below each program name:
* **Admixture** (https://dalexander.github.io/admixture/download.html)
  * admixturePipeline.py
* **CLUMPAK** (http://clumpak.tau.ac.il/download/CLUMPAK.zip)
  * submitClumpak.py
* **distruct** (https://rosenberglab.stanford.edu/distructDownload.html)
  * distructRerun.py
* **evalAdmix** (https://github.com/GenisGE/evalAdmix)
  * runEvalAdmix.py
* **PLINK 1.9 beta 4.5 or newer** (https://www.cog-genomics.org/plink2)
  * admixturePipeline.py
  * runEvalAdmix.py
* **VCFtools** (https://vcftools.github.io/index.html)
  * admixturePipeline.py

It is advised that you install the latest version of each program manually. For example, admixturePipeline.py utilizes options in PLINK and VCFtools that are sometimes absent from the versions of these programs curated within repositories of some Linux package managers. Each program should be added to your $PATH as the lowercase version of its name (i.e., 'plink', 'vcftools', 'admixture', 'distruct') with the exception of evalAdmix (which should be in your $PATH as 'evalAdmix'). Special instructions are also provided below for manual installation of CLUMPAK. Additionally, you must make sure the vcf-query script from the vcftools package is present in your $PATH because it is now required by the admixturePipeline.py script. If you installed vcftools through the "sudo make install" method, then this should have already happened. 

You may also have to modify the first line of each of the five AdmixPipe v3.1 module files (admixturePipeline.py, submitClumpak.py, distructRerun.py, cvSum.py, and runEvalAdmix.py). By default, the first line of each reads:
```
#!/usr/bin/env python3
```

To find the location of your Python installation, you can type the following at the bash command prompt:
```
which python3
```
This will return your /path/to/python3. Then modify the first line of each module to reflect the location of your python3 installation.

Other dependencies (mainly Python libraries) are required for some modules. These dependencies are discussed with their associated modules below. I have provided instructions for each module separately because installation difficulty varies from one module to the next. Your utilization of AdmixPipe may not require all modules depending upon the goals of your study.

## Special Instructions for Each Module:
1. [admixturePipeline.py](#admixinstall)
2. [submitClumpak.py](#clumpakinstall)
3. [distructRerun.py](#distructinstall)
4. [cvSum.py](#cvinstall)
5. [runEvalAdmix.py](#evalinstall)

### Installation and Setup for admixturePipeline.py:<a name="admixinstall"></a>

There are no additional dependencies for this module, assuming you have already installed the latest versions of Admixture, PLINK, and VCFtools (including vcf-query) as described above. 

### Installation & Setup for submitClumpak.py:<a name="clumpakinstall"></a>

Manual configuration of this module can be complicated depending upon your desired functionality (webserver utilization vs. local CLUMPAK installation), and your operating system. 

#### Webserver Configuration

Webserver configuration is relatively easy for Ubuntu users because it just requires installation of selenium (Python library) and the Firefox gecko driver, both of which can be installed from package repositories. 

This module has three requirements for usage with the CLUMPAK webserver:
1. selenium (python library)
2. Firefox web browser
3. Firefox gecko driver (firefox-geckodriver)

Currently, Firefox is the only supported web browser. Installation of selenium and the gecko driver can be accomplished with the following commands (you may have to run each as 'sudo' depending upon your system configuration and/or use a different package manager and/or package name for the gecko driver installation if you are not using Ubuntu or another Debian-based distribution):

selenium:
```
pip3 install selenium
```

gecko driver:
```
apt-get install firefox-geckodriver
```
#### Local CLUMPAK Installation

Manual installation of CLUMPAK can be achieved, but I highly recommend 1) using the Docker container or 2) manually submitting your admixturePipeline.py results to the CLUMPAK webserver as alternatives. This is because manual CLUMPAK installation requires several dependencies and modifications of the CLUMPAK code. But if you insist on conducting a full manual installation of AdmixPipe, here is how I got it running in the Docker container: 

Most dependencies can be installed through Ubuntu's repositories. You may need to use alternate commands or determine equivalent package names if using a different Linux distribution:
```
apt-get install libgetopt-long-descriptive-perl \
 libfile-slurp-perl \
 libfile-path-tiny-perl \
 liblist-moreutils-perl \
 libpdf-api2-perl \
 libpdf-table-perl \
 libgd-graph-perl \
 libscalar-list-utils-perl \
 libscalar-util-numeric-perl \
 libstatistics-distributions-perl \
 libarchive-extract-perl \
 libarray-utils-perl \
 libarchive-zip-perl \
 ghostscript
```

The perl [List::Permutor](https://metacpan.org/pod/List::Permutor) package also must also be installed. I am not aware of an Ubuntu repository containing this package. Here's how to do a manual install once you have downloaded the List::Permutor package code:

```
tar -zxvf List-Permutor-0.022.tar.gz
cd List-Permutor-0.022
perl Makefile.PL
make
sudo make install
```

The CLUMPAK source code is available [here](http://clumpak.tau.ac.il/download/CLUMPAK.zip). Download it and unzip the file. 
Some of the CLUMPAK perl scripts have issues that must be corrected before they can be used. 
1. Some have Windows line breaks. The dos2unix program in Ubuntu can fix these for you (`sudo apt-get install dos2unix`). Go into the `CLUMPAK/26_03_2015_CLUMPAK/CLUMPAK/` folder and run it on all .pl files to be make sure these are fixed. 
2. The 'BestKByEvanno.pl' script is missing the `#!/usr/bin/perl` at the beginning. 
3. Make sure all scripts are executable. 
4. Copy all .pm files to a location monitored by perl's @INC variable. In the Docker container, I copied them to /etc/perl. You may need sudo permissions to access /etc/perl on your computer. Alternatively, [here's a way to install perl modules in your home directory](https://kb.iu.edu/d/baiu) if you do not have admin privileges.

Once you have downloaded the CLUMPAK.zip file, the following commands will perform the above 4 corrections. The last `cp` command may require admin privileges. 
```
unzip CLUMPAK.zip
cd CLUMPAK/26_03_2015_CLUMPAK/CLUMPAK
dos2unix *.pl
sed -i '1s/^/\#!\/usr\/bin\/perl\n/' BestKByEvanno.pl
chmod u+x *.pl
cp *.pm /etc/perl/.
```

Next, make sure you have CLUMPP, distruct1.1, and mcl installed. Also set them to be executable with the `chmod` command. All of these programs are included in the CLUMPAK.zip file you downloaded. 

You also need to modify a few of the .pm files with the path to CLUMPP, distruct, and mcl on your system. For example, here's how I accomplished this with `sed` commands in the Docker container setup. Just replace `\/app\/src\/clumpak` with the location where you unzipped the CLUMPAK.zip file on your computer.

```
sed -i 's/CLUMPP\//\/app\/src\/clumpak\/CLUMPAK\/26_03_2015_CLUMPAK\/CLUMPAK\/CLUMPP\//g' ClumppAccessor.pm
sed -i 's/mcl\/bin\//\/app\/src\/clumpak\/CLUMPAK\/26_03_2015_CLUMPAK\/CLUMPAK\/mcl\/bin\//g' MCLAccessor.pm 
sed -i 's/distruct\//\/app\/src\/clumpak\/CLUMPAK\/26_03_2015_CLUMPAK\/CLUMPAK\/distruct\//g' ClusterAccessor.pm
```

Finally, make sure the `CLUMPAK.pl` and `BestKByEvanno.pl` scripts are located in a directory monitored by your $PATH. 

### Installation & Setup for distructRerun.py:<a name="distructinstall"></a>

There are no additional dependencies required for distructRerun.py (assuming you have already installed distruct itself). However, it is advised if you want to use the colorbrewer options in distruct that you modify the default location of the ColorBrewer palettes in the distructComline.py file (line 61) so that you do not need to specify this path each time you run this module. I also recommend you place the ColorBrewer folder in your home directory (e.g., `/home/username/ColorBrewer`). Burying it several directories deep on your system will prevent it from being read properly due to a bug in distruct. 

### Installation & Setup for cvSum.py:<a name="cvinstall"></a>

Two additional python3 libraries required for this module: **matplotlib** and **pandas**. Each can be installed via `pip3`. Commands may need to be run as 'sudo' depending upon your system configuration:

```
pip3 install pandas
pip3 install matplotlib
```

### Installation and Setup for runEvalAdmix.py:<a name="evalinstall"></a>

This module can be particularly challenging to configure manually, so this is my final plea to **please just use the Docker container**. This module has several requirements in addition to installation of the evalAdmix program itself and PLINK. First, two python3 libraries are required: pandas and rpy2. Specifically, a recent version of rpy2 (>= v3.4) is required.

```
pip3 install pandas
pip3 install rpy2
```

R (>= version 4.0.2) is required. It's possible that this can be installed through Ubuntu repositories. To accomplish this, I install the following under Ubuntu. If you use another OS, you might need to figure out the exact package that ensures the libR.so shared library is installed.

```
apt-get install r-base r-base-dev
```

In the event that installing R from your Linux distribution's package manager fails, then I advise compiling and installing from source because rpy2 will not work if the libR.so library is statically linked to R. If you go down this route, I provide an example of how to do this while installing R to a custom location. First, download the source code for R from `https://cran.r-project.org/src/base/R-4/`. Follow the commands below, and replace '/path/to/install/' with your preferred installation directory. Additionally, I want to stress the importance of running ./configure with the --enable-R-shlib command. This is absolutely vital to creating the dynamically-linked libR.so library which allows rpy2 to function properly.

```
tar -zxvf R-4.0.2.tar.gz
cd R-4.0.2/
./configure --prefix=/path/to/install/ --enable-R-shlib
make
sudo make install
```

After installing R from source, you may also need to set the $LD_LIBRARY_PATH of your system so that rpy2 knows where to find the libR.so library. To accomplish this, you can add the below 'export' command to your ~/.bashrc file. If you do not want to permanently pollute your $LD_LIBRARY_PATH variable with this new location, then you will need to run this command whenever you open a new terminal window to execute runEvalAdmix.py. Again, '/path/to/install' is the location where you chose to install R when running the ./configure command in the above code block.

```
export LD_LIBRARY_PATH="/path/to/install/lib/R/lib/:$LD_LIBRARY_PATH"
```

Lastly, the runEvalAdmix.py module requires the location of the 'visFuns.R' file that is included in the evalAdmix package (https://github.com/GenisGE/evalAdmix). You can specify this location via command line input whenever the program is run; however, I would recommend modifying the evalAdmixComline.py file included with AdmixPipe so that you do not need to do this. You can specify your path to 'visFuns.R' on line 46 of this file.
