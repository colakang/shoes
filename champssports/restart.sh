#!/bin/bash

kill -9 `ps -ef | grep champssports | grep -v grep | awk '{print $2}'`

for file in ` ls *Champssports*.sh `  
do  
	./$file
done  
