#!/bin/bash

rm eastbay/debug/* -f
rm eastbay/log/* -f
rm footaction/debug/* -f
rm footaction/log/* -f
rm footlocker/debug/* -f
rm footlocker/log/* -f
rm champssports/debug/* -f
rm champssports/log/* -f

for file in ` ls eastbay/*Eastbay*.sh `  
do  
	rm $file
done  

for file in ` ls footlocker/*Footlocker*.sh `  
do  
	rm $file
done  

for file in ` ls footaction/*Footaction*.sh `  
do  
	rm $file
done  

for file in ` ls champssports/*Champssports*.sh `  
do  
	rm $file
done  

