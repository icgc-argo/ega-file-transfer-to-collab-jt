import json
import hashlib
import os

def get_task_dict(json_string):
    try:
        task_dict = json.loads(json_string)
    except:
        return {}

    return task_dict


def save_output_json(output_dict={}):
    with open('output.json', 'w') as f:
        f.write(json.dumps(output_dict, indent=2))


def get_md5(fname):
    hash = hashlib.md5()
    if not os.path.isfile(fname): return None
    with open(fname) as f:
        for chunk in iter(lambda: f.read(1024*1024), ""):
            hash.update(chunk)
    return hash.hexdigest()

def is_aligned(analysis_id, reference_genome, files):
    for file in files:
        if file.get('file_name').endswith('.bam')\
                and 'EGAZ' in analysis_id and reference_genome is not None:
            return True
    return False
