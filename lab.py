import re
import random
from utilities import Utils

u = Utils()

class Lab:
    
    def __init__(self):
        self.pricelist = {
            "x_rays": (8.0, 10.0),
            "ct_scan": (40.0, 75.0),
            "cytologic": (15.0, 20),
            "bronchoscopesis": (15.0, 20),
            "fna": (90.0, 110.0),
            "pet_scan": (750.0, 800.0),
            "fna_and_pet_scan": (840.0, 910.0),
            "mri_brain": (120.0, 150.0),
            "ro_bones": (8.0, 10.0),
            "scintigraphy": (240.0, 260.0),
        }
        
        self.delay = {
            "x_rays": (2, 4),
            "ct_scan": (7, 45),
            "cytologic": (3, 4),
            "bronchoscopesis": (2, 4),
            "fna": (5, 30),
            "pet_scan": (5, 60),
            "fna_and_pet_scan": (10, 90),
            "mri_brain": (5, 15),
            "ro_bones": (2, 4),
            "scintigraphy": (3, 7),
        }
    
    def exam_for_tumor(self, subject):
        print(subject.tumor_requirements)
        for attr_name, attr_value in subject.tumor_requirements.items():
            if attr_name == 'mass' and attr_value is None:
                subject.tumor_requirements['mass'] = random.choice([True, False])
                extra_cost = u.gaussian(self.pricelist["x_rays"][0], self.pricelist["x_rays"][1])
                extra_delay = u.gaussian(self.delay["x_rays"][0], self.delay["x_rays"][1])
                print('extra cost for chest x_rays: ', round(extra_cost, 2))
                print('extra delay for chest x_rays: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2) 
                subject.total_delay += int(extra_delay) 
                return

            if attr_name == 'diameter' and attr_value is None:
                if subject.tumor_requirements['mass'] and subject.tumor_requirements['mass'] == True:
                    subject.tumor_requirements['diameter'] = round(random.uniform(0, 14), 2)
                    rand = round(random.uniform(0, 10), 2)
                    if rand <= 2:
                        subject.tumor_requirements['nearby_organs'] = True
                        subject.tumor_requirements['fna_and_pet_scan'] = True
                    else:
                        subject.tumor_requirements['nearby_organs'] = False
                        subject.tumor_requirements['fna_and_pet_scan'] = True                    
                else:
                    subject.tumor_requirements['diameter'] = 0.0
                    subject.tumor_requirements['nearby_organs'] = False
                    subject.tumor_requirements['fna_and_pet_scan'] = False
                extra_cost = u.gaussian(self.pricelist["ct_scan"][0], self.pricelist["ct_scan"][1])
                extra_delay = u.gaussian(self.delay["ct_scan"][0], self.delay["ct_scan"][1])
                print('extra cost for ct_scan: ', round(extra_cost, 2))
                print('extra delay for ct_scan: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2) 
                subject.total_delay += int(extra_delay)
                return

            if attr_name == 'bronchoscopesis' and attr_value is None:
                subject.tumor_requirements['bronchoscopesis'] = random.choice([True, False])
                extra_cost = u.gaussian(self.pricelist["bronchoscopesis"][0], self.pricelist["bronchoscopesis"][1])
                extra_delay = u.gaussian(self.delay["bronchoscopesis"][0], self.delay["bronchoscopesis"][1])
                print('extra cost for bronchoscopesis: ', round(extra_cost, 2))
                print('extra delay for bronchoscopesis: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2)
                subject.total_delay += int(extra_delay)
                return

            if attr_name == 'cytologic' and attr_value is None:
                subject.tumor_requirements['cytologic'] = random.choice([True, False])
                extra_cost = u.gaussian(self.pricelist["cytologic"][0], self.pricelist["cytologic"][1])
                extra_delay = u.gaussian(self.delay["cytologic"][0], self.delay["cytologic"][1])
                print('extra cost for cytologic: ', round(extra_cost, 2))
                print('extra delay for cytologic: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2) 
                subject.total_delay += int(extra_delay)
                return

            if attr_name == 'fna_and_pet_scan' and attr_value is None:
                subject.tumor_requirements['fna_and_pet_scan'] = random.choice([True, False])
                extra_cost = u.gaussian(self.pricelist["fna_and_pet_scan"][0], self.pricelist["fna_and_pet_scan"][1])
                extra_delay = u.gaussian(self.delay["fna_and_pet_scan"][0], self.delay["fna_and_pet_scan"][1])
                print('extra cost for fna_and_pet_scan: ', round(extra_cost, 2))
                print('extra delay for fna_and_pet_scan: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2) 
                subject.total_delay += int(extra_delay)
                return

    def exam_for_nodes(self, subject):
        for attr_name, attr_value in subject.nodes_requirements.items():
            if attr_name == 'lymph_nodes_size' and attr_value is None:
                if subject.tumor_stage == 'T0':
                    subject.nodes_requirements['lymph_nodes_size'] = 0.5
                    subject.nodes_requirements['peribronchial_metastasis'] = False
                    subject.nodes_requirements['mediastinal_metastasis'] = False
                elif re.match('T1.', subject.tumor_stage):
                    subject.nodes_requirements['lymph_nodes_size'] = round(random.uniform(0.5, 1.5), 2)
                    subject.nodes_requirements['peribronchial_metastasis'] = False
                    subject.nodes_requirements['mediastinal_metastasis'] = False
                else:
                    subject.nodes_requirements['lymph_nodes_size'] = round(random.uniform(1.6, 11), 2)
                    subject.nodes_requirements['peribronchial_metastasis'] = random.choice([True, False])
                    subject.nodes_requirements['mediastinal_metastasis'] = True

                extra_cost = u.gaussian(self.pricelist["ct_scan"][0], self.pricelist["ct_scan"][1])
                extra_delay = u.gaussian(self.delay["ct_scan"][0], self.delay["ct_scan"][1])
                print('extra cost for ct_scan: ', round(extra_cost, 2))
                print('extra delay for ct_scan: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2) 
                subject.total_delay += int(extra_delay) 
                return

            if attr_name == 'peribronchial_metastasis' and attr_value is None:
                subject.nodes_requirements['peribronchial_metastasis'] = random.choice([True, False])
                subject.nodes_requirements['mediastinal_metastasis'] = random.choice([True, False])
                extra_cost = u.gaussian(self.pricelist["pet_scan"][0], self.pricelist["pet_scan"][1])
                extra_delay = u.gaussian(self.delay["pet_scan"][0], self.delay["pet_scan"][1])
                print('extra cost for pet_scan: ', round(extra_cost, 2))
                print('extra delay for pet_scan: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2) 
                subject.total_delay += int(extra_delay) 
                return

            if attr_name == 'fna_positive' and attr_value is None:
                subject.nodes_requirements['fna_positive'] = random.choice([True, False])
                extra_cost = u.gaussian(self.pricelist["fna"][0], self.pricelist["fna"][1])
                extra_delay = u.gaussian(self.delay["fna"][0], self.delay["fna"][1])
                print('extra cost for fna: ', round(extra_cost, 2))
                print('extra delay for fna: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2) 
                subject.total_delay += int(extra_delay) 
                return        

    def exam_for_metastasis(self, subject):
        for attr_name, attr_value in subject.metastasis_requirements.items():
            if attr_name == 'separate_tumor_nodules' and attr_value is None:
                subject.metastasis_requirements['separate_tumor_nodules'] = random.choice([True, False])
                extra_cost = u.gaussian(self.pricelist["scintigraphy"][0], self.pricelist["scintigraphy"][1])
                extra_delay = u.gaussian(self.delay["scintigraphy"][0], self.delay["scintigraphy"][1])
                print('extra cost for scintigraphy: ', round(extra_cost, 2))
                print('extra delay for scintigraphy: ', int(extra_delay))
                subject.total_cost += extra_cost 
                subject.total_delay += int(extra_delay) 
                return

            if attr_name == 'distant_metastasis' and attr_value is None:
                subject.metastasis_requirements['distant_metastasis'] = random.choice([True, False])
                extra_cost = u.gaussian(self.pricelist["mri_brain"][0], self.pricelist["mri_brain"][1])
                extra_delay = u.gaussian(self.delay["mri_brain"][0], self.delay["mri_brain"][1])
                print('extra cost for mri_brain: ', round(extra_cost, 2))
                print('extra delay for mri_brain: ', int(extra_delay))
                subject.total_cost += round(extra_cost, 2) 
                subject.total_delay += int(extra_delay) 
                return
