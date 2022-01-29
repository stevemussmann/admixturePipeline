[![DOI](https://zenodo.org/badge/96546673.svg)](https://zenodo.org/badge/latestdoi/96546673)

# AdmixPipe v3: A Method for Parsing and Filtering VCF Files for Admixture Analysis
A pipeline that accepts a VCF file to run through Admixture

## Citing AdmixPipe
AdmixPipe is now published in BMC Bioinformatics. You should cite the following publication if you use any part of this pipeline:

S.M. Mussmann, M.R. Douglas, T.K. Chafin, M.E. Douglas 2020. AdmixPipe: population analyses in ADMIXTURE for non-model organisms. BMC Bioinformatics 21:337. DOI: 10.1186/s12859-020-03701-4

## IMPORTANT NOTE BEFORE PROCEEDING (19-April-2021)

The remainder of this current README.md file is an early draft of the documentation for AdmixPipe v3, which has several "behind the scenes" changes, bug fixes, and enhancements to existing modules. Two new modules have been developed: 
1) a new module will allow for automatic submission of admixturePipeline.py output to the CLUMPAK website.
2) a second new module will help assess the best K using the evalAdmix package (http://www.popgen.dk/software/index.php/EvalAdmix). 

Consequently, if you do not want to try these experimental features yet, then **I strongly recommend at this time that you download the latest release version (AdmixPipe v2.0.2) rather than clone this repository.**  

If you proceed with cloning the master branch of the repository, I will warn you that: 
1) whereas AdmixPipe v2 was backward compatible with Python 2.7.x, v3 requires Python 3.
2) Some command line options have changed slightly (especially long form commands - you can get the current list of commands by running any module with the --help option).
3) The submitClumpak.py module has not been robustly tested. It requires selenium and currently is only compatible if you have Firefox installed. 
4) the evalAdmix module will require rpy2 which can be a pain to get working on some systems.

## Installation & Setup for AdmixPipe v3:

This pipeline was written to be run on Unix based operating systems, such as the various Linux distributions and Mac OS X.  To get started, clone this repository. If you do not want to utilize the new (and sometimes experimental) features of AdmixPipe v3, then I strongly recommend downloading the version 2.0.2 release. If using v2.0.2, then refer to the README.md file distributed with that release for installation details.

### Program Dependencies
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

It is advised that you install the latest version of each program manually. For example, admixturePipeline.py utilizes options in PLINK and VCFtools that are not present in the versions curated within the standard Ubuntu repositories. Each program should be added to your $PATH as the lowercase version of its name (i.e., 'plink', 'vcftools', 'admixture', 'distruct') with the exception of evalAdmix (which should be in your path as 'evalAdmix'). For an example of how I accomplish this, open the example_install.sh script in a text editor. This script contains commented commands that explain what each step of installation accomplishes. **NOTE: The example_install.sh script has not yet been updated for AdmixPipe v3.**

You may also have to modify the first line of each of the five module files (admixturePipeline.py, submitClumpak.py, distructRerun.py, cvSum.py, and runEvalAdmix.py). By default, the first line of each reads:
```
#!/usr/bin/env python3
```

To find the location of your Python installation, you can type the following at the bash command prompt:
```
which python3
```
This will return your /path/to/python3. Then modify the first line of each module to reflect the location of your python3 installation.

# Running AdmixPipe v3

AdmixPipe v3 is composed of five different modules. This is because some dependencies may be challenging to install on different systems, and I wanted to maximize the utility of the program even in cases where some dependencies prove problematic. Follow the links below in the table of contents to find specific requirements and instructions for running each module.

