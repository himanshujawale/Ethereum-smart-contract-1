filenames=`ls -l | grep '^-' | awk '{print $9}'`
[ -d "data_log" ] && echo "ok" || echo -e "Data log \n Directory Creating...." $(mkdir data_log) 

temp=1
for eachfile in $filenames
do
  if [ "${eachfile: -4}" == ".sol" ]  #check sol file extension. 
  then

        myth analyze $eachfile &> log_$temp   # execute myth analyze on Smart Contract  and save result inside  log file
        mv log_$temp data_log/                # move all log file in data_log folder 
        echo task $temp Completed
  fi
  ((temp=temp+1))
done

