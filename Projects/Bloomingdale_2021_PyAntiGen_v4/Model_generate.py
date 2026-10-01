"""
Model builder. Outputs go to antimony_models/{MODEL_NAME}/ and generated/{MODEL_NAME}/.
"""
import os
import sys

import AntiGen_paths


from pyantigen.generate.pyantigen import PyAntiGen
from antimony_modules.Tissue_Rxns.Tissue_rxns_bloomingdale_1a import Tissue_RxnsModule
from antimony_modules.Tissue_Rxns.Plasma_rxns_bloomingdale_1a import Plasma_RxnsModule
from antimony_modules.Tissue_Flows.Tissue_flows_bloomingdale_1a import Tissue_FlowsModule
from antimony_modules.Tissue_Flows.FCRn_flows_bloomingdale_1a import FcRn_FlowsModule
from antimony_modules.Tissue_Flows.cns_flows_bloomingdale_1a import CNS_FlowsModule


def generate_antimony_model(Isotopes=['']):
    MODEL_NAME = AntiGen_paths.MODEL_NAME
    model = PyAntiGen(name=MODEL_NAME, isotopes=Isotopes)
    
    SpeciesList = ['Antibody','Gadobutrol']
    for Species in SpeciesList:
        Tissue_FlowsModule(model, Species=Species)
        CNS_FlowsModule(model, Species=Species)

    SpeciesList = ['Antibody']
    for Species in SpeciesList:
        Tissue_RxnsModule(model, Species=Species)
        FcRn_FlowsModule(model, Species=Species)

    SpeciesList = ['Gadobutrol']
    for Species in SpeciesList:
        Plasma_RxnsModule(model, Species=Species)

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
