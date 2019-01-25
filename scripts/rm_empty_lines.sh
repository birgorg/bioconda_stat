#!/bin/sh
files="/home/fuan/Documents/birc/bioconda_stat/results/*.txt"
for i in $files
do
  sed '/^$/d' $i > $i.out 
  mv  $i.out $i
done
