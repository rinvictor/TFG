#!/bin/sh
export PYTHONPATH="PYTHONPATH:/home/pi/TFG/code/modules:/home/pi/TFG/code/datacollecting"
path=/home/pi/TFG/code/apps/actions
cd $path
out=$(python3 actions.py)
status=$(echo $?)

now=$(date)

if test $status -eq 0
then
        echo $now "success" $out >>$path/logs/success.log
        echo "" >> $path/logs/success.log
else
        echo $now "error in actions.py" $out >> $path/logs/error.log
        echo "" >> $path/logs/error.log
fi
