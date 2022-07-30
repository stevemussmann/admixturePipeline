[![DOI](https://zenodo.org/badge/96546673.svg)](https://zenodo.org/badge/latestdoi/96546673)

# AdmixPipe v3: A Method for Parsing and Filtering VCF Files for Admixture Analysis
A pipeline that accepts a VCF file to run through Admixture

## Citing AdmixPipe
AdmixPipe v2.0 is published in BMC Bioinformatics. A manuscript is currently in preparation for v3.0. For now, you should cite the publication below if you use any part of this pipeline:

S.M. Mussmann, M.R. Douglas, T.K. Chafin, M.E. Douglas 2020. AdmixPipe: population analyses in ADMIXTURE for non-model organisms. BMC Bioinformatics 21:337. DOI: 10.1186/s12859-020-03701-4

## IMPORTANT NOTE ON v3.0 (30-January-2022)

The remainder of this README.md file details documentation for AdmixPipe v3.0, which has several "behind the scenes" changes, bug fixes, and enhancements to existing modules. Two new modules have also been developed for the following purposes: 
1) automatic submission of admixturePipeline.py output to the CLUMPAK website.
2) assessment of the best K using the evalAdmix package (http://www.popgen.dk/software/index.php/EvalAdmix). 

Some of the outputs from AdmixPipe v2.0 are not compatible with the v3.0 scripts because I use json files to track data and file names from early parts of the pipeline that are needed in some of the later modules. If you need to use the v2.0 scripts for any reason, they are still available from the prior releases on this page (v2.0.2 was the final release of AdmixPipe v2.0).  

Other important notes for v3.0: 
1) whereas AdmixPipe v2.0 was backward compatible with Python 2.7.x, v3.0+ requires Python 3.
2) Some command line options have changed slightly (especially long form commands - you can get the current list of commands by running any module with the --help option).
3) There is now a Docker container to streamline the installation process.
4) The submitClumpak.py module is **completely optional**. You can accomplish the same results by manually submitting your admixturePipeline.py module outputs to the CLUMPAK website. 
5) The submitClumpak.py module will not function in the Docker container. If you wish to use it, this module must be set up on your own computer. It requires selenium and currently is only compatible if you have Firefox installed. 
6) The data processing and plotting functions of the cvSum.py module underwent a complete rewrite for v3.0.

## Installation & Setup for AdmixPipe v3:

