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

decrypt_container = "quay.io/baminou/dckr_ega_decrypt"

subprocess.check_output(['docker', 'pull', decrypt_container+':1.0'])

for _file in files:
    try:
        file_name = os.path.join('/app', _file.get('file_name'))
        encrypted_file_name = os.path.join('/app', _file.get('file_name'))+'.aes'
        r = subprocess.check_output(['docker','run',
                                     '-e','EGA_DCK_KEY',
                                     '-v',input_dir+':/app',
                                     decrypt_container,
                                     '-i',encrypted_file_name,
                                     '-o',file_name])
        os.remove(os.path.join(input_dir,_file.get('file_name'))+'.aes')
        if not get_md5(os.path.join(input_dir, _file.get('file_name'))) == _file.get('file_md5sum'):
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
