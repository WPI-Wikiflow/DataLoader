#!/usr/bin/env bash
#SBATCH -N 1
#SBATCH -c 10
#SBATCH --mem 30G

python dataLoader.py
