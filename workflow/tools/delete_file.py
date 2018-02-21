#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      file:
        type: string
        is_file: true
"""
file_ = task_dict.get('input').get('file')

task_start = int(time.time())

# do the real work here
task_info = ''

if file_:
    try:
        os.remove(file_)
        task_info = 'File removed'
    except:
        task_info = "Error: failed to remove file '%s'" % file_
else:
    task_info = 'No file to remove, task skipped'

# complete the task
task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    },
    'task_info': task_info
}

save_output_json(output_json)

if task_info.startswith('Error'):
    sys.exit(1)
