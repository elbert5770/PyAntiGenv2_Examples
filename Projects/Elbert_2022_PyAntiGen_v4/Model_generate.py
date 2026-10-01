"""
Model builder. Outputs go to antimony_models/{MODEL_NAME}/ and generated/{MODEL_NAME}/.
"""
import os
import sys

import AntiGen_paths


from pyantigen.generate.pyantigen import PyAntiGen
from antimony_modules.Abeta.Abeta_production_clearance_elbert_1a import AbetaProductionModule
from antimony_modules.Abeta.APP_reactions_elbert_1a import APP_ReactionsModule
from antimony_modules.Tissue_Flows.cns_flows_elbert_1a import CNS_FlowsModule

def generate_antimony_model(Isotopes=['']):
    MODEL_NAME = AntiGen_paths.MODEL_NAME
    model = PyAntiGen(name=MODEL_NAME, isotopes=Isotopes)
    
    APP_ReactionsModule(model)
    
    Species_List = ['AB38','AB40','AB42']
    
    for Species in Species_List:
        AbetaProductionModule(model, Species=Species)
        CNS_FlowsModule(model, Species=Species)  

    print(f"Reactions generated: {model.counter}")
    print(f"Rules generated: {len(model.rules)}")

    model.generate(__file__, model_name=MODEL_NAME)
    
    print("\nModel generated successfully.")
    print("Next steps:")
    print(f"  1. Optionally edit parameters in antimony_models/{MODEL_NAME}/{MODEL_NAME}_parameters.csv")
    print(f"  2. From scripts/{MODEL_NAME}/, run: python {MODEL_NAME}_run.py")


def update_antimony_model():
    Isotopes = ['','13C6Leu']
    generate_antimony_model(Isotopes)

if __name__ == "__main__":
    update_antimony_model()
