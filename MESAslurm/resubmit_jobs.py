from __future__ import print_function
import re
import os
import glob
from file_read_backwards import FileReadBackwards

from tempfile import mkstemp
from shutil import move
from os import fdopen, remove


OutputPath = '/mnt/scratch_a/users/c/csavvas/He_stars_grid/gpu_partition/z0p1_eta1p0'


def replace_line(file_path, old_line, new_line, new_file_path):
    #Create temp file
	fh, abs_path = mkstemp()
	with fdopen(fh,'w') as new_file:
		with open(file_path) as old_file:
			for line in old_file:
				new_file.write(line.replace(old_line, new_line))
	move(abs_path, new_file_path)


def searchOutput(path):
    '''
    Search the terminal log file for the last saved model
    '''

    with FileReadBackwards(path +'/terminal_log') as file:
        for line in file:
            if line.startswith('save ' + path + '/photos/'):
                words = re.split('/|, | ', line)
                if words[-2] == 'photos':
                    break
    return words[-1]


def createBatchScript(path):
    '''
    Create the template for resubmitting jobs to Slurm
    '''

    os.chdir(path)
    os.system('touch restart_job.sh')

    os.system('echo ' + '\#\!/bin/bash >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --job-name=restart_mesa_template >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --output=job_output.stdout >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --error=job_error.stderr >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --partition=batch >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --nodes=1 >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --ntasks-per-node=1 >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --cpus-per-task=10 >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --time=07-00:00:00 >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --mail-type=FAIL >> restart_job.sh')
    os.system('echo ' + '\#\SBATCH --mail-user=schanlar@physics.auth.gr >> restart_job.sh')

    os.system('echo ' + 'export OMP_NUM_THREADS=\$\SLURM_CPUS_PER_TASK >> restart_job.sh')
    os.system('echo ' + 'module rm gcc python >> restart_job.sh')
    os.system('echo ' + 'module load MESA >> restart_job.sh')
    os.system('echo ' + 'source \$\MESASDK_ROOT/bin/mesasdk_init.sh >> restart_job.sh')
    os.system('echo ' + './re >> restart_job.sh')


def restartMesa(path, photo):
    '''
    Modify the template for the batch script
    '''

    os.chdir(path)

    replace_line(os.path.join(path, 'restart_job.sh'),
            '#SBATCH --job-name=restart_mesa_template',
            '#SBATCH --job-name=rMESAjob',
            os.path.join(path, 'restart_job.sh'))

    replace_line(os.path.join(path, 'restart_job.sh'),
            '#SBATCH --output=job_output.stdout',
            '#SBATCH --output=restarted_job_output.stdout',
            os.path.join(path, 'restart_job.sh'))

    replace_line(os.path.join(path, 'restart_job.sh'),
            '#SBATCH --error=job_error.stderr',
            '#SBATCH --error=restarted_job_error.stderr',
            os.path.join(path, 'restart_job.sh'))
    
    replace_line(os.path.join(path, 'restart_job.sh'), 
            './re',
            './re ' + photo,
            os.path.join(path, 'restart_job.sh'))

    os.system('chmod +x ' + os.path.join(path, 'restart_job.sh'))
    os.system('sbatch restart_job.sh')






def main(fullStart=False):

    for path in glob.glob(OutputPath +'/*'):
        restartJob = False

        # Check if the model had not started to begin with
        if fullStart:
            if not os.path.exists(path + '/terminal_log'):
                try:
                    os.system('sbatch run_mesa.sh')
                except Exception as e:
                    print(e)

        # Check if a stderr file exists
        for f in glob.glob(path + '/*_error.stderr'):
            with open(f) as error_file:
                # Check if the model stopped due to time or memory limit
                for line in error_file:
                    if (line.startswith('slurmstepd: error:')) or (line.startswith('date: write error:')):
                        restartJob = True
                        break

        # Check if a stdout file exists
        for f in glob.glob(path + '/*_output.stdout'):
            with open(f) as output_file:
                # Check if the model stopped due to memory limit
                for line in output_file:
                    if line.endswith(': No space left on device'):
                        restartJob = True
                        break 


        if restartJob:
            try:
                photo = searchOutput(path)
                createBatchScript(path)
                restartMesa(path, photo)
                print('Restart photo {} from path {}'.format(photo, path))
            except Exception as e:
                print(e)
                                



if __name__ == "__main__":
    main(fullStart=False)
