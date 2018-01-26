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
ega_expriment_id = task_dict.get('input').get('ega_expriment_id')
ega_analysis_id = task_dict.get('input').get('ega_analysis_id')
ega_run_id = task_dict.get('input').get('ega_run_id', '')
output_file = task_dict.get('input').get('ega_metadata_file_name')
ega_metadata_repo = task_dict.get('input').get('ega_metadata_repo')

# do the real work here
task_start = int(time.time())

try:
    subprocess.check_output(['docker','pull','quay.io/baminou/ega-collab-dckr:latest'])
    subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr'
      'prepare_ega_xml_audit.py',
      '-i',ega_metadata_repo,
      '-p',project_code,
      '-o','/app/'+output_file,
      '-d',ega_dataset_id,
      '-a',ega_analysis_id if ega_analysis_id else '',
      '-e',ega_expriment_id if ega_expriment_id else '',
      '-r',ega_run_id if ega_run_id else '',
      '-sa',ega_sample_id if ega_sample_id else '',
      '-st',ega_study_id if ega_study_id else ''])

except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed

# complete the task
task_stop = int(time.time())


"""
    output:
      xml_file:
        type: string
        is_file: true
      xml_file_name:  # passing through from ega_metadata_file_name
        type: string
      xml_file_size:
        type: integer
      xml_file_md5sum:
        type: string
"""

output_json = {
    'xml_file': os.path.join(cwd, output_file),
    'xml_file_name': output_file,
    'xml_file_size': os.path.getsize(output_file),
    'xml_file_md5sum': get_md5(output_file),
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)

