#!/bin/bash
#SBATCH --job-name=hello-parallel
# Get the account with
# sacctmgr show assoc user=<username> format=User,Account%50
#SBATCH --account=<group.department.uni>
#SBATCH --array=0-2
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:10:00
#SBATCH --output=logs/%A_%a.out

module load apptainer

apptainer run \
  --env COURSE_ID=$SLURM_ARRAY_TASK_ID \
  --bind ./data/raw:/app/data/raw \
  --bind ./data/final:/app/data/final \
  exohw-env_2.0.0.sif \
  python scripts/say_hello.py
