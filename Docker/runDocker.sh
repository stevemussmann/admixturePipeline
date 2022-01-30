#!/bin/bash

# get working directory
dir=`pwd`

# make data folder in current folder if it doesn't exist.
if [ -d ${dir}/data ]
then
	echo "Directory \"${dir}/data\" already exists on your machine."
	echo "You can copy your data for AdmixPipe into this directory and"
	echo "it will be accessible at \"/app/data\" in the Docker container."
	echo ""
	echo ""
else
	mkdir ${dir}/data
	echo "Directory ${dir}/data was created on your machine."
	echo "You can copy your data for AdmixPipe into this directory and"
	echo "it will be accessible at \"/app/data\" in the Docker container."
	echo ""
	echo ""
fi

# run docker container
echo "Starting docker container for mussmann/admixpipe."
echo ""
echo "Type \"exit\" at the command prompt to exit the container."
echo "Only data saved in \"/app/data\" will be retrievable after exiting."
echo "All data saved in other locations within the container will"
echo "be lost upon exiting."
echo ""
echo ""

docker container run -v ${dir}/data/:/app/data --rm -it mussmann/admixpipe:3.0 /bin/bash

exit
