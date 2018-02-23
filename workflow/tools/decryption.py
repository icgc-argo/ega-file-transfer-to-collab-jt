#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
import subprocess
from utils import get_task_dict, save_output_json, get_md5


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      input_dir:
        type: string
      files:
        type: array

"""
input_dir = task_dict.get('input').get('input_dir')
files = task_dict.get('input').get('files')

task_start = int(time.time())

for _file in files:
    try:
        file_name = os.path.join(input_dir, _file.get('file_name'))
        encrypted_file_name = os.path.join(input_dir, _file.get('file_name'))+'.aes'
        r = subprocess.check_output(['decrypt_ega_file.py','-i',encrypted_file_name,'-o', file_name])
        os.remove(encrypted_file_name)
        if not get_md5(file_name) == _file.get('file_md5sum'):
            sys.exit(1)
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