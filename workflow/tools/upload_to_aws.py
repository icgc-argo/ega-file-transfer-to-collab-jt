#!/usr/bin/env python

import os
import sys
import time
import subprocess
from utils import get_md5, get_task_dict, save_output_json

allowed_codes = { 'LIRI-JP', 'PACA-CA' , 'PRAD-CA', 'RECA-EU', 'PAEN-AU', 'PACA-AU',
'BOCA-UK','OV-AU', 'MELA-AU', 'BRCA-UK', 'PRAD-UK', 'CMDI-UK', 'LINC-JP',
'ORCA-IN', 'BTCA-SG', 'LAML-KR', 'LICA-FR', 'CLLE-ES', 'ESAD-UK', 'PAEN-IT'}

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

file_ = task_dict.get('input').get('file')
file_name = task_dict.get('input').get('file_name')
file_md5sum = task_dict.get('input').get('file_md5sum')
object_id = task_dict.get('input').get('object_id')
idx_file_ = task_dict.get('input').get('idx_file')
idx_file_name = task_dict.get('input').get('idx_file_name')
idx_object_id = task_dict.get('input').get('idx_object_id')
idx_file_md5sum = task_dict.get('input').get('idx_file_md5sum')
project_code = task_dict.get('input').get('project_code')


task_start = int(time.time())
file_size = 0
idx_file_size = 0
run = project_code in allowed_codes

if run: 

    if file_md5sum is None:
        file_md5sum = str(get_md5(file_))

    if idx_file_ and idx_file_md5sum is None:
        idx_file_md5sum = str(get_md5(idx_file_))

    file_size = int(os.path.getsize(file_))

    if idx_object_id:
        idx_file_size = int(os.path.getsize(idx_file_))
        try:
            print subprocess.check_output(['icgc-storage-client', '--profile', 'aws', 'upload', '--file', idx_file_, '--object-id', idx_object_id, '--md5', idx_file_md5sum, '--force'])
        except Exception, e:
            with open('jt.log', 'w') as f: f.write(str(e))
            sys.exit(1)  # task failed

    try:
        print subprocess.check_output(['icgc-storage-client', '--profile', 'aws', 'upload','--file', file_, '--object-id', object_id, '--md5', file_md5sum, '--force'])

        #metadata step
        if file_.endswith('.xml'):
            print subprocess.check_output(['aws', '--profile', 'amazon', 's3', 'cp', file_, os.path.join('s3://oicr.icgc.meta/metadata/', object_id)])

    except Exception, e:
        with open('jt.log', 'w') as f: f.write(str(e))
        sys.exit(1)


task_stop = int(time.time())


output_json = {
    'file': file_,
    'allowed_upload': run,
    'file_md5sum': file_md5sum,
    'idx_file': idx_file_,
    'idx_file_md5sum': idx_file_md5sum,
    'file_size' : file_size,
    'idx_file_size' : idx_file_size,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
