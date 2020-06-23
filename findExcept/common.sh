#!/bin/sh

printLog(){
        if [ ! -z "$3" ]; then
                printf "[%s:%d]-[%s]\n" "$1" "$3" "$2"
        else
                #printf "[%s]-[%s]\n" "$1" "$2"
                printf "%s: %s\n" "$1" "$2"
        fi
}

delimiter(){
	colSize=`tput cols`
	deliChar="="
	deliLine=""
	
	i=0
#	for((i=0;i<${colSize};i++))
	while true
	do
		if [ ${i} -ge ${colSize} ]; then
			break
		else
			deliLine=${deliLine}${deliChar}
			i=`expr ${i} + 1`
		fi
	done

	echo ${deliLine}
}
