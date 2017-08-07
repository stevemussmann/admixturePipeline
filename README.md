# admixturePipeline
A pipeline that accepts a VCF file to run through Admixture

## Installation:

This pipeline was written to be run on Unix based operating systems, such as the various Linux distributions and Mac OS X.  To get started, clone this project to the desired location on your computer.  

This pipeline has three dependencies that must be installed:
* PLINK 1.9 beta 4.5 or newer (https://www.cog-genomics.org/plink2)
* VCFtools (https://vcftools.github.io/index.html)
* Admixture (https://www.genetics.ucla.edu/software/admixture/download.html)

The VCFtools package can be easily installed on Ubuntu.  The following command should work:
```
sudo apt-get install vcftools
```
The PLINK version in the standard Ubuntu repository is unsupported.  Please install it and Admixture manually.  The executable for each program should be the lowercase version of its name (i.e., plink, vcftools, admixture), and should be placed in your path.  

## Running the pipeline:

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

Plink optional arguments:
* **-a / --maf:** Enter a minimum frequency for the minor allele frequency filter.  Number must be entered as an integer.  For example, 1 = 0.01. (default = off, specify an integer greater than 0 to turn it on).

VCFtools optional arguments:
* **-t / --thin:** Filter loci by thinning out any loci falling within the specified proximity to one another, measured in basepairs.  (default = off, specify an integer greater than 0 to turn it on).

## Example:

The following command will run the program from K values 1 through 10, conducting 10 repetitions at each K value.  Admixture will use all 16 processors available on the hypothetical machine, VCFtools will filter SNPs at an interval of 100bp, and the minor allele frequency filter in PLINK will drop any loci with a minor allele frequency less than 0.05:

```
admixturePipeline.py -m popmap.txt -v input.vcf -k 1 -K 10 -n 16 -t 100 -a 5
```

## Outputs:

For the example line of code above, the following outputs will be produced:
* **input.ped**, **input.map**: output of plink
* **results.zip**: a compressed file that can be input into a pipeline such as CLUMPAK
* **loglik.txt**: a file containing the log likelihood values of each iteration of each K value.
* **input.{k}\_{r}.P** and **input.{k}\_{r}.Q**: Admixture output files for each iteration{r} of each K{k} value
* **input\_pops.txt**: a list of population data that can be input into a pipeline such as CLUMPAK
* **input\_cv\_summary.txt**: a list of all CV values produced for each iteration of each K value.  This can be summarized and plotted using another of my repositories: (https://github.com/smussmann82/admixture_cv_sum)
