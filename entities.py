import random

class Subject:
    
    def __init__(self, id, 
                 
                 cancer_suspected=None,
                 tumor_stage=None,
                 nodes_stage=None,
                 metastasis_stage=None,
                 
                 cancer_stage=None, 
                 
                 total_cost=0.0, 
                 total_delay=0, 
                 
                 suspicion_requirements=None, 
                 tumor_requirements=None, 
                 nodes_requirements=None, 
                 metastasis_requirements=None, 
                 tnm_requirements=None):
        
        self.id = id
        
        self.cancer_suspected = cancer_suspected
        
        self.tumor_stage = tumor_stage
        self.nodes_stage = nodes_stage
        self.metastasis_stage = metastasis_stage
        
        self.cancer_stage = cancer_stage
        
        self.total_cost = total_cost
        self.total_delay = total_delay
        
        self.suspicion_requirements = suspicion_requirements 
        self.tumor_requirements = tumor_requirements 
        self.nodes_requirements = nodes_requirements 
        self.metastasis_requirements = metastasis_requirements 
        self.tnm_requirements = tnm_requirements

        self.suspicion_requirements = {
            'smoking': None,
            'asbestos': None,
            'radio': None,
            'history': None,
            'tsymptoms': None,
            'nsymptoms': None,
            'msymptoms': None
        }

        self.tumor_requirements = {
            'mass': None,
            'diameter': None,
            'bronchoscopesis': None,
            'cytologic': None,
            'nearby_organs': None,
            'fna_and_pet_scan': None
        }

        self.nodes_requirements = {
            'lymph_nodes_size': None,
            'peribronchial_metastasis': None,
            'mediastinal_metastasis': None,
            'fna_positive': None
        }

        self.metastasis_requirements = {
            'separate_tumor_nodules': None,
            'distant_metastasis': None
        }

        self.tnm_requirements = {
            'T': None,
            'N': None,
            'M': None
        }

    def set_suspicion_requirements(self):
        self.total_cost = 0.0
        self.total_delay = 1
        rand = round(random.uniform(0, 10), 2)
        if rand <= 2:
            for key in self.suspicion_requirements.keys():
                self.suspicion_requirements[key] = random.choice([True, False])
        else:
            for key in self.suspicion_requirements.keys():
                self.suspicion_requirements[key] = False

    def set_tumor_requirements(self):
        self.tumor_requirements['mass'] = random.choice([True, False])
        if self.tumor_requirements['mass'] and self.tumor_requirements['mass'] == True:
            self.tumor_requirements['diameter'] = round(random.uniform(0, 14), 2)
        for key in ['bronchoscopesis', 'cytologic', 'nearby_organs', 'fna_and_pet_scan']:
            self.tumor_requirements[key] = random.choice([True, False, None])

    def set_nodes_requirements(self):
        for key in self.nodes_requirements.keys():
            self.nodes_requirements[key] = random.choice([True, False, None])

    def set_metastasis_requirements(self):
        for key in self.metastasis_requirements.keys():
            self.metastasis_requirements[key] = random.choice([True, False, None])
