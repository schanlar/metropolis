#!/bin/bash
#SBATCH --job-name=run_mesa_template
#SBATCH --output=job_output.stdout
#SBATCH --error=job_error.stderr
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --time=01-00:00:00
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=schanlar@physics.auth.gr

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

source $MESASDK_ROOT/bin/mesasdk_init.sh

# echo "trying to execute ./mk"
./mk

#module load MESA
# echo "trying to execute ./rn"
./rn