### Docker Setup
This pipeline was written for Unix based operating systems, such as the various Linux distributions and Mac OS X. As of v3.0, we have achieved platform independence and greater ease of installation through development of a Docker container. This is now the recommended method for running the program. To get started, install [Docker](https://www.docker.com/) on your machine and pull the Docker image using the following command:

```
docker pull mussmann/admixpipe:3.0
```

Launch the container by placing the "runDocker.sh" script in the folder from which you want to run the container, then executing it as shown below. This script can be found in the "Docker" folder of this github repository.
```
./runDocker.sh
```
This script creates a folder named "data" in the directory on your machine from which you launched the Docker container. You can put any input files for AdmixPipe v3.0 into this folder and they will be accessible inside the container (in /app/data/). Any outputs written to this folder and any of its subdirectories will still be accessible after you exit the container. If you write any output to other locations inside the container, they will be lost upon exit. All required AdmixPipe modules (i.e., all except submitClumpak.py) have been setup within the container and will function with the commands provided throughout the remainder of this documentation. 

### Manual Setup
Due to the many (sometimes complex) dependencies required by this pipeline, manual installation is not advised. However, if you insist upon installing the pipeline manually, you should get started by cloning this repository. Then install the program dependencies listed below. 

#### Program Dependencies
The complete pipeline has five external program dependencies that must be installed. The modules from which they are called are listed below each program name:
* **PLINK 1.9 beta 4.5 or newer** (https://www.cog-genomics.org/plink2)
  * admixturePipeline.py
  * runEvalAdmix.py
* **VCFtools** (https://vcftools.github.io/index.html)
  * admixturePipeline.py
* **Admixture** (https://dalexander.github.io/admixture/download.html)
  * admixturePipeline.py
* **distruct** (https://rosenberglab.stanford.edu/distructDownload.html)
  * distructRerun.py
* **evalAdmix** (https://github.com/GenisGE/evalAdmix)
  * runEvalAdmix.py

It is advised that you install the latest version of each program manually. For example, admixturePipeline.py utilizes options in PLINK and VCFtools that are not present in the versions curated within the standard Ubuntu repositories. Each program should be added to your $PATH as the lowercase version of its name (i.e., 'plink', 'vcftools', 'admixture', 'distruct') with the exception of evalAdmix (which should be in your path as 'evalAdmix'). Additionally, you must make sure the vcf-query script from the vcftools package is present in your $PATH because it is now required by the admixturePipeline.py script. If you installed vcftools through the "sudo make install" method, then this should have already happened. 

You may also have to modify the first line of each of the five module files (admixturePipeline.py, submitClumpak.py, distructRerun.py, cvSum.py, and runEvalAdmix.py). By default, the first line of each reads:
```
#!/usr/bin/env python3
```

To find the location of your Python installation, you can type the following at the bash command prompt:
```
which python3
```
This will return your /path/to/python3. Then modify the first line of each module to reflect the location of your python3 installation.

Other dependencies (mainly Python libraries) are also required for some of the modules. These dependencies are discussed alongside their associated modules below.

# Running AdmixPipe v3

AdmixPipe v3 is composed of five different modules. Follow the links below in the table of contents to find specific instructions for running each module.

### Table of Contents:
1. [admixturePipeline.py](#admixturepipeline)
2. [submitClumpak.py](#submitclumpak)
3. [distructRerun.py](#distructrerun)
4. [cvSum.py](#cvsum)
5. [runEvalAdmix.py](#runevaladmix)

# 1. admixturePipeline.py: <a name="admixturepipeline"></a>

**New feature in AdmixPipe v3.0:** This module will now filter out individuals not present in your popmap file. For example, if you want to exclude an individual sample from your analysis, just leave it out of your popmap file and it will be removed from your vcf file before admixture is executed. 

You can run the program to print help options with the following command:

```
./admixturePipeline.py -h
```

List of current required options:
* **-m / --popmap:** Specify a tab-delimited population map (sample --> population).  This will be converted to a population list that can be input into a pipeline such as CLUMPAK (http://clumpak.tau.ac.il/) for visualization of data
* **-v / --vcf:** Specify a VCF file for input.

Optional arguments:
* **-n / --np:** Specify the number of processors.  Currently the only multithreaded program is Admixture.

Admixture optional arguments:
* **-k / --minK:** Specify the minimum K value to be tested (default = 1).
* **-K / --maxK:** Specify the maximum K value to be tested (default = 20).
* **-c / --cv:** Specify the cross-validation number for the admixture program.  See the admixture program manual for more information (default = 20)
* **-R / --rep:** Specify the number of replicates for each K value (default = 20)

VCFtools optional arguments:
* **-M / --mac:** Enter the minimum count for the minor allele filter. (default = off, specify a positive integer to turn it on).
* **-a / --maf:** Enter a minimum frequency for the minor allele frequency filter. (default = off, specify a value between 0.0 and 1.0 to turn it on).
* **-b / --bi:** Turns biallelic filter off. (default = on, **we do not recommend turning this setting off because ADMIXTURE only processes biallelic SNPs**)  
* **-r / --remove:** Provide a blacklist of individuals that will be filtered out by VCFtools. This is a textfile with each name on its own line. Names of individuals must match those in the .vcf file exactly. 
* **-t / --thin:** Filter loci by thinning out any loci falling within the specified proximity to one another, measured in basepairs.  (default = off, specify an integer greater than 0 to turn it on).
* **-C / --indcov:** Filter samples based on maximum allowable missing data. Feature added by tkchafin. (default = 0.9, input = float). 
* **-S / --snpcov:** Filter SNPs based on proportion of allowable missing data. Feature added by tkchafin. (default = 0.1; defined to be between 0 and 1, where 0 allows sites that are completely missing and 1 indicates no missing data allowed; input = float).

## Example:

The following command will run the program from K values 1 through 10, conducting 10 repetitions at each K value.  Admixture will use all 16 processors available on the hypothetical machine, VCFtools will filter SNPs at an interval of 100bp, and the minor allele frequency filter in VCFtools will drop any loci with a minor allele frequency less than 0.05. Any individuals not present in popmap.txt will also be filtered out before Admixture is executed:

```
admixturePipeline.py -m popmap.txt -v input.vcf -k 1 -K 10 -n 16 -t 100 -a 0.05
```

## Outputs:

For the example line of code above, the following outputs will be produced:
* **input.ped**, **input.map**: output of plink
* **results.zip**: a compressed file that can be input into a pipeline such as CLUMPAK
* **input.{k}\_{r}.P** and **input.{k}\_{r}.Q**: Admixture output files for each iteration {r} of each K value {k}
* **input\_pops.txt**: a list of population data that can be input into a pipeline such as CLUMPAK
* **input.recode.strct_in**: a structure-formatted file of filtered SNPs
* **input.qfiles.json**: a json file containing all .Q file names per K value that were produced by this pipeline (new in AdmixPipe v3; required for runEvalAdmix.py module) 

Once you have finished running this stage of the pipeline, you can submit the two above files designated as CLUMPAK inputs to the online resource CLUMPAK (http://clumpak.tau.ac.il/). Once that analysis finishes, you can continue on with the pipeline using distructRerun.py

# 2. submitClumpak.py <a name="submitclumpak"></a>

This module was developed to automate the process of submitting admixturePipeline.py results to the CLUMPAK website (http://clumpak.tau.ac.il/). This module is **completely optional** because the same results can be accomplished by manually submitting your files to the CLUMPAK server. **You can skip this module and instead submit your files manually to the CLUMPAK server if you are using the Docker container.** Because it is optional, it is also the only module not functional in the Docker container. If you want to use this module, you will have to configure it on your own machine. Fortunately, this is easy for Ubuntu users because it just requires installation of selenium (a Python library) and the Firefox gecko driver, both of which can be installed from package repositories.

## Installation & Setup for submitClumpak.py:

This module has three requirements:
1. selenium (python library)
2. Firefox web browser
3. Firefox gecko driver (firefox-geckodriver)

Currently, Firefox is the only supported web browser. Assuming you already have Firefox installed, you will only need to install selenium and the gecko driver. These can be accomplished with the following commands (you may have to run each as 'sudo' depending upon your system configuration and/or use a different package manager and/or package name for the gecko driver installation if you are not using Ubuntu or another Debian-based distribution):

selenium:
```
pip3 install selenium
```

gecko driver:
```
apt-get install firefox-geckodriver
```

Once all dependencies are installed, you can run the program to print help options with the following command:

```
submitClumpak.py -h
```

## Usage:

Change directories into the folder where the admixturePipeline.py module wrote all output. Execute submitClumpak.py from this directory. The only things you must specify are the prefix of your VCF file (i.e., the VCF file name without the .vcf extension) and an email address which is submitted to the online CLUMPAK server. For example:

```
submitClumpak.py -p prefix -e email@domain.com
```

List of current options:
* **-r / --results:** Provide the results.zip file from your admixpipe run. Specifying the name is only necessary if you have changed it from the default of 'results.zip'.
* **-p / --prefix:** Specify the prefix from your admixpipe run. This will be the same name as your VCF file without the .vcf file extension.
* **-e / --email:** Specify your email address for submission to the CLUMPAK web server.
* **-m / --MCL:** \[optional\] Provide user-defined MCL threshold for similarity scores. Must be >=0 and <=0.99.
* **-d / --DISTRUCT:** \[optional\] Provide user-defined DISTRUCT threshold for minimal distruct cluster threshold. Must be >=0 and <=0.95.

## Outputs:

This module does not write any output to your computer. You must retrieve the zipped CLUMPAK output from their webserver after your job completes running.

# 3. distructRerun.py <a name="distructrerun"></a>

This code was written to help streamline the process of re-running distruct on the major and minor clusters that are found by CLUMPAK. This code was written with the intention of operating on CLUMPAK analysis of ADMIXTURE data, however an experimental option has been added that will allow you to run this section of the pipeline on CLUMPAK analysis of STRUCTURE data.

## Installation & Setup for distructRerun.py:

You can skip reading this paragraph if you are using the Docker container. If you installed the pipeline manually, there are no additional dependencies required for distructRerun.py (assuming you have already installed distruct itself). However, it is advised if you want to use the colorbrewer options in distruct that you modify the default location of the ColorBrewer palettes in the distructComline.py file (line 61) so that you do not need to specify this path each time you run this module.

## Usage:

Download your results from the CLUMPAK server. This should give you a zipped folder of your results, named something like "1516030453.zip". If you are using the Docker container, you should put this file into the "data" folder created on your computer when you launched Docker through the runDocker.sh script. First, unzip this folder:
```
unzip 1516030453.zip
```
This should produce a folder in your current directory named 1516030453.  Now, run distructRerun.py on your folder.  The command will be something like the below command.  In this example, -a is used to provide the path to the directory of results produced by admixturePipeline.py, -d is used to give the name of the directory that the program will use as input, -k (lower case) specifies the lowest clustering value that you tested in Admixture, and -K (upper case) specifies the highest clustering value you tested.

```
distructRerun.py -a example_admixturePipeline_result/ -d 1516030453/ -k 1 -K 12
```
This should have produced a file named MajorClusterRuns.txt in the directory from which you executed distructRerun.py.  This file contains all of the names of the .stdout files produced by my admixturePipeline repository that correspond to each of the major clusters recovered by CLUMPAK. AdmixPipe v3 also produces a similar file for each Minor Cluster detected by CLUMPAK (if any were present). These will be named 'MinorClusterRuns.K{i}.{j}, where '{i}' is the associated K value, and '{j}' represents sequentially numbered minor clusters. You should also have a file named cv_file.MajClust.txt that contains all of the CV values for your major cluster runs, and a separate file for each minor cluster (e.g., cv_file.MinClust.K{i}.{j}.  Finally, if you have chosen to run distruct itself (by invoking the -r option), then distruct will return a postscript file (.ps) for each major and minor cluster of each K value that you evaluated. These .ps files will appear in a 'best_results' subdirectory within your CLUMPAK output folder (e.g., '1516030453/best_results/' for the above example). The rest of the processing can be accomplished through cvSum.py and runEvalAdmix.py.

List of current options:
* **-a / --ad:** Specify the directory containing the output of your admixturePipeline.py run (required).
* **-c / --colorbrew:** Specify a color palette from the colorbrewer options in distruct 1.1. Enter the prefix of the color palette you want (for example, BrBG) and the pipeline will take care of adding the appropriate K value and palette suffix. If a palette is not available at a particular K value, then distruct will revert to the default palette. (optional, default = BrBG)
* **-d / --directory:** Specify the directory containing the output of your CLUMPAK run (required).
* **-k / --minK:** Specify the minimum K value to be tested (required).
* **-K / --maxK:** Specify the maximum K value to be tested (required).
* **-m / --majc:** Provide the name of the output file that will hold the names of runs corresponding to the major clusters (optional; default = MajorClusterRuns.txt)
* **-p / --pathtocolorbrew:** Specify the full path to the location of distruct1.1's colorbrewer files on your computer. 
* **-r / --run:** Boolean switch. Using this option will run distruct for each drawparams file. (optional, default = off)
* **-w / --width:** Provide the width of each individual bar in the distruct output (optional; default = 2).

Experimental options:
* **-l / --otl:** Specify a custom toplabels file. This option may allow you to utilize the distructRerun.py segment of this pipeline on STRUCTURE data processed by CLUMPAK. This has not been robustly tested. Use at your own risk.

## Outputs:

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

This code was written to summarize the variability of cross-validation values across multiple runs of admixture.

## Installation & Setup for cvSum.py:

You can skip this paragraph if you are running the Docker container. If you installed the pipeline manually, there are some additional libraries you need to install. The plotting and data processing functions of cvSum.py underwent a complete rewrite in AdmixPipe v3. There are now two additional python3 libraries required for this module: **matplotlib** and **pandas**. Each can be installed by the following. Commands may need to be run as 'sudo' depending upon your system configuration:
```
pip3 install pandas
pip3 install matplotlib
```

## Usage:
It is assumed that you have already processed your data with admixturePipeline.py and distructRerun.py. Simply execute the cvSum.py script in the directory containing your cv_file.MajClust.txt and loglikelihood_file.MajClust.txt outputs from distructRerun.py to generate the summary information for your major and minor cluster runs identified by CLUMPAK.

The output of this program is a plot of boxplots representing the variation in the CV values found by different runs of ADMIXTURE.  The X axis of the plot corresponds to K values, while the Y axis corresponds to the CV values.  Lower CV values are preferred.  The plot file name will be same as your input file, but with a .png extension (i.e., "cv_file.MajClust.png"). Boxplots for minor clusters, if present, are plotted alongside the major cluster CV value distributions in this same plot. The summary statistics are saved in a file named "cv_output.txt" unless you use the -o option to specify a custom file name.  As of version 3.0.2, the same summary statistics and boxplots are also prepared by this module for loglikelihood values.

List of current options:
* **-c / --cv:** Specify the name of your file with cross-validation values for your admixture runs (optional, default = cv_file.MajClust.txt).
* **-l / --ll:** Specify the name of your file with loglikelihood values for your admixture runs (optional, default = loglikelihood.MajClust.txt).
* **-o / --out:** Specify the name of your cv value output file (optional, default = cv_output.txt).
* **-L / --llout:** Specify the name of your loglikelihood output file (optional, default = loglikelihood_output.txt).

## Outputs:

The following outputs will be produced in the directory where cvSum.py was executed:
* **cv_file.MajClust.png**: Boxplot chart providing a visual summary of your your CV values for both major and minor cluster runs.
* **cv_output.txt**: Text file containing summary statistics of CV values for each K.
* **loglikelihood_file.MajClust.png**: Boxplot chart providing a visual summary of your your loglikelihood values for both major and minor cluster runs.
* **loglikelihood_output.txt**: Text file containing summary statistics of loglikelihood values for each K.

# 5. runEvalAdmix.py <a name="runevaladmix"></a>

This code was written to aid in identifying the best K value by running the evalAdmix program on each individual run of Admixture, as well as the summarized .Q outputs from CLUMPAK for all major and minor clusters. 

## Installation and Setup for runEvalAdmix.py:

If you are using the Docker container, you can skip over this section and keep reading at the "Usage" section. This module can be particularly challenging to configure manually, so consider this your last warning to **please just use the Docker container**. This module has several requirements in addition to installation of the evalAdmix program itself and PLINK. First, two python3 libraries are required: pandas and rpy2. Specifically, a recent version of rpy2 (>= v3.4) is required.
```
pip3 install pandas
pip3 install rpy2
```

R (>= version 4.0.2) is also required. I advise compiling and installing from source because rpy2 will not work if the libR.so library is statically linked to R. If you go down this route, I provide an example of how to do this while installing R to a custom location. First, download the source code for R from https://cran.r-project.org/src/base/R-4/. Follow the commands below, and replace '/path/to/install/' with your preferred installation directory. Additionally, I want to stress the importance of running ./configure with the --enable-R-shlib command. This is absolutely vital to creating the dynamically-linked libR.so library which allows rpy2 to function properly.
```
tar -zxvf R-4.0.2.tar.gz
cd R-4.0.2/
./configure --prefix=/path/to/install/ --enable-R-shlib
make
sudo make install
```
After installing R from source, you may also need to set the $LD_LIBRARY_PATH of your system so that rpy2 knows where to find the libR.so library. To accomplish this, you can add the below 'export' command to your ~/.bashrc file. If you do not want to permanently pollute your $LD_LIBRARY_PATH variable with this new location, then you will need to run this command whenever you open a new terminal window to execute runEvalAdmix.py. Again, '/path/to/install' is the location where you chose to install R when running the ./configure command in the above block of code.

```
export LD_LIBRARY_PATH="/path/to/install/lib/R/lib/:$LD_LIBRARY_PATH"
```
Lastly, the runEvalAdmix.py module requires the location of the 'visFuns.R' file that is included in the evalAdmix package (https://github.com/GenisGE/evalAdmix). You can specify this location via command line input whenever the program is run; however, I would recommend modifying the evalAdmixComline.py file included with AdmixPipe so that you do not need to do this. You can specify your path to 'visFuns.R' on line 41 of this file.

## Usage:
Change directories to the folder containing the output from admixturePipeline.py. You must be in this folder to execute commands for runEvalAdmix.py because it requires JSON files that were written in this location by some of the earlier modules of this pipeline that you ran (specifically, admixturePipeline.py and distructRerun.py). These are new outputs as of AdmixPipe v3, so you cannot execute the runEvalAdmix.py module on outputs from earlier versions of AdmixPipe. The following is an example command for this module:
```
runEvalAdmix.py -p prefix -k 1 -K 12 -m popmap.txt -n 8
```
The above command will first execute PLINK to convert your .ped file to a .bed file. Then it will run evalAdmix on all original .Q files produced by admixturePipeline.py before finally running evalAdmix on the .Q outputs for major and minor clusters identified by CLUMPAK. The plots for the major and minor clusters are produced by averaging across the .corres files produced for each run corresponding to a particular major or minor cluster, then input into evalAdmix using the .Q scores file for that cluster which was output by CLUMPP when the CLUMPAK pipeline was run.

List of current options:
* **-p / --prefix:** Specify your .ped file prefix from your initial admixturePipeline.py run. This should be the same as the name of your original input VCF file, except without the .vcf extension (required).
* **-k / --minK:** Specify the minimum K value (required).
* **-K / --maxK:** Specify the maximum K value (required).
* **-m / --popmap:** Specify a tab-delimited population map (sample --> population) (required).  
* **-M / --mc:** Provide path to the file that will hold names of runs corresponding to the major clusters (optional; should not be necessary unless you have renamed files or specified custom names).
* **-R / --evalAdmixRcode:** Provide the path to where visualization functions for evalAdmix are stored on your machine.
* **-n / --np:** Provide the number of processors to use for evalAdmix (optional; default=1).

## Outputs:

The following outputs will be produced in the directory where runEvalAdmix.py was executed:
* **prefix.{i}\_{j}.corres**: Matrix produced by R code in visFuns.R for the jth run at K=i.
* **prefix.{i}\_{j}.corres.png**: Plot produced by R code in visFuns.R from the prefix.{i}\_{j}.corres file for the jth run at K=i
* **{i}.png**: Plot produced by R code in visFuns.R summarizing the major cluster at K=i. 
* **{i}.MinClust.{j}.png**: Plot produced by R code in visFuns.R summarizing the jth minor cluster at K=i. 
