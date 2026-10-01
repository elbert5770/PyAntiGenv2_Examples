"""
Model builder. Outputs go to antimony_models/{MODEL_NAME}/ and generated/{MODEL_NAME}/.
"""
import os
import sys

import AntiGen_paths


from pyantigen.generate.pyantigen import PyAntiGen
from antimony_modules.Abeta.APP_reactions_Lin2022 import APP_reactions_Lin2022_Module
from antimony_modules.Abeta.Abeta_aggregation_Lin2022 import Abeta_aggregation_Lin2022_Module
from antimony_modules.Tissue_Flows.cns_flows_Lin2022_modular import CNS_flows_Lin2022_Module
from antimony_modules.Antibody.Antibody_PK_Lin2022_modular import Antibody_PK_Lin2022_Module
from antimony_modules.Abeta.Abeta_antibody_binding_Lin2022_modular import Abeta_antibody_binding_Lin2022_Module
from antimony_modules.Abeta.Abeta_ADCP_clearance_Lin2022 import Abeta_ADCP_clearance_Lin2022_Module

def generate_antimony_model(Isotopes=['']):
    MODEL_NAME = AntiGen_paths.MODEL_NAME
    model = PyAntiGen(name=MODEL_NAME, isotopes=Isotopes)
    
    SpeciesList_Abeta_peptides = ['AB42']
    No_Isotope_SpeciesList = ['Antibody', 'FcR']

    Antibody_PK_Lin2022_Module(model, Species='Antibody', No_Isotope_SpeciesList=No_Isotope_SpeciesList)

    for Species in SpeciesList_Abeta_peptides:
        APP_reactions_Lin2022_Module(model, Species=Species, No_Isotope_SpeciesList=No_Isotope_SpeciesList)
        Abeta_aggregation_Lin2022_Module(model, Species=Species, No_Isotope_SpeciesList=No_Isotope_SpeciesList)
        CNS_flows_Lin2022_Module(model, Species=Species, No_Isotope_SpeciesList=No_Isotope_SpeciesList)
        Abeta_antibody_binding_Lin2022_Module(model, Species=Species, No_Isotope_SpeciesList=No_Isotope_SpeciesList)
        Abeta_ADCP_clearance_Lin2022_Module(model, Species=Species, No_Isotope_SpeciesList=No_Isotope_SpeciesList)



    print(f"Reactions generated: {model.counter}")
    print(f"Rules generated: {len(model.rules)}")

    model.generate(__file__, model_name=MODEL_NAME)
    
    print("\nModel generated successfully.")
    print("Next steps:")
    print(f"  1. Optionally edit parameters in antimony_models/{MODEL_NAME}/{MODEL_NAME}_parameters.csv")
    print(f"  2. From Projects/{MODEL_NAME}/, run: python Model_run.py")


def update_antimony_model():
    Isotopes = ['']
    generate_antimony_model(Isotopes)

if __name__ == "__main__":
    update_antimony_model()
