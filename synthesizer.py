
import json

from subject import *

class Synthesizer:
    
    def __init__(self):
        pass

    def create_subjects(self, n):
        subjects = []
        for i in range(1, n+1):
            p = Subject(i)
            p.set_suspicion_requirements()
            p.set_tumor_requirements()
            p.set_nodes_requirements()
            p.set_metastasis_requirements()
            subjects.append(p)
        return subjects

    def subjects_to_json(self, subjects, file_name):
        data = []
        for subject in subjects:
            subject_dict = vars(subject)
            clean_dict = {k: v for k, v in subject_dict.items() if v is not None}
            data.append(clean_dict)
        with open(file_name, 'w') as f:
            json.dump(data, f)

    def load_subjects_from_json(self, file_name):
        with open(file_name, 'r') as f:
            data = json.load(f)
        return [Subject(**d) for d in data]
