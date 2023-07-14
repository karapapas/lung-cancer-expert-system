
from datetime import datetime
from lab import Lab
from experta import *
from expertawrapper import *

lab = Lab()
utils = Utils()

# Initialize the knowledge engines.
suspicion_engine = SuspicionInvestigation()
tumor_engine = TumorStage()
nodes_engine = NodesStage()
metastasis_engine = MetastasisStage()
cancer_engine = CancerStage()

date_str = datetime.now().strftime('%Y%m%d')
file_name = f'subjects_results_{date_str}.csv'

class Doctor:
    
    def __init__(self):
        pass

    def estimate(self, subject):

        if subject.cancer_suspected == None:
            print('Suspected for cancer None')
            if utils.ready_to_determine(subject.suspicion_requirements) == True:
                subject.cancer_suspected = utils.determine(suspicion_engine, SUSPICION_FACTS, subject.suspicion_requirements)
            else:
                subject.set_suspicion_requirements()
                subject.cancer_suspected = utils.determine(suspicion_engine, SUSPICION_FACTS, subject.suspicion_requirements)
                self.estimate(subject)
        
        elif subject.cancer_suspected == 'False':
            print('Suspected for cancer False')
            return
    
        else:
            print('Suspected for cancer True')
        
            if subject.tumor_stage == None:
                if utils.ready_to_determine(subject.tumor_requirements) == True:
                    subject.tumor_stage = utils.determine(tumor_engine, TUMOR_FACTS, subject.tumor_requirements)
                    print('Tumor estimated as: ', subject.tumor_stage)
                    print('subject.tumor_requirements: ', subject.tumor_requirements)
                else:
                    lab.exam_for_tumor(subject)
                    self.estimate(subject)        

            if subject.nodes_stage == None:
                if utils.ready_to_determine(subject.nodes_requirements) == True:
                    subject.nodes_stage = utils.determine(nodes_engine, NODES_FACTS, subject.nodes_requirements)
                    print('Nodes estimated as: ', subject.nodes_stage)
                    print('subject.nodes_requirements: ', subject.nodes_requirements)
                else:
                    lab.exam_for_nodes(subject)
                    self.estimate(subject)

            if subject.metastasis_stage == None:
                if utils.ready_to_determine(subject.metastasis_requirements) == True:
                    subject.metastasis_stage = utils.determine(metastasis_engine, METASTASIS_FACTS, subject.metastasis_requirements)
                    print('Metastasis estimated as: ', subject.metastasis_stage)
                    print('subject.metastasis_requirements: ', subject.metastasis_requirements)
                else:
                    lab.exam_for_metastasis(subject)
                    self.estimate(subject)

            if subject.cancer_stage == None:
                if subject.tumor_stage != None and subject.nodes_stage != None and subject.metastasis_stage != None:
    #               if we have reached this point and either T,N or M have value None this means that no appropriate rule was found,
    #               and no further exams are available for the respective T, N, M
    #               therefore we should set the None to Tx, Nx or Mx respectively
                    if subject.tumor_stage != None:
                        subject.tnm_requirements['T'] = subject.tumor_stage
                    else:
                        subject.tnm_requirements['T'] = 'Tx'
                    if subject.nodes_stage != None:
                        subject.tnm_requirements['N'] = subject.nodes_stage
                    else:
                        subject.tnm_requirements['N'] = 'Nx'
                    if subject.metastasis_stage != None:
                        subject.tnm_requirements['M'] = subject.metastasis_stage
                    else:
                        subject.tnm_requirements['M'] = 'Mx'
                    print(subject.tnm_requirements)
                    subject.cancer_stage = utils.determine(cancer_engine, TNM_FACTS, subject.tnm_requirements)
                    print('Cancer estimated as: ', subject.cancer_stage)
                    result = (f'Subject: {subject.id}, '
                            f'Cancer suspected: {subject.cancer_suspected}, '
                            f'Cancer diagnosis: {subject.cancer_stage}, '
                            f'Total cost: {round(subject.total_cost, 2)}, '
                            f'Total delay: {subject.total_delay}\n')
                    logger =  (f'{subject.id}, '
                            f'{subject.cancer_suspected}, '
                            f'{subject.cancer_stage}, '
                            f'{round(subject.total_cost, 2)}, '
                            f'{subject.total_delay}\n')
                    print(result)
                    print(logger)

                    with open(file_name, 'a') as f:
                        f.write(logger)
                    return
                else:
                    self.estimate(subject)