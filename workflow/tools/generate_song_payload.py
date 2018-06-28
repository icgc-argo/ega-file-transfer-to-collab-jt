#!/usr/bin/env python3

from utils import get_task_dict, save_output_json, is_aligned

from overture_song_payload import DonorPayload
from overture_song_payload import ExperimentPayload
from overture_song_payload import FilePayload
from overture_song_payload import SpecimenPayload
from overture_song_payload import SamplePayload
from overture_song_payload import SongPayload

import sys
import os
import hashlib
import json

task_dict = get_task_dict(sys.argv[1])
cwd = os.getcwd()

input_dir = task_dict.get('input').get('input_dir')
files = task_dict.get('input').get('files')
metadata_file_name = task_dict.get('input').get('metadata_file_name')

analysis_id = task_dict.get('input').get('analysis_id')
analysis_type = task_dict.get('input').get('analysis_type')
donor_gender = task_dict.get('input').get('donor_gender')
donor_submitter_id = task_dict.get('input').get('donor_submitter_id')
library_strategy = task_dict.get('input').get('library_strategy')
reference_genome = task_dict.get('input').get('reference_genome')
specimen_type = task_dict.get('input').get('specimen_type')
submitter_specimen_id = task_dict.get('input').get('submitter_specimen_id')
sample_submitter_id = task_dict.get('input').get('sample_submitter_id')
study_id = task_dict.get('input').get('study_id')

sample_type = 'DNA'


def get_file_type(fname):
    if fname.endswith('.xml'):
        return 'XML'
    if fname.endswith('.bai'):
        return 'BAI'
    if fname.endswith('.bam'):
        return 'BAM'
    if '.fastq' in fname:
        return 'FASTQ'
    return None

def get_specimen_class(specimen_type):
    if 'normal' in specimen_type.lower():
        return 'Normal'
    return 'Tumour'

def md5sum(filename):
    md5 = hashlib.md5()
    with open(filename, 'rb') as f:
        for chunk in iter(lambda: f.read(128 * md5.block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


output_file = os.path.join(input_dir,'payload.json')
experiment_payload = ExperimentPayload(aligned=is_aligned(analysis_id, reference_genome, files), library_strategy=library_strategy, reference_genome=reference_genome)
song_payload = SongPayload(analysis_id=analysis_id, analysis_type='sequencingRead', experiment_payload=experiment_payload)
donor_payload = DonorPayload(donor_gender=donor_gender, donor_submitter_id=donor_submitter_id)
specimen_payload = SpecimenPayload(specimen_class=get_specimen_class(specimen_type),
                                   specimen_type=specimen_type,specimen_submitter_id=submitter_specimen_id)
sample_payload = SamplePayload(donor_payload=donor_payload, sample_submitter_id=sample_submitter_id, sample_type=sample_type, specimen_payload=specimen_payload)

song_payload.add_sample_payload(sample_payload)
song_payload.add_info('isPcawg', False)
song_payload.add_info('dcc_project_code', study_id)

for file in files:
    file_path = os.path.join(input_dir, file.get('file_name'))
    idx_file = file.get('file_name')+'.bai'
    idx_file_path = os.path.join(input_dir, idx_file)
    song_payload.add_file_payload(FilePayload(file_access='controlled',
                              file_name=file.get('file_name'),
                              md5sum = md5sum(file_path),
                              file_type=get_file_type(file.get('file_name')),
                              file_size=os.stat(file_path).st_size))

    if os.path.isfile(idx_file_path):
        song_payload.add_file_payload(FilePayload(file_access='controlled',
                                  file_name=idx_file,
                                  md5sum = md5sum(idx_file_path),
                                  file_type=get_file_type(idx_file),
                                  file_size=os.stat(idx_file_path).st_size))

file_path = os.path.join(input_dir, metadata_file_name)
song_payload.add_file_payload(FilePayload(file_access='open',
                          file_name=metadata_file_name,
                          md5sum=md5sum(file_path),
                          file_type=get_file_type(metadata_file_name),
                          file_size=os.stat(file_path).st_size))


song_payload.to_json_file(output_file)

save_output_json({
    'payload': 'payload.json',
    'payload_json': json.load(open(os.path.join(input_dir,'payload.json')))
})