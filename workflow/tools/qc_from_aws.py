#!/usr/bin/env python

import subprocess
import os
import sys
import time
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])

allowed_codes = { 'LIRI-JP', 'PACA-CA' , 'PRAD-CA', 'RECA-EU', 'PAEN-AU', 'PACA-AU',
'BOCA-UK','OV-AU', 'MELA-AU', 'BRCA-UK', 'PRAD-UK', 'CMDI-UK', 'LINC-JP',
'ORCA-IN', 'BTCA-SG', 'LAML-KR', 'LICA-FR', 'CLLE-ES', 'ESAD-UK', 'PAEN-IT'}

object_id = task_dict.get('input').get('object_id')
file_name = task_dict.get('input').get('file_name')
project_code = task_dict.get('input').get('project_code')

run = project_code in allowed_codes

task_start = int(time.time())
task_info = ''

if run:

    tmp_dir = '/tmp'

    try:
        r = subprocess.check_output(['download_icgc_file.py','-id',object_id,'-s','aws', '-o', tmp_dir])
        if not os.path.isfile(tmp_dir+"/"+file_name):
            task_info = "Error: File "+object_id+":"+file_name+" couldn't be downloaded from aws."
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