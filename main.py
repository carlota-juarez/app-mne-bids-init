# This file is a MNE python-based brainlife.io App

# Carlota Juárez Alonso

# Set up enviroment
import sys
import json
import os
import subprocess
from shutil import copyfile
import mne_bids_pipeline

# Current path 
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Path to mne-study-template
mnest_path = '/mne-bids-pipeline'

# Read the parameters 
with open (os.path.join(__location__, 'config.json')) as f:
    config = json.load(f)

# Entry and output paths 
bids_root = str(config['bids'])
deriv_root = os.path.join(__location__, 'out_dir')

# Verify the output file
if not os.path.exists(deriv_root):
    os.makedirs(deriv_root)

# Rewrite the info in the .json file into a .py file
file_name = os.path.join(__location__, 'pipeline_config.py')

# Inputs from the interface web to MNE variables
with open(file_name, 'w') as f:
    # -- General settings --

    f.write(f"bids_root = '{bids_root}'\n")
    f.write(f"deriv_root = '{deriv_root}'\n")

    if config['sessions']:
        f.write(f"sessions = {config['sessions']}\n")

    if config['allow_missing_sessions']:
        f.write(f"allow_missing_sessions = {config['allow_missing_sessions']}\n")

    if config['task']:
        f.write(f"task = '{config['task']}'\n")

    if config['runs']:
        f.write(f"runs = {config['runs']}\n")
    
    if config['exclude_runs']:
        f.write(f"exclude_runs = {config['exclude_runs']}\n")

    if config['crop_runs']:
        f.write(f"crop_runs = {config['crop_runs']}\n")
    
    if config['proc']:
        f.write(f"proc = '{config['proc']}'\n")

    if config['rec']:
        f.write(f"rec = '{config['rec']}'\n")

    if config['space']:
        f.write(f"space = '{config['space']}'\n")
    
    if config['acq']:
        f.write(f"acq = '{config['acq']}'\n")
    
    if config['conditions']:   
        f.write(f"conditions = {config['conditions']}\n")
    
    if config['subjects']:
        f.write(f"subjects = {config['subjects']}\n")

    if config['exclude_subjects']:
        f.write(f"exclude_subjects = {config['exclude_subjects']}\n")

    if config['task_is_rest']:
        f.write(f"task_is_rest = {config['task_is_rest']}\n")

    if config['interactive']:
        f.write(f"interactive = {config['interactive']}\n")

    # -- EEG configurations --

    if config['ch_types']: 
        f.write(f"ch_types = {config['ch_types']}\n")

    if config['data_type']:
        f.write(f"data_type = '{config['data_type']}'\n")

    if config['eeg_reference']:
        f.write(f"eeg_reference = '{config['eeg_reference']}'\n")
    else:
        f.write("eeg_reference = 'average'\n")
    
    f.close()

# Run python script

os.system(mnest_path+'/_run.py --config='+__location__+'/mne_config.py --steps=preprocessing,report/make_reports.py')


# Find the reports and make a copy in out_html folder
for dirpaths, dirnames, filenames in os.walk(deriv_root):
    for filename in [f for f in filenames if f.endswith(".html")]:
        if not "sub-average" in filename:
            print(filename)
            copyfile(os.path.join(__location__, "out_dir", dirpath, filename), os.path.join(__location__, "html_report", filename))