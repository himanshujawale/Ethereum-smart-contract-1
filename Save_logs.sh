#!/bin/bash
filenames=`ls -l solidity_files | grep '^-' | awk '{print $9}'`
[ -d "data_log" ] && echo "Mythril analyzing..." || echo -e " Directory Creating.... \n Mythril analyzing..." $(mkdir data_log) 

for eachfile in $filenames
do
  if [ "${eachfile: -4}" == ".sol" ]  #check sol file extension. 
  then

        myth analyze solidity_files/$eachfile &> ${eachfile%.*}_log   # execute myth analyze on Smart Contract  and save result inside  log file
        mv log_$temp data_log/                # move all log file in data_log folder 
        echo ${eachfile%.*}_log file created successfully. 
  fi
  
done
