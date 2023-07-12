
from experta import *

class Result(Fact):
    value = Field(str, default="")

class BaseStage(KnowledgeEngine):
    def get_result(self):
        for fact in self.facts.values():
            if isinstance(fact, Result):
                return fact["value"]
        return None
    
# Initialize the Facts

class SUSPICION_FACTS(Fact):
    smoking = Field(bool, mandatory=False)
    asbestos = Field(bool, mandatory=False)
    radio = Field(bool, mandatory=False)                       # radionucleids
    history = Field(bool, mandatory=False)
    tsymptoms = Field(bool, mandatory=False)
    nsymptoms = Field(bool, mandatory=False)
    msymptoms = Field(bool, mandatory=False)

class TUMOR_FACTS(Fact):
    mass = Field(bool, mandatory=True)                        # mass found with x-rays
    diameter = Field(float, mandatory=False)                  # diameter determined with ct-scan
    bronchoscopesis = Field(bool, mandatory=False)            # bronchoscopesis examination as part of pathologoanatomical examination
    cytologic = Field(bool, mandatory=False)                  # cytologic examination as part of pathologoanatomical examination
    nearby_organs = Field(bool, mandatory=False)              # infiltracion of nearby organs found with ct-scan
    fna_and_pet_scan = Field(bool, mandatory=False)           # the results of these two should always agree

class NODES_FACTS(Fact):
    lymph_nodes_size = Field(float, mandatory=True)
    peribronchial_metastasis = Field(bool, mandatory=False)
    mediastinal_metastasis = Field(bool, mandatory=False)
    fna_positive = Field(bool, mandatory=False)

class METASTASIS_FACTS(Fact):
    separate_tumor_nodules = Field(bool, mandatory=False)
    distant_metastasis = Field(bool, mandatory=False)

class TNM_FACTS(Fact):
    T = Field(str, mandatory=False)
    N = Field(str, mandatory=False)
    M = Field(str, mandatory=False)
    
# Initialize the rules

class SuspicionInvestigation(BaseStage):
    @Rule(SUSPICION_FACTS(smoking=False, asbestos=False, radio=False, history=False, tsymptoms=False, nsymptoms=False, msymptoms=False))
    def suspicion_does_not_exist(self):
        self.declare(Result(value = 'False'))
    @Rule(OR( 
        SUSPICION_FACTS(smoking=True, asbestos=W(), radio=W(), history=W(), tsymptoms=W(), nsymptoms=W(), msymptoms=W()),
        SUSPICION_FACTS(smoking=W(), asbestos=True, radio=W(), history=W(), tsymptoms=W(), nsymptoms=W(), msymptoms=W()),
        SUSPICION_FACTS(smoking=W(), asbestos=W(), radio=True, history=W(), tsymptoms=W(), nsymptoms=W(), msymptoms=W()),
        SUSPICION_FACTS(smoking=W(), asbestos=W(), radio=W(), history=True, tsymptoms=W(), nsymptoms=W(), msymptoms=W()),
        SUSPICION_FACTS(smoking=W(), asbestos=W(), radio=W(), history=W(), tsymptoms=True, nsymptoms=W(), msymptoms=W()), 
        SUSPICION_FACTS(smoking=W(), asbestos=W(), radio=W(), history=W(), tsymptoms=W(), nsymptoms=True, msymptoms=W()), 
        SUSPICION_FACTS(smoking=W(), asbestos=W(), radio=W(), history=W(), tsymptoms=W(), nsymptoms=W(), msymptoms=True)))
    def suspicion_exists(self):
        self.declare(Result(value = 'True'))
    
class TumorStage(BaseStage):
    @Rule(TUMOR_FACTS(mass=False, diameter=P(lambda x: x==0.0), 
                      bronchoscopesis=W(), cytologic=W(), nearby_organs=False, fna_and_pet_scan=False))
    def rule_tumor_t0(self):
        self.declare(Result(value='T0'))
    @Rule(OR(
        TUMOR_FACTS(mass=False, diameter=P(lambda x: x==0), 
                    bronchoscopesis=False, cytologic=True, nearby_organs=False, fna_and_pet_scan=False),
        TUMOR_FACTS(mass=False, diameter=P(lambda x: x==0), 
                    bronchoscopesis=True, cytologic=False, nearby_organs=False, fna_and_pet_scan=False)))
    def rule_tumor_tx(self):
        self.declare(Result(value='Tx'))
    @Rule(TUMOR_FACTS(mass=True, diameter=P(lambda x: x <= 2), 
                      bronchoscopesis=W(), cytologic=W(), nearby_organs=False, fna_and_pet_scan=True))
    def rule_tumor_t1a(self):
        self.declare(Result(value='T1a'))
    @Rule(TUMOR_FACTS(mass=True, diameter=P(lambda x: 2 < x <= 3), 
                      bronchoscopesis=W(), cytologic=W(), nearby_organs=False, fna_and_pet_scan=True))
    def rule_tumor_t1b(self):
        self.declare(Result(value='T1b'))
    @Rule(TUMOR_FACTS(mass=True, diameter=P(lambda x: 3 < x <= 5), 
                      bronchoscopesis=W(), cytologic=W(), nearby_organs=False, fna_and_pet_scan=True))
    def rule_tumor_t2a(self):
        self.declare(Result(value='T2a'))
    @Rule(TUMOR_FACTS(mass=True, diameter=P(lambda x: 5 < x <= 7), 
                      bronchoscopesis=W(), cytologic=W(), nearby_organs=False, fna_and_pet_scan=True))
    def rule_tumor_t2b(self):
        self.declare(Result(value='T2b'))
    @Rule(TUMOR_FACTS(mass=True, diameter=P(lambda x: x > 7), 
                      bronchoscopesis=W(), cytologic=W(), nearby_organs=False, fna_and_pet_scan=W()))
    def rule_tumor_t3(self):
        self.declare(Result(value='T3'))
    @Rule(TUMOR_FACTS(mass=True, diameter=W(), 
                      bronchoscopesis=W(), cytologic=W(), nearby_organs=True, fna_and_pet_scan=W()))
    def rule_tumor_t4(self):
        self.declare(Result(value='T4'))

