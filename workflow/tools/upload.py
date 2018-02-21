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
      input_directory:
        type: string
      payload:
        type: string
      study_id:
        type: boolean
      files:
        type: array
"""
input_directory = task_dict.get('input').get('input_directory')
payload = task_dict.get('input').get('payload')
study_id = task_dict.get('input').get('study_id')
files = task_dict.get('input').get('files')


task_start = int(time.time())

upload_container = "quay.io/baminou/dckr_song_upload"
song_server = 'http://142.1.177.168:8080'

subprocess.check_output(['docker', 'pull', upload_container])

subprocess.check_output(['docker', 'run', '-e', 'ACCESSTOKEN',
                         '-v', input_directory + ':/app', upload_container, 'upload', '-s', study_id,
                         '-u', song_server, '-p', '/app/' + payload,
                         '-o', 'manifest.txt', '-j', 'manifest.json',
                         '-d', '/app/'])

manifest_json = json.load(open(os.path.join(input_directory,'manifest.json')))


#for file in files:
#    if file.endswith('.xml'):
#        print subprocess.check_output(['aws', '--profile', 'collab', '--endpoint-url', 'https://object.cancercollaboratory.org:9080', 's3', 'cp', file_, os.path.join('s3://oicr.icgc.meta/metadata/', file.get('object_id'))])
#try:
#    #metadata step
#    if file_.endswith('.xml'):
#        print subprocess.check_output(['aws', '--profile', 'collab', '--endpoint-url', 'https://object.cancercollaboratory.org:9080', 's3', 'cp', file_, os.path.join('s3://oicr.icgc.meta/metadata/', object_id)])

#    r = subprocess.check_output("%s -i %s -g %s -id %s -md5 %s" % (cmd, file_, bundle_id, object_id, file_md5sum), shell=True)
#except Exception, e:
#    with open('jt.log', 'w') as f: f.write(str(e))
#    sys.exit(1)  # task failed

# index exist
#if idx_object_id:
#    try:
#        r = subprocess.check_output("%s -i %s -g %s -id %s -md5 %s" % (cmd, idx_file, bundle_id, idx_object_id, idx_file_md5sum), shell=True)
#    except Exception, e:
#        with open('jt.log', 'w') as f: f.write(str(e))
#        sys.exit(1)  # task failed


# complete the task
task_stop = int(time.time())

output_json = {
    'manifest': manifest_json,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
