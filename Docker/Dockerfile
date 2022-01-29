FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base r-base-dev python3.6 python3-pip python3-setuptools python3-dev git autoconf automake

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

## Install PLINK
RUN mkdir -p /app/src/plink
WORKDIR /app/src/plink
COPY plink_linux_x86_64_20210606.zip /app/src/plink
RUN unzip /app/src/plink/plink_linux_x86_64_20210606.zip

## Install VCFtools
RUN mkdir -p /app/src/vcftools
WORKDIR /app/src/vcftools
COPY vcftools-vcftools-v0.1.16-18-g581c231.zip /app/src/vcftools
RUN unzip /app/src/vcftools/vcftools-vcftools-v0.1.16-18-g581c231.zip
WORKDIR /app/src/vcftools/vcftools-vcftools-581c231/
RUN ./autogen.sh
RUN ./configure
RUN make
RUN make install

## Install Admixture
RUN mkdir -p /app/src/admixture
WORKDIR /app/src/admixture
COPY admixture_linux-1.3.0.tar.gz /app/src/admixture
RUN tar -zxvf /app/src/admixture/admixture_linux-1.3.0.tar.gz

## Install distruct
RUN mkdir -p /app/src/distruct
WORKDIR /app/src/distruct
COPY distruct1.1.tar.gz /app/src/distruct
RUN tar -zxvf /app/src/distruct/distruct1.1.tar.gz

## Install evalAdmix
RUN mkdir -p /app/src/evaladmix
WORKDIR /app/src/evaladmix
COPY evalAdmix-master.zip /app/src/evaladmix
RUN unzip /app/src/evaladmix/evalAdmix-master.zip
WORKDIR /app/src/evaladmix/evalAdmix-master
RUN make

## link binaries and scripts
# make bin directory
RUN mkdir -p /app/bin
WORKDIR /app/bin

# link binaries
RUN ln -s /app/src/plink/plink
RUN ln -s /app/src/admixture/dist/admixture_linux-1.3.0/admixture
RUN ln -s /app/src/distruct/distruct1.1/distructLinux1.1 distruct
RUN ln -s /app/src/evaladmix/evalAdmix-master/evalAdmix

## Install AdmixPipe
RUN mkdir -p /app/scripts/python 
WORKDIR /app/scripts/python
RUN git clone https://github.com/stevemussmann/admixturePipeline.git
WORKDIR /app/scripts/python/admixturePipeline
RUN sed -i 's/\/home\/mussmann\/local\/src\/distruct1.1\/ColorBrewer\//\/app\/ColorBrewer\//g' distructComline.py
RUN sed -i 's/\/home\/mussmann\/local\/src\/evalAdmix\/visFuns.R/\/app\/src\/evaladmix\/evalAdmix-master\/visFuns.R/g' evalAdmixComline.py

#echo /app/bin to path
RUN echo "export PATH=/app/bin:/app/scripts/python/admixturePipeline:${PATH}" >> /root/.bashrc

## Move stuff around
RUN mv /app/src/distruct/distruct1.1/ColorBrewer /app/.

WORKDIR /app
