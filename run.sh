#!/usr/bin/env bash
#SBATCH -N 1
#SBATCH -c 32
#SBATCH --mem 64G

python datacleaner.py
