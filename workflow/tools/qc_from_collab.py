#!/usr/bin/env python

from utils import get_task_dict, save_output_json, get_md5
import subprocess
import os
import sys
import time

task_dict = get_task_dict(sys.argv[1])

manifest = task_dict.get('input').get('manifest')

task_start = int(time.time())
task_info = ''

cwd = os.getcwd()

try:
    download_container = "quay.io/baminou/dckr_download_ega_file:1.0"
    subprocess.check_output(['docker', 'pull', download_container])

    for file in manifest.get('files'):
        subprocess.check_output(['docker','run',
                                 '--net=host',
                                 '-e', 'ACCESSTOKEN',
                                 '-e', 'STORAGEURL=' + os.environ.get('STORAGEURL_COLLAB'),
                                 '-e', 'METADATAURL=' + os.environ.get('METADATAURL_COLLAB'),
                                 '-v', cwd+':/app',
                                 download_container,'download',
                                 '-id',file.get('object_id'), '-o', '/app','--skip-validation'])

        if not os.path.isfile(os.path.join(cwd,os.path.basename(file.get('file_name')))):
            task_info = "Error: File "+file.get('object_id')+":"+os.path.basename(file.get('file_name'))+" couldn't be downloaded from collab."
        else:
            if not get_md5(os.path.join(cwd, os.path.basename(file.get('file_name')))) == file.get('md5'):
                task_info = "Error: File " + file.get('object_id') + ":" + os.path.basename(
                    file.get('file_name')) + " does not have matching md5 sum."
            else:
                os.remove(os.path.join(cwd,os.path.basename(file.get('file_name'))))
except Exception, e:
    task_info = "Error: "+str(e)

task_stop = int(time.time())

output_json = {
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop,
    },
    'task_info': task_info,
    'out_dir': cwd
}

save_output_json(output_json)

if task_info != '':
    sys.exit(1)