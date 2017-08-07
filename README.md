# admixturePipeline
A pipeline that accepts a VCF file to run through Admixture

## Installation:

This pipeline was written to be run on Unix based operating systems, such as the various Linux distributions and Mac OS X.  To get started, clone this project to the desired location on your computer.  

This pipeline has three dependencies that must be installed:
* PLINK 1.9 beta 4.5 or newer (https://www.cog-genomics.org/plink2)
* VCFtools (https://vcftools.github.io/index.html)
* Admixture (https://www.genetics.ucla.edu/software/admixture/download.html)

The VCFtools package can be installed on Ubuntu, the following command should work:
```
sudo apt-get install vcftools
```
The PLINK version in the standard Ubuntu repository is unsupported.  Please install it and Admixture manually.  The executable for each program should be the lowercase version of its name (i.e., plink, vcftools, admixture), and should be placed in your path.  

## Running the script:

You can run the program to print help options with the following command:

```
./admixturePipeline.py -h
```
