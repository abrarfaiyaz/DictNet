#!/bin/sh
#SBATCH -p standard
#SBATCH -c 24
#SBATCH -t 20:00:00

module load matlab/r2019a

Protocol="$1";
dataName="$2" # replace with $1
matlab -nosplash -r "Protocol = \"$Protocol\";dataName=\"$dataName\";\
        run('DLpN.m');"
