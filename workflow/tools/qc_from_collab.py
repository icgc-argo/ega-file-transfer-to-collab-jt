#!/usr/bin/env python

from utils import get_task_dict, save_output_json
import subprocess
import os
import sys
import time
import docker

task_dict = get_task_dict(sys.argv[1])

object_id = task_dict.get('input').get('object_id')
file_name = task_dict.get('input').get('file_name')

task_start = int(time.time())
task_info = ''

tmp_dir = '/tmp'

try:
	r = subprocess.check_output(['download_icgc_file.py','-id',object_id,'-s','collab', '-o', tmp_dir])
	if not os.path.isfile(tmp_dir+"/"+file_name):
		task_info = "Error: File "+object_id+":"+file_name+" couldn't be downloaded from collab."
	else:
		os.remove(tmp_dir+"/"+file_name)
except Exception, e:
	task_info = "Error: "+str(e)

task_stop = int(time.time())


output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop,
    },
    'task_info': task_info
}

save_output_json(output_json)

if task_info != '':
    sys.exit(1)