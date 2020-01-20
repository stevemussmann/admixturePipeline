# Admixture Pipeline: A Method for Parsing and Filtering VCF Files for Admixture Analysis
A pipeline that accepts a VCF file to run through Admixture

## Example Files

Here we provide example files to test the pipeline. The example VCF file has been compressed because its uncompressed size exceeds the maximum file size limit of github (50MB). You can uncompress it with the following command:

```
tar -zxvf example.vcf.tar.gz
```

This should produce a new file named **example.vcf** with a size of approximately 57MB. The example popmap file is presented here as **example_map.txt**

## Running the pipeline with the example files:

You can run the program to validate that it works by running the following command. This will run the pipeline for two iterations each on K=1 and K=2. 

```
admixturePipeline.py -m example_map.txt -v example.vcf -k 1 -K 2 -R 2
```
