#!/bin/bash

kill -9 `ps -ef | grep eastbay | grep -v grep | awk '{print $2}'`

for file in ` ls *astbay*.sh `  
do  
	./$file
done  
