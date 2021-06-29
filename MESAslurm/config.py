#path to folder that contains the mesa executable

mesa_root_dir = '/scratch/schanlaridis/privatemodules/mesa-r15140'
mesa_directory = '/home/schanlaridis/MESAslurm/Slurm/work'
out_directory = '/home/schanlaridis/core_he_burn/zsol_eta1p0'
script_directory = '/home/schanlaridis/MESAslurm'


#Can explore up to three variables

variable1 = {'name': 'initial_mass',
             'location': 'inlist_var',
             'type': 'array',
             'minimum': 0.8,
             'maximum': 3.5,
             'step': 0.1,
}

variable2 = {'name': 'initial_z',
             'location': 'inlist_var',
             'type': 'predetermined_array',
             #'values': [0.0001,0.001,0.02]
	'values': [0.02]
}

variable3 = {'name': 'wind_scaling_factor',
             'location': 'inlist_var',
             'type': 'predetermined_array',
             #'values': [0.1, 0.5, 2.0, 10.0]
		'values': [1.0]
}
