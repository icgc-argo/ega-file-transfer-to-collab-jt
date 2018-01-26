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
      project_code:
        type: string
      ega_file_id:
        type: string
      file_name:
        type: string
      file_md5sum:
        type: string
      object_id:
        type: string
"""
ega_file_id = task_dict.get('input').get('ega_file_id')
file_name = task_dict.get('input').get('file_name')
encrypted_file_name = file_name+".aes"
file_md5sum = task_dict.get('input').get('file_md5sum')
object_id = task_dict.get('input').get('object_id')
project_code = task_dict.get('input').get('project_code')


task_start = int(time.time())

try:
    subprocess.check_output(['docker','pull','quay.io/baminou/ega-collab-dckr:latest'])

    #Download
    if project_code in ['LINC-JP', 'BTCA-JP']:
      r = subprocess.check_output(['docker','run','-e ASCP_EGA_USER','-e ASCP_EGA_HOST','-e ASPERA_SCP_PASS','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','download_ega_file.py',
        '-p',project_code,'-f',str(ega_file_id)[-2:]+"/"+ega_file_id+".aes",'-o','/app/'+encrypted_file_name])
    else:
      r = subprocess.check_output(['docker','run','-e ASCP_EGA_USER','-e ASCP_EGA_HOST','-e ASPERA_SCP_PASS','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','download_ega_file.py',
        '-p',project_code,'-f',ega_file_id+".aes",'-o','/app/'+encrypted_file_name])


      #Decryption
    r = subprocess.check_output(['docker','run','-e EGA_DCK_KEY','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr',
      'decrypt_ega_file.py','-i',os.path.join('/app',encrypted_file_name),'-o', os.path.join('/app',file_name)])

    #Check MD5 sum
    if get_md5(file_name) == file_md5sum:
      task_info = 'Error: mismatch file_md5sum'
      sys.exit(1)

    #Delete encrypted file
    os.remove(encrypted_file_name)

    #Generate bai file
    r = subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','samtools','index','/app/'+file_name])

except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed


# complete the task

task_stop = int(time.time())

"""
    output:
      file:  # new field
        type: string
        is_file: true
      ega_file_id:  # passing through
        type: string
      file_name:  # passing through
        type: string
      file_md5sum:  # passing through
        type: string
      object_id:  # passing through
        type: string
"""

output_json = {
    'file': os.path.join(cwd, file_name),
    'ega_file_id': ega_file_id,
    'file_name': file_name,  # we may need to deal with encrypted / unencypted file names
    'object_id': object_id,
    'file_md5sum': file_md5sum,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
