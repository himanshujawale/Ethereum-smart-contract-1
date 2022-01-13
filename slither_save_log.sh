#!/bin/bash
filenames=`ls -l solidity_files | grep '^-' | awk '{print $9}'`
[ -d "data_log" ] && echo "slither analyzing..." || echo -e " Directory Created \n slither analyzing..." $(mkdir data_log) 

for eachfile in $filenames
do
  if [ "${eachfile: -4}" == ".sol" ]  #check sol file extension. 
  then

        slither solidity_files/$eachfile &> ${eachfile%.*}_log   # execute slither-analyze on Solidity file and save result inside  log file
        mv ${eachfile%.*}_log data_log/                # move all log file in data_log folder 
        echo ${eachfile%.*}_log file created successfully. 
  fi

done
