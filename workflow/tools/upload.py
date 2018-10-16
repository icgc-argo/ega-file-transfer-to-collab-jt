#!/usr/bin/env python3

import os
import json
import subprocess
from utils import get_task_dict, save_output_json, get_md5
import sys


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

payload = task_dict.get('input').get('payload')
input_dir = task_dict.get('input').get('input_dir')
study_id = task_dict.get('input').get('study_id')


upload_container = "quay.io/baminou/dckr_song_upload"
song_server = os.environ.get('SONG_SERVER_COLLAB')

subprocess.check_output(['docker', 'pull', upload_container+':1.0'])

subprocess.check_output(['docker','run',
                         '--net=host',
                         '-e','ACCESSTOKEN',
                         '-e','STORAGEURL='+os.environ.get('STORAGEURL_COLLAB'),
                         '-e','METADATAURL='+os.environ.get('METADATAURL_COLLAB'),
                         '-v', input_dir+':/app',upload_container,
                         'upload','-s',study_id,
                         '-u', song_server, '-p', '/app/'+payload,
                         '-o','manifest.txt','-j','manifest.json',
                         '-d', '/app/'])
manifest = json.load(open(os.path.join(input_dir,'manifest.json')))


#subprocess.check_output(['docker', 'pull', 'mesosphere/aws-cli'])
#for file in manifest.get('files'):
#    if file.get('file_name').endswith('.xml'):
#        subprocess.check_output(['docker', 'run',
#                                 '-e', 'AWS_ACCESS_KEY_ID='+os.environ.get('COLLAB_ACCESS_KEY_ID'),
#                                 '-e', 'AWS_SECRET_ACCESS_KEY='+os.environ.get('COLLAB_SECRET_ACCESS_KEY'),
#                                 '-v', input_dir + ':/project',
#                                 'mesosphere/aws-cli', 's3', 'cp',
#                                 os.path.join('/project', os.path.basename(file.get('file_name'))),
#                                 os.path.join('https://object.cancercollaboratory.org:9080', file.get('object_id'))])

save_output_json({
    'manifest': manifest
})
