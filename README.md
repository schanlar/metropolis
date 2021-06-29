# MESAslurm
Scripts to submit jobs at [Slurm](https://slurm.schedmd.com/overview.html) cluster manager

## Download
You can download the repository as a zip file, or by typing

```bash
 ~$ git clone https://github.com/schanlar/MESAslurm.git
```

in a terminal window.

## Initialize and Run
**Step 0-1** : Open the template for the batch script required to submit jobs at Slurm.
You can change the directives depending on your needs (e.g. number of nodes, cpus per task etc).
**DO NOT** modify the script besides the directives that are meant to be used with Slurm (the ones starting with ``#SBATCH``).

**Step 0-2** : Open the template for the inlist and set the paths to keep the caches separately.
This is important because the main mesa directory is located in a system directory that requires "root" access to write.
Thus, the caches must be moved out of the main directory to locations that the user can write (see [here](http://mesa.sourceforge.net/star_job_defaults.html#cache_directories) for details).

**Step 1** : Open ``config.py`` using the editor of your choice.

**Step 2** : Specify the paths for the ``MESA`` stellar evolution code (check their [site](http://mesa.sourceforge.net/)),
the output directory etc.

> Warning: You need to create a copy of the ``work`` directory used in MESA.
You also need to specify the absolute path to this copied version using the ``mesa_directory`` variable.

**Step 3** : Create your stellar grid. You can explore up to 3 variables at a time (courtesy of John Antoniadis).
In our case, these 3 variables refer to ``initial mass``, ``initial metallicity``, and ``wind efficiency``.
If you want to explore other variables, you need to modify the inlist template accordingly.

**Step 4** : Save your changes and then run the ``submit_jobs.py`` script.
