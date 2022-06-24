#!/bin/sh

export PYTHONPATH="PYTHONPATH:/home/pi/TFG/code/modules"

path=/home/pi/TFG/code/datacollecting

cd $path
out=$(python db_conn.py)
status=$(echo $?)

now=$(date)
if test $status -eq 0
then
	echo $now "success" $out >> $path/logs/success.log
	echo "" >> $path/logs/success.log
else 
	echo $now "exec error" $out >> $path/logs/error.log
	echo "" >> $path/logs/error.log
	python db_conn.py
	status=$(echo $?)
	if test $status -eq 0
	then
		echo $now "success in second attempt" $out >> $path/logs/success.log
		echo "" >> $path/logs/success.log
		exit 0
	else
		for i in 1 2; do
			sleep 1
			python db_conn.py
			status=$(echo $?)
			if test $status -eq 0
			then
				echo $now "success in " $i " ececution, third attempt" $out >> $path/logs/success.log
				echo "" >> $path/logs/success.log
				exit 0
			fi
		done
		echo $now "FATAL ERROR" $out >> $path/logs/error.log
		echo "" >> $path/logs/error.log
		exit 0
	fi
fi
