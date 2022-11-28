#!/usr/bin/env bash
#SBATCH -N 1
#SBATCH -c 32
#SBATCH --mem 10G
#SBATCH -p long

python doc2vec.py