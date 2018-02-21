#!/usr/bin/env python3

import os
import sys
import json
import time
from random import randint
import subprocess
from utils import get_task_dict, save_output_json
from overture_song_payload import DonorPayload
from overture_song_payload import ExperimentPayload
from overture_song_payload import FilePayload
from overture_song_payload import SpecimenPayload
from overture_song_payload import SamplePayload
from overture_song_payload import SongPayload
import hashlib



task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

"""
    input:
      input_directory:
        type: string
      files:
        type: array
"""
input_directory = task_dict.get('input').get('input_directory')
files = task_dict.get('input').get('files')
#sample = task_dict.get('input').get('sample')
song_analysis_id = task_dict.get('input').get('bundle_id')
experiment_library_strategy = task_dict.get('input').get('experiment_library_strategy')
reference_genome = task_dict.get('input').get('reference_genome')

# TODO analysis_type = task_dict.get() 
# TODO analysis_id = task_dict.get()
# TODO library_strategy = ...
# TODO reference_strategy = ...

task_start = int(time.time())
cwd = os.getcwd()

# TODO verify song_analysis_type
def create_payload_json(file, experiment_library_strategy, reference_genome, song_analysis_id,input_directory, output_file):
    aligned = False
    if file.get('file_name').endswith('fastq'):
        aligned = True

    donor_payload = DonorPayload(donor_gender=sample.get('donor').get('gender'),donor_submitter_id=sample.get('donor').get('submitter_id'))
    experiment_payload = ExperimentPayload(aligned=aligned,library_strategy=experiment_library_strategy,reference_genome=reference_genome)

    file_path = os.path.join(input_directory,file.get('file_name'))
    payload = FilePayload(file_access=file.get('access'),file_name=file.get('file_name'),
                                  md5sum=hashlib.md5(open(file_path,'rb').read()).hexdigest(),file_type='BAM',file_size=os.stat(file_path).st_size)

    specimen_payload = SpecimenPayload(specimen_class=sample.get('specimen').get('class'),
                                   specimen_type=sample.get('specimen').get('type'),
                                   specimen_submitter_id=sample.get('specimen').get('submitter_id'))

    sample_payload = SamplePayload(donor_payload=donor_payload, sample_submitter_id=sample.get('submitter_id'),sample_type=sample.get('type'),
                               specimen_payload=specimen_payload)

    song_payload = SongPayload(analysis_id=song_analysis_id, analysis_type='sequencingRead',experiment_payload=experiment_payload)
    song_payload.add_file_payload(payload)
    song_payload.add_sample_payload(sample_payload)
    song_payload.to_json_file(output_file)



payload = os.path.join(cwd,'payload.json')

for file in files:
    create_payload_json(file, experiment_library_strategy, reference_genome, song_analysis_id, input_directory, os.path.join(input_directory,payload))
    create_payload_json(file, experiment_library_strategy, reference_genome, song_analysis_id, input_directory, os.path.join(input_directory,payload))

save_output_json({
    'payload': payload
})