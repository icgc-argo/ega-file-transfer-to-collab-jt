#!/usr/bin/env python

import os
import sys
import time
import subprocess
import json
from utils import get_md5, get_task_dict, save_output_json

allowed_codes = { 'LIRI-JP', 'PACA-CA' , 'PRAD-CA', 'RECA-EU', 'PAEN-AU', 'PACA-AU',
'BOCA-UK','OV-AU', 'MELA-AU', 'BRCA-UK', 'PRAD-UK', 'CMDI-UK', 'LINC-JP',
'ORCA-IN', 'BTCA-SG', 'LAML-KR', 'LICA-FR', 'CLLE-ES', 'ESAD-UK', 'PAEN-IT'}

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

input_dir = task_dict.get('input').get('input_dir')
payload = task_dict.get('input').get('payload')
study_id = task_dict.get('input').get('study_id')


task_start = int(time.time())
run = study_id in allowed_codes

manifest=''

if run:

    upload_container = "quay.io/baminou/dckr_song_upload:1.0"
    song_server = os.environ.get('SONG_SERVER_AWS')

    subprocess.check_output(['docker', 'pull', upload_container])

    subprocess.check_output(['docker','run',
                             '--net=host',
                             '-e','ACCESSTOKEN',
                             '-e','STORAGEURL='+os.environ.get('STORAGEURL_AWS'),
                             '-e','METADATAURL='+os.environ.get('METADATAURL_AWS'),
                             '-v', input_dir+':/app',upload_container,
                             'upload','-s',study_id,
                             '-u', song_server, '-p', '/app/'+payload,
                             '-o','manifest.txt','-j','manifest.json',
                             '-d', '/app/'])
    manifest = json.load(open(os.path.join(input_dir,'manifest.json')))

#    subprocess.check_output(['docker','pull','mesosphere/aws-cli'])
#    for file in manifest.get('files'):
#        if file.get('file_name').endswith('.xml'):
#            subprocess.check_output(['docker', 'run',
#                                    '-e','AWS_ACCESS_KEY_ID',
#                                    '-e', 'AWS_SECRET_ACCESS_KEY',
#                                     '-v', input_dir+':/project',
#                                     'mesosphere/aws-cli', 's3', 'cp',
#                                     os.path.join('/project',os.path.basename(file.get('file_name'))),
#                                     os.path.join('s3://oicr.icgc.meta/metadata/', file.get('object_id'))])


task_stop = int(time.time())


output_json = {
    'allowed_upload': run,
    'manifest': manifest,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    },
    'out_dir': cwd
}

save_output_json(output_json)
