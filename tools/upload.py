#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json
import subprocess

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      donor_id:
        type: string
      library_strategy:
        type: string
      paired_end:
        type: boolean
      input_dir:
        type: string
      files:
        type: array
"""
donor_id = task_dict.get('input').get('donor_id')
library_strategy = task_dict.get('input').get('library_strategy')
paired_end = task_dict.get('input').get('paired_end')
input_dir = task_dict.get('input').get('input_dir')
files = task_dict.get('input').get('files')


task_start = int(time.time())

# do the real work here
cmd = 'upload_file_to_collab.py'

try:
    #metadata step
    if file_.endswith('.xml'):
        print subprocess.check_output(['aws', '--profile', 'collab', '--endpoint-url', 'https://object.cancercollaboratory.org:9080', 's3', 'cp', file_, os.path.join('s3://oicr.icgc.meta/metadata/', object_id)])

    r = subprocess.check_output("%s -i %s -g %s -id %s -md5 %s" % (cmd, file_, bundle_id, object_id, file_md5sum), shell=True)
except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed

# index exist
if idx_object_id:
    try:
        r = subprocess.check_output("%s -i %s -g %s -id %s -md5 %s" % (cmd, idx_file, bundle_id, idx_object_id, idx_file_md5sum), shell=True)
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
