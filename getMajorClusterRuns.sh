#!/bin/bash

# Use this script to take all of the runs corresponding to the major clusters and put them into a file named "MajorClusterRuns.txt"

echo -n "" > MajorClusterRuns.txt

for file in K\=*/MajorCluster/clusterFiles
do 
	cat $file >> MajorClusterRuns.txt
done

sed -i 's/Q\.converted/stdout/g' MajorClusterRuns.txt

exit
