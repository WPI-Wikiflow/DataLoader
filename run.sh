#!/usr/bin/env bash
#SBATCH -N 1
#SBATCH -c 10
#SBATCH -t 10:00:00
#SBATCH --mem 10G

python dataloader.py