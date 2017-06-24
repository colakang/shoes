#!/bin/bash

kill -9 `ps -ef | grep footlocker | grep -v grep | awk '{print $2}'`

for file in ` ls *ootlocker*.sh `  
do  
	./$file
done  
