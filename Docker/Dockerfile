FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

ARG USERNAME=admixuser
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG IMAGE_NAME=admixpipe
ARG IMAGE_TAG=3.0
ENV USER $USERNAME
ENV HOME /home/$USERNAME
ENV IMAGE_NAME $IMAGE_NAME
ENV IMAGE_TAG $IMAGE_TAG

RUN apt-get update && apt-get install -y --no-install-recommends build-essential r-base r-base-dev python3.8 python3-pip python3-setuptools python3-dev git autoconf automake vim wget less libgdal-dev perl libgetopt-long-descriptive-perl libfile-slurp-perl libfile-path-tiny-perl liblist-moreutils-perl libpdf-api2-perl libpdf-table-perl libgd-graph-perl libscalar-list-utils-perl libscalar-util-numeric-perl libstatistics-distributions-perl libarchive-extract-perl libarray-utils-perl libarchive-zip-perl dos2unix ghostscript

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip3 install -r requirements.txt

## Install Perl requirements
RUN mkdir -p /app/src/perl
WORKDIR /app/src/perl
COPY List-Permutor-0.022.tar.gz /app/src/perl
RUN tar -zxvf List-Permutor-0.022.tar.gz
WORKDIR /app/src/perl/List-Permutor-0.022
RUN perl Makefile.PL
RUN make
RUN make install

## Install PLINK
RUN mkdir -p /app/src/plink
WORKDIR /app/src/plink
COPY plink_linux_x86_64_20220402.zip /app/src/plink
RUN unzip /app/src/plink/plink_linux_x86_64_20220402.zip

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

## Install CLUMPAK
RUN mkdir -p /app/src/clumpak
WORKDIR /app/src/clumpak
COPY CLUMPAK.zip /app/src/clumpak/.
RUN unzip CLUMPAK.zip 
WORKDIR /app/src/clumpak/CLUMPAK
RUN unzip 26_03_2015_CLUMPAK.zip
WORKDIR /app/src/clumpak/CLUMPAK/26_03_2015_CLUMPAK/CLUMPAK
RUN chmod a+x *.pl
RUN dos2unix *.pl
RUN sed -i '1s/^/\#!\/usr\/bin\/perl\n/' BestKByEvanno.pl
RUN cp *.pm /etc/perl/.
WORKDIR /app/src/clumpak/CLUMPAK/26_03_2015_CLUMPAK/CLUMPAK/CLUMPP
RUN chmod a+x CLUMPP
WORKDIR /app/src/clumpak/CLUMPAK/26_03_2015_CLUMPAK/CLUMPAK/distruct
RUN chmod a+x distruct1.1
WORKDIR /app/src/clumpak/CLUMPAK/26_03_2015_CLUMPAK/CLUMPAK/mcl/bin
RUN chmod a+x *
WORKDIR /etc/perl
RUN sed -i 's/CLUMPP\//\/app\/src\/clumpak\/CLUMPAK\/26_03_2015_CLUMPAK\/CLUMPAK\/CLUMPP\//g' ClumppAccessor.pm
RUN sed -i 's/mcl\/bin\//\/app\/src\/clumpak\/CLUMPAK\/26_03_2015_CLUMPAK\/CLUMPAK\/mcl\/bin\//g' MCLAccessor.pm 
RUN sed -i 's/distruct\//\/app\/src\/clumpak\/CLUMPAK\/26_03_2015_CLUMPAK\/CLUMPAK\/distruct\//g' ClusterAccessor.pm

## link binaries and scripts
# make bin directory
RUN mkdir -p /app/bin
WORKDIR /app/bin

# link binaries
RUN ln -s /app/src/plink/plink
RUN ln -s /app/src/admixture/dist/admixture_linux-1.3.0/admixture
RUN ln -s /app/src/distruct/distruct1.1/distructLinux1.1 distruct
RUN ln -s /app/src/evaladmix/evalAdmix-master/evalAdmix
RUN ln -s /app/src/clumpak/CLUMPAK/26_03_2015_CLUMPAK/CLUMPAK/CLUMPAK.pl
RUN ln -s /app/src/clumpak/CLUMPAK/26_03_2015_CLUMPAK/CLUMPAK/BestKByEvanno.pl

## Install AdmixPipe
RUN mkdir -p /app/scripts/python 
WORKDIR /app/scripts/python
RUN git clone https://github.com/stevemussmann/admixturePipeline.git
WORKDIR /app/scripts/python/admixturePipeline
RUN sed -i 's/\/home\/mussmann\/local\/src\/distruct1.1\/ColorBrewer\//\/app\/ColorBrewer\//g' distructComline.py
RUN sed -i 's/\/home\/mussmann\/local\/src\/evalAdmix\/visFuns.R/\/app\/src\/evaladmix\/evalAdmix-master\/visFuns.R/g' evalAdmixComline.py

## Move stuff around
RUN mv /app/src/distruct/distruct1.1/ColorBrewer /app/.
RUN mkdir -p /app/data
COPY vimrc /home/admixuser/.vimrc

## comment out the following 6 lines for debugging of container as root
RUN groupadd --gid $USER_GID $USERNAME \
	&& adduser --uid $USER_UID --gid $USER_GID --disabled-password $USERNAME \
	--gecos "First LAST,RoomNumber,WorkPhone,HomePhone" \
	&& apt-get update \
	&& chown -R $USERNAME:$USERNAME /home/$USERNAME \
	&& chown $USERNAME /app

#echo /app/bin to path
RUN echo "export PATH=/app/bin:/app/scripts/python/admixturePipeline:${PATH}" >> /home/admixuser/.bashrc

## comment out the following 1 line for debugging as root
USER $USER

WORKDIR /app/data
