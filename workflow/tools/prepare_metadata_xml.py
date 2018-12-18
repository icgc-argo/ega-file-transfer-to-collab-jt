#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json, get_md5
import subprocess

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      ega_metadata_git_repo:
        type: string
      ega_metadata_path:
        type: string
      project_code:
        type: string
      bundle_id:  # EGAR or EGAZ ID
        type: string
      ega_dataset_id:
        type: string
      ega_sample_id:
        type: string
      ega_metadata_file_name:
        type: string
"""
project_code = task_dict.get('input').get('project_code')
bundle_id = task_dict.get('input').get('bundle_id')
ega_dataset_id = task_dict.get('input').get('ega_dataset_id')
ega_sample_id = task_dict.get('input').get('ega_sample_id')
ega_study_id = task_dict.get('input').get('ega_study_id')
ega_metadata_file_name = task_dict.get('input').get('ega_metadata_file_name')
ega_experiment_id = task_dict.get('input').get('ega_experiment_id')
ega_analysis_id = task_dict.get('input').get('ega_analysis_id')
ega_run_id = task_dict.get('input').get('ega_run_id', '')
output_file = task_dict.get('input').get('ega_metadata_file_name')
ega_metadata_repo = task_dict.get('input').get('ega_metadata_repo')
out_dir = task_dict.get('input').get('out_dir')

# do the real work here
task_start = int(time.time())

metadata_container = "quay.io/baminou/dckr_prepare_metadata_xml"
subprocess.check_output(['docker', 'pull', metadata_container+':1.0'])

if not ega_metadata_repo.startswith('https://'):
    ega_metadata_repo = 'https://'+ega_metadata_repo

try:
    subprocess.check_output(['docker','run',
                             '-v', out_dir + ':/app',
                             metadata_container,
                              '-i',ega_metadata_repo,
                              '-p',project_code,
                              '-o',os.path.join('/app',output_file),
                              '-d',ega_dataset_id,
                              '-a',ega_analysis_id if ega_analysis_id else '',
                              '-e',ega_experiment_id if ega_experiment_id else '',
                              '-r',ega_run_id if ega_run_id else '',
                              '-sa',ega_sample_id if ega_sample_id else '',
                              '-st',ega_study_id if ega_study_id else ''])

except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed

# complete the task
task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)

