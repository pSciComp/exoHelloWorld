#!/bin/bash
#SBATCH --job-name=helloworld
# Get the account with
# sacctmgr show assoc user=<username> format=User,Account%50
#SBATCH --account=<group.department.uni>
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --output=logs/%j.out

module load apptainer

apptainer run \
  --bind ./data/raw:/app/data/raw \
  --bind ./data/final:/app/data/final \
  exohw-env_1.0.0.sif \
  python scripts/say_hello.py
