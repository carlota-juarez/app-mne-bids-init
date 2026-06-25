# This file is a MNE python-based brainlife.io App

# Carlota Juárez Alonso

# Set up enviroment

import json
from pathlib import Path
import subprocess
from shutil import copyfile


# Current path 

__location__ = Path(__file__).resolve().parent

# Read the parameters from Brainlife 

config_path = __location__/'config.json'
if not config_path.exists():
    raise FileNotFoundError(f"The configuration file could not be found in {config_path}")

with open (config_path, 'r') as f:
    config = json.load(f)

# Entry and output paths 

bids_root = config.get('bids')
ch_types = config.get('ch_types')

if not bids_root:
    raise ValueError("The 'bids' parameter is required")
if not ch_types:
    raise ValueError("The 'ch_types' parameter is required")

deriv_root = __location__/'out_dir'
html_report_dir = __location__/'html_report'

# Ensure output directories exist

deriv_root.mkdir(parents = True, exist_ok = True)
html_report_dir.mkdir(parents = True, exist_ok = True)

# Rewrite the info in the .json file into a .py file

file_name = __location__/'pipeline_config.py'

# Inputs from the interface web to MNE variables

with open(file_name, 'w') as f:

    f.write(f"bids_root = '{bids_root}'\n")
    f.write(f"deriv_root = '{deriv_root}'\n")
    f.write(f"ch_types = {ch_types}\n")

    # General settings

    subjects_dir = config.get('subjects_dir', None)
    if subjects_dir:
        f.write(f"subjects_dir = '{subjects_dir}'\n")

    sessions = config.get('sessions', 'all')
    if sessions:
        if isinstance(sessions, str):
            f.write(f"sessions = '{sessions}'\n")
        else:
            f.write(f"sessions = {sessions}\n")

    allow_missing_sessions = config.get('allow_missing_sessions', False)
    f.write(f"allow_missing_sessions = {allow_missing_sessions}\n")

    task = config.get('task', None)
    if task:
        f.write(f"task = '{task}'\n")

    runs = config.get('runs', 'all')
    if runs:
        if isinstance(runs, str):
            f.write(f"runs = '{runs}'\n")
        else:
            f.write(f"runs = {runs}\n")
    
    exclude_runs = config.get('exclude_runs', [])
    if exclude_runs:
        f.write(f"exclude_runs = {exclude_runs}\n")

    crop_runs = config.get('crop_runs', None)
    if crop_runs:
        f.write(f"crop_runs = {crop_runs}\n")
    
    proc = config.get('proc', None)
    if proc:
        f.write(f"proc = '{proc}'\n")

    rec = config.get('rec', None)
    if rec:
        f.write(f"rec = '{rec}'\n")

    space = config.get('space', None)
    if space:
        f.write(f"space = '{space}'\n")
    
    acq = config.get('acq', None)
    if acq:
        f.write(f"acq = '{acq}'\n")
    
    conditions = config.get('conditions', None)
    if conditions:
        f.write(f"conditions = {conditions}\n")
    
    subjects = config.get('subjects', 'all')
    if subjects:
        if isinstance(subjects, str):
            f.write(f"subjects = '{subjects}'\n")
        else:
            f.write(f"subjects = {subjects}\n")

    exclude_subjects = config.get('exclude_subjects', [])
    if exclude_subjects:
        f.write(f"exclude_subjects = {exclude_subjects}\n")

    task_is_rest = config.get('task_is_rest', False)
    f.write(f"task_is_rest = {task_is_rest}\n")

    interactive = config.get('interactive', False)
    f.write(f"interactive = {interactive}\n")
    
    process_empty_room = config.get('process_empty_room', False)
    f.write(f"process_empty_room = {process_empty_room}\n") 

    process_rest = config.get('process_rest', False)
    f.write(f"process_rest = {process_rest}\n")

    data_type = config.get('data_type', None)
    if data_type:
        f.write(f"data_type = '{data_type}'\n")

    eog_channels = config.get('eog_channels', None)
    if eog_channels:
        f.write(f"eog_channels = {eog_channels}\n")

    eeg_bipolar_channels = config.get('eeg_bipolar_channels', None)
    if eeg_bipolar_channels:
        f.write(f"eeg_bipolar_channels = {eeg_bipolar_channels}\n")
    
    eeg_reference = config.get('eeg_reference', 'average')
    if eeg_reference:
        f.write(f"eeg_reference = '{eeg_reference}'\n")

    eeg_template_montage = config.get('eeg_template_montage', None)
    f.write(f"eeg_template_montage = {eeg_template_montage}\n")

    drop_channels = config.get('drop_channels', [])
    if drop_channels:
        f.write(f"drop_channels = {drop_channels}\n")

    analyze_channels = config.get('analyze_channels', 'ch_types')
    if isinstance(analyze_channels, str):
        f.write(f"analyze_channels = '{analyze_channels}'\n")
    else:
        f.write(f"analyze_channels = {analyze_channels}\n")

    reader_extra_params = config.get('reader_extra_params', {})
    if reader_extra_params:
        f.write(f"reader_extra_params = {reader_extra_params}\n")
    
    read_raw_bids_verbose = config.get('read_raw_bids_verbose', None)
    if read_raw_bids_verbose:
        f.write(f"read_raw_bids_verbose = {read_raw_bids_verbose}\n")

    plot_psd_for_runs = config.get('plot_psd_for_runs', 'all')
    if plot_psd_for_runs:
        f.write(f"plot_psd_for_runs = {plot_psd_for_runs}\n")

    random_state = config.get('random_state', None)
    if random_state:
        f.write(f"random_state = {random_state}\n")
        
# Run python script

command = ["mne_bids_pipeline", f"--config={file_name}", "--steps=init"]

try:
    subprocess.run(command, check=True)
except subprocess.CalledProcessError as e:
    raise e

# Find the reports and make a copy in out_html folder

real_deriv_root = deriv_root.resolve()

for path in real_deriv_root.rglob("*.html"):
        if "sub-average" not in path.name:
            print(path.name)
            copyfile(path, html_report_dir/path.name)