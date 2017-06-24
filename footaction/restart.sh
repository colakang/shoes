#!/bin/bash

kill -9 `ps -ef | grep footaction | grep -v grep | awk '{print $2}'`

for file in ` ls *ootaction*.sh `  
do  
	./$file
done  