### Table of Contents:
1. [admixturePipeline.py](#admixturepipeline)
2. [submitClumpak.py](#submitclumpak)
3. [distructRerun.py](#distructrerun)
4. [cvSum.py](#cvsum)
5. [runEvalAdmix.py](#runevaladmix)

# 1. admixturePipeline.py: <a name="admixturepipeline"></a>

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

The following command will run the program from K values 1 through 10, conducting 10 repetitions at each K value.  Admixture will use all 16 processors available on the hypothetical machine, VCFtools will filter SNPs at an interval of 100bp, and the minor allele frequency filter in VCFtools will drop any loci with a minor allele frequency less than 0.05:

```
admixturePipeline.py -m popmap.txt -v input.vcf -k 1 -K 10 -n 16 -t 100 -a 0.05
```

## Outputs:

For the example line of code above, the following outputs will be produced:
* **input.ped**, **input.map**: output of plink
* **results.zip**: a compressed file that can be input into a pipeline such as CLUMPAK
* **loglik.txt**: a file containing the log likelihood values of each iteration of each K value.
* **input.{k}\_{r}.P** and **input.{k}\_{r}.Q**: Admixture output files for each iteration{r} of each K{k} value
* **input\_pops.txt**: a list of population data that can be input into a pipeline such as CLUMPAK
* **input.recode.strct_in**: a structure-formatted file of filtered SNPs
* **input.qfiles.json**: a json file containing all .Q file names per K value that were produced by this pipeline (new in AdmixPipe v3; required for runEvalAdmix.py module) 

Once you have finished running this stage of the pipeline, you can submit the two above files designated as CLUMPAK inputs to the online resource CLUMPAK (http://clumpak.tau.ac.il/). Once that analysis finishes, you can continue on with the pipeline using distructRerun.py

# 2. submitClumpak.py <a name="submitclumpak"></a>

This module was developed to automate the process of submitting admixturePipeline.py results to the CLUMPAK website (http://clumpak.tau.ac.il/). This module is still a work in progress and has not been robustly tested on a variety of systems. I have so far only tested this under Ubuntu 18.04.

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

Currently this module does not write any output to your computer. You must retrieve the zipped CLUMPAK output from their webserver after your job completes running.

# 3. distructRerun.py <a name="distructrerun"></a>

This code was written to help streamline the process of re-running distruct on the major and minor clusters that are found by CLUMPAK.  This code was written with the intention of operating on CLUMPAK analysis of ADMIXTURE data, however an experimental option has been added that will allow you to run this section of the pipeline on CLUMPAK analysis of STRUCTURE data.

## Installation & Setup for distructRerun.py:

There are no additional dependencies for distructRerun.py (assuming you have already installed distruct itself). However, it is advised if you want to use the colorbrewer options in distruct that you modify the default location of the ColorBrewer palettes in the distructComline.py file (line 61) so that you do not need to specify this path each time you run this module.

## Usage:

Download your results from the CLUMPAK server. This should give you a zipped folder of your results, named something like "1516030453.zip".  First, unzip this folder:
```
unzip 1516030453.zip
```
This should produce a folder in your current directory named 1516030453.  Now, run distructRerun.py on your folder.  Assuming that you have installed distructRerun.py somewhere in your path, the command will be something like the below command.  In this example, -a is used to provide the path to the directory of results produced by admixturePipeline.py, -d is used to give the name of the directory that the program will use as input, -k (lower case) specifies the lowest clustering value that you tested in Admixture, and -K (upper case) specifies the highest clustering value you tested.

```
distructRerun.py -a example_admixturePipeline_result/ -d 1516030453/ -k 1 -K 12
```
This should have produced a file named MajorClusterRuns.txt in the directory from which you executed distructRerun.py.  This file contains all of the names of the .stdout files produced by my admixturePipeline repository that correspond to each of the major clusters recovered by CLUMPAK. AdmixPipe v3 also produces a similar file for each Minor Cluster detected by CLUMPAK (if any were present). These will be named something like 'MinorClusterRuns.K{i}.{j}, where '{i}' is the associated K value, and '{j}' represents sequentially numbered minor clusters. You should also have a file named cv_file.MajClust.txt that contains all of the CV values for your major cluster runs, and a separate file for each minor cluster (e.g., cv_file.MinClust.K{i}.{j}.  Finally, if you have chosen to run distruct itself (by invoking the -r option), then distruct will return a postscript file (.ps) for each major and minor cluster of each K value that you evaluated. These .ps files will appear in a 'best_results' subdirectory within your CLUMPAK output folder (e.g., '1516030453/best_results/' for the above example). The rest of the processing can be accomplished through cvSum.py and runEvalAdmix.py.

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
* **cvRuns.json**: Run names associated with each major and minor cluster, stored in JSON format. This file is stored in your admixturePipeline.py output directory, and will be utilized by runEvalAdmix.py.
* **qfilePaths.json**: CLUMPP output .Q files associated with each major and minor cluster, stored in JSON format. This file is stored in your admixturePipeline.py output directory, and will be utilized by runEvalAdmix.py.

# 4. cvSum.py <a name="cvsum"></a>

This code was written to summarize the variability of cross-validation values across multiple runs of admixture.

## Installation & Setup for cvSum.py:

The plotting and data processing functions of cvSum.py underwent a complete rewrite in AdmixPipe v3. There are now two additional python3 libraries required for this module: **matplotlib** and **pandas**. Each can be installed by the following. Commands may need to be run as 'sudo' depending upon your system configuration:
```
pip3 install pandas
pip3 install matplotlib
```

## Usage:
It is assumed that you have already processed your data with admixturePipeline.py and distructRerun.py. Simply execute the cvSum.py script in the directory containing your cv_file.MajClust.txt output from distructRerun.py to generate the summary information for your major and minor cluster runs identified by CLUMPAK.

The output of this program is a plot of boxplots representing the variation in the CV values found by different runs of ADMIXTURE.  The X axis of the plot corresponds to K values, while the Y axis corresponds to the CV values.  Lower CV values are preferred.  The plot file name will be same as your input file, but with a .png extension (i.e., "cv_file.MajClust.png"). Boxplots for minor clusters, if present, are plotted alongside the major cluster CV value distributions in this same plot. The summary statistics are saved in a file named "cv_output.txt" unless you use the -o option to specify a custom file name.  

List of current options:
* **-c / --cv:** Specify the name of your file with cross-validation values for your admixture runs (optional, default = cv_file.MajClust.txt).
* **-o / --out:** Specify the name of your output file (optional, default = cv_output.txt).

## Outputs:

The following outputs will be produced in the directory where cvSum.py was executed:
* **cv_file.MajClust.png**: Boxplot chart providing a visual summary of your your CV values for both major and minor cluster runs.
* **cv_output.txt**: Text file containing summary statistics of CV values for each K.

# 5. runEvalAdmix.py <a name="runevaladmix"></a>

This code was written to aid in identifying the best K value by running the evalAdmix program on each individual run of Admixture, as well as the summarized .Q outputs from CLUMPAK for all major and minor clusters. 

## Installation and Setup for runEvalAdmix.py:

This module has several requirements in addition to installation of the evalAdmix program itself and PLINK. Some requirements are particularly challenging to get functioning correctly. First, two python3 libraries are required: pandas and rpy2. Specifically, a recent version of rpy2 (>= v3.4) is required.
```
pip3 install pandas
pip3 install rpy2
```

R (>= version 4.0.2) is also required. I advise compiling and installing from source because rpy2 will not work if the libR.so library is statically linked to R. If you go down this route, I provide an example of how to do this while installing R to a custom location. First, download the source code for R from https://cran.r-project.org/src/base/R-4/ (I recommend version 4.0.2 because I have only tested this module with this version). Follow the following commands, and replace '/path/to/install/' with your preferred installation directory. Additionally, I want to stress the importance of running ./configure with the --enable-R-shlib command. This is absolutely vital to creating the dynamically-linked libR.so library which allows rpy2 to function properly.
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
* **-p / --prefix:** Specify your .ped file previx from your initial admixturePipeline.py run. This should be the same as the name of your original input VCF file, except without the .vcf extension (required).
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
