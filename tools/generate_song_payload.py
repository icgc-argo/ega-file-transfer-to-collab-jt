#!/usr/bin/env python

import os
import sys
import json
import time
from random import randint
import subprocess
from utils import get_task_dict, save_output_json


task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      input_file:
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
input_file = task_dict.get('input').get('input_file')
ega_file_id = task_dict.get('input').get('ega_file_id')
file_name = task_dict.get('input').get('file_name')
file_md5sum = task_dict.get('input').get('file_md5sum')
object_id = task_dict.get('input').get('object_id')

# TODO analysis_type = task_dict.get() 
# TODO analysis_id = task_dict.get()
# TODO library_strategy = ...
# TODO reference_strategy = ...

task_start = int(time.time())

payload_file = 'payload.json'

try:
    subprocess.check_output(['docker','pull','quay.io/baminou/ega-collab-dckr:latest'])

    #Initialization of the payload json
    r = subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','SongAdapter.py','init',os.path.join('/app',payload_file)])
    
    #Analysis ID added to the payload json
    r = subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','SongAdapter.py',
      'add:analysis_id',
      '--input',os.path.join('/app',payload_file),
      '--id', analysis_id
      ])

    #Analysis Type added to the payload json
    r = subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','SongAdapter.py',
      'add:analysis_type',
      '--input', os.path.join('/app',payload_file),
      '--type', analysis_type
      ])

    # TODO bam or fastq, aligned or not aligned
    r = subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','SongAdapter.py',
      'add:bam:experiment',
      '--input', os.path.join('/app',payload_file),
      '--library-strategy', library_strategy,
      '--reference-genome', reference_genome
      ])

    for _file in task_dict.get('files'):
      r = subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','SongAdapter.py',
        'add:file',
        '--input', os.path.join('/app',payload_file),
        '--md5sum', _file.get('file_md5sum'),
        '--name', _file.get('file_name'),
        '--size', _file.get('file_size'),
        '--type', _file.get('file_type'),
        '--reference-genome', reference_genome
        ])

    r = subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','SongAdapter.py',
      'add:info',
      '--input', os.path.join('/app',payload_file),
      '--key', 'is_pcawg',
      '--value', 'true'
      ])

    r = subprocess.check_output(['docker','run','-v',os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','SongAdapter.py',
      'add:sample',
      '--input', os.path.join('/app',payload_file),
      '--donor-gender', donor_gender,
      '--donor-submitter-id', donor_submitter_id,
      '--sample-submitter-id', sample_submitter_id,
      '--sample-type', sample_type,
      '--specimen-class', specimen_class,
      '--speciment-submitter-id',specimen_submitter_id,
      '--specimen_type',specimen_type
      ])

    r = subprocess.check_output(['docker','run','-v', os.getcwd()+':/app','quay.io/baminou/ega-collab-dckr','SongAdapter.py',
      'sing','upload','-f',os.path.join('/app',payload_file)])

except Exception, e:
    with open('jt.log', 'w') as f: f.write(str(e))
    sys.exit(1)  # task failed


# complete the task
task_stop = int(time.time())

"""
    output:
      file:
        type: string
        is_file: true
      ega_file_id:  # passing through
        type: string
      file_name:  # passing through
        type: string
      file_size:  
        type: string
      file_md5sum:  # passing through
        type: string
      object_id:  # passing through
        type: string
"""

output_json = {
    'file': os.path.join(cwd, file_name),
    'ega_file_id': ega_file_id,
    'file_name': file_name,
    'file_size': os.path.getsize(file_name),
    'file_md5sum': file_md5sum,
    'object_id': object_id,
    'runtime': {
        'task_start': task_start,
        'task_stop': task_stop
    }
}

save_output_json(output_json)