class NodesStage(BaseStage):
    @Rule(NODES_FACTS(lymph_nodes_size=P(lambda x: x < 0.5), 
                      peribronchial_metastasis=False, mediastinal_metastasis=False, fna_positive=False))
    def rule_nodes_stage_n0(self):
        self.declare(Result(value='N0'))
    @Rule(NODES_FACTS(lymph_nodes_size=P(lambda x: 0.5 <= x <= 1.5), 
                      peribronchial_metastasis=False, mediastinal_metastasis=False, fna_positive=False))
    def rule_nodes_stage_nx(self):
        self.declare(Result(value='Nx'))
    @Rule(NODES_FACTS(lymph_nodes_size=P(lambda x: x > 1.5), 
                      peribronchial_metastasis=True, mediastinal_metastasis=False, fna_positive=False))
    def rule_nodes_stage_n1(self):
        self.declare(Result(value='N1'))
    @Rule(NODES_FACTS(lymph_nodes_size=P(lambda x: x > 1.5), 
                      peribronchial_metastasis=W(), mediastinal_metastasis=True, fna_positive=False))
    def rule_nodes_stage_n2(self):
        self.declare(Result(value='N2'))
    @Rule(NODES_FACTS(lymph_nodes_size=W(), 
                      peribronchial_metastasis=W(), mediastinal_metastasis=W(), fna_positive=True))
    def rule_nodes_stage_n3(self):
        self.declare(Result(value='N3'))

class MetastasisStage(BaseStage):
    @Rule(METASTASIS_FACTS(separate_tumor_nodules=False, distant_metastasis=False))
    def rule_metastasis_stage_m0(self):
        self.declare(Result(value='M0'))
    @Rule(METASTASIS_FACTS(separate_tumor_nodules=True, distant_metastasis=False))
    def rule_metastasis_stage_m1a(self):
        self.declare(Result(value='M1a'))
    @Rule(METASTASIS_FACTS(separate_tumor_nodules=W(), distant_metastasis=True))
    def rule_metastasis_stage_m1b(self):
        self.declare(Result(value='M2b'))
    
class CancerStage(BaseStage):
    @Rule(OR(TNM_FACTS(T='Tx', N=W(), M=W()), 
             TNM_FACTS(T=W(), N='Nx', M=W()), 
             TNM_FACTS(T=W(), N=W(), M='Mx')))
    def rule_stage_x(self):
        self.declare(Result(value='Stage Undetermined'))
    @Rule(TNM_FACTS(T='T0', N='N0', M='M0'))
    def rule_stage_0(self):
        self.declare(Result(value='No indication')) # No indication of Lung Cancer was found
#     @Rule(TNM_FACTS(T='Tis', N='N0', M='M0'))
#     def rule_stage_0(self):
#         self.declare(Result(value='Stage 0')) # in situ
#     @Rule(TNM_FACTS(T='T1mi', N='N0', M='M0'))
#     def rule_stage_ia1(self):
#         self.declare(Result(value='Stage IA1')) # Non small cell lung cancer, adenocarcinoma
    @Rule(TNM_FACTS(T='T1a', N='N0', M='M0'))
    def rule_stage_ia2(self):
        self.declare(Result(value="Stage IA2"))
    @Rule(TNM_FACTS(T='T1b', N='N0', M='M0'))
    def rule_stage_ia3(self):
        self.declare(Result(value="Stage IA3"))
    @Rule(OR(TNM_FACTS(T='T1c', N='N0', M='M0'), 
             TNM_FACTS(T='T2a', N='N0', M='M0')))
    def rule_stage_ib(self):
        self.declare(Result(value="Stage IB"))
    @Rule(OR(TNM_FACTS(T='T2b', N='N0', M='M0'), 
             TNM_FACTS(T='T3', N='N0', M='M0')))
    def rule_stage_iia(self):
        self.declare(Result(value="Stage IIA"))
    @Rule(OR(TNM_FACTS(T='T1', N='N1', M='M0'), 
             TNM_FACTS(T='T2', N='N1', M='M0')))
    def rule_stage_iib(self):
        self.declare(Result(value="Stage IIB"))
    @Rule(OR(TNM_FACTS(T='T1', N='N2', M='M0'), 
             TNM_FACTS(T='T2', N='N2', M='M0'), 
             TNM_FACTS(T='T3', N='N1', M='M0'), 
             TNM_FACTS(T='T3', N='N2', M='M0'), 
             TNM_FACTS(T='T4', N='N1', M='M0'), 
             TNM_FACTS(T='T4', N='N2', M='M0')))
    def rule_stage_iiia(self):
        self.declare(Result(value="Stage IIIA"))
    @Rule(TNM_FACTS(T=W(), N='N3', M='M0'))
    def rule_stage_iiib(self):
        self.declare(Result(value="Stage IIIB"))
    @Rule(TNM_FACTS(T=W(), N=W(), M='M1a'))
    def rule_stage_iiic(self):
        self.declare(Result(value="Stage IIIC"))
    @Rule(OR(TNM_FACTS(T=W(), N=W(), M='M1b'), 
             TNM_FACTS(T=W(), N=W(), M='M1c')))
    def rule_stage_iv(self):
        self.declare(Result(value="Stage IV"))