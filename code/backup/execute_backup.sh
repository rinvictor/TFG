#!/bin/sh
export PYTHONPATH="PYTHONPATH:/home/pi/TFG/code/modules"

path=/home/pi/TFG/code/backup
cd $path
out=$(python3 backup.py)
status=$(echo $?)

now=$(date)

if test $status -eq 0
then
        echo $now "success" $out >>$path/logs/success.log
        echo "" >> $path/logs/success.log
else
        echo $now "error in backup.py" $out >> $path/logs/error.log
        echo "" >> $path/logs/error.log
fi
