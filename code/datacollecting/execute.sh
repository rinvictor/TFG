#!/bin/sh

#Con este script se pretende controlar el flujo de accion de la aplicación de tal manera que 
#se ejecutara cada X minutos el script 'db_conn.py' en el caso de la salida sea errónea se
#debe repetir la ejecución.
export PYTHONPATH="PYTHONPATH:/home/pi/TFG/code/modules"

path=/home/pi/TFG/code/datacollecting

cd $path #Pongo esto para poder ejecutarlo desde fuera del diectorio, ya que si no daría problemas de dependencias
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
	#en algunas ocasiones salta el error 'StatisticsError' por la lista vacia
	#es un error que se da por la mala lectura de los sensores, pero volviendo a ejecutar se soluciona
	python db_conn.py
	#Si tras esta ejecución vuelve a fallar pruebo 2 veces más, si no funciona FATAL ERROR
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
