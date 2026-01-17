
         
            
from ge_lib.shared.shared import json_objs
from .ground_model_footing import ground_model_footing
from .ground_model_pile_set import ground_model_pile_set
from .ground_model_stiffness_pile_set import ground_model_stiffness_pile_set
from .ground_models_pile_sets import ground_models_pile_sets

class FoundExamples(json_objs):
    def __init__(self):
        super().__init__(id= '01', description='JSON object templates for foundations',version='p01.1',type="examples")
        self.add('ground_model_footing.json',ground_model_footing, 'example of ground model with footing and loadings','P01.1')
        self.add('ground_model_pile_set.json',ground_model_pile_set, 'example of ground model with pile set and loadings','P01.1')
        self.add('ground_model_stiffness_pile_set.json',ground_model_stiffness_pile_set, 'example of ground model piles set with settlements','P01.1')
        self.add('ground_models_pile_sets.json',ground_models_pile_sets, 'example of multiple ground models and pile sets with loadings','P01.1')
