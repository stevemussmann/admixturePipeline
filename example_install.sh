#!/bin/bash

echo "###############################################################################################################"
echo "## PLEASE READ BEFORE PROCEEDING. THIS IS AN EXAMPLE OF HOW TO INSTALL THE PIPELINE AND ALL DEPENDENCIES.    ##"
echo "## THIS INSTALL SCRIPT WAS DESIGNED TO WORK ON UBUNTU 18.04. SOME COMMANDS WILL VARY IF YOU ARE WORKING ON   ##"
echo "## A MAC OR OTHER UNIX-BASED OPERATING SYSTEM. OPEN THIS FILE IN A TEXT EDITOR TO VIEW THE INSTALLATION      ##"
echo "## EXAMPLE WITHOUT RUNNING IT.                                                                               ##"
echo "###############################################################################################################"

read -r -p "Are you sure you want to continue? [Y/n] " input
 
case $input in
    [yY][eE][sS]|[yY])
 echo "Yes"
 ;;
    [nN][oO]|[nN])
 echo "No"
 exit 1
       ;;
    *)
 echo "Invalid input..."
 exit 1
 ;;
esac

## Make directories to hold the source code (src), links to binaries (bin), and python scripts (scripts/python)
mkdir -p $HOME/local/src $HOME/local/bin $HOME/local/scripts/python

## Move into the directory for the python scripts
cd $HOME/local/scripts/python

## Clone the admixturePipeline.py repository
git clone https://github.com/stevemussmann/admixturePipeline.git

## Move to your source code directory
cd $HOME/local/src

## Get copies of all dependency programs
## VCFtools
git clone https://github.com/vcftools/vcftools.git
## ADMIXTURE
wget http://software.genetics.ucla.edu/admixture/binaries/admixture_linux-1.3.0.tar.gz
## DISTRUCT
wget https://rosenberglab.stanford.edu/software/distruct1.1.tar.gz

## Make a directory to hold PLINK
mkdir $HOME/local/src/plink
cd $HOME/local/src/plink
## Download PLINK
wget http://s3.amazonaws.com/plink1-assets/plink_linux_x86_64_20200121.zip

## unzip files
cd $HOME/local/src
tar -zxvf admixture_linux-1.3.0.tar.gz
tar -zxvf distruct1.1.tar.gz
cd $HOME/local/src/plink
unzip plink_linux_x86_64_20200121.zip

## Build VCFtools
cd $HOME/local/src/vcftools
./autogen.sh
./configure
make

## Link all binaries and python scripts
## Each dependencies should be the lower case version of its name
cd $HOME/local/bin
ln -s $HOME/local/src/vcftools/src/cpp/vcftools vcftools
ln -s $HOME/local/src/plink/plink plink
ln -s $HOME/local/src/admixture_linux-1.3.0/admixture admixture
ln -s $HOME/local/src/distruct1.1/distructLinux1.1 distruct
ln -s $HOME/local/scripts/python/admixturePipeline/admixturePipeline.py
ln -s $HOME/local/scripts/python/admixturePipeline/cvSum.py
ln -s $HOME/local/scripts/python/admixturePipeline/distructRerun.py

## Make sure your $HOME/local/bin folder is in your path
echo 'export PATH=$HOME/local/bin:$PATH' >> $HOME/.bashrc

exit
