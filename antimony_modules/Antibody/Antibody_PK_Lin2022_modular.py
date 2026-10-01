import sys
import os

from pyantigen.generate.module_base import PyAntiGenModule

class Antibody_PK_Lin2022_Module(PyAntiGenModule):
    """
    Modular Lin2022 Module for Antibody (Aducanumab) Pharmacokinetics.
    """
    def build(self):
        Species_param = self.config.get('Species')
        No_Isotope_SpeciesList = self.config.get('No_Isotope_SpeciesList', [])
        Isotopes = [''] if Species_param in No_Isotope_SpeciesList else self.model.isotopes

        kinfusion = "kinfusion" # Defined dynamically
        kclearmAb = "kclearmAb"
        k12mAb = "k12mAb"
        k21mAb = "k21mAb"
        
        k13mAb = "k13mAb"
        k31mAb = "k31mAb"
        k14mAb = "k14mAb"
        k41mAb = "k41mAb"
        k43mAb = "k43mAb"

        # Dictionary of all MA flows mapping (Comp1, Comp2) to (NamePrefix, RateConstant)
        # Empty string '' denotes clearance or external source
        flows = {
            ('IV', 'Plasma'): ("Flow_IV", kinfusion),
            ('Plasma', ''): ("Clear_Plasma", kclearmAb),
            ('Plasma', 'Peripheral'): ("Flow_Plasma_Peripheral", k12mAb),
            ('Peripheral', 'Plasma'): ("Flow_Peripheral_Plasma", k21mAb),
            ('Plasma', 'CSF'): ("Flow_Plasma_CSF", k13mAb),
            ('CSF', 'Plasma'): ("Flow_CSF_Plasma", k31mAb),
            ('Plasma', 'BrainISF'): ("Flow_Plasma_BrainISF", k14mAb),
            ('BrainISF', 'Plasma'): ("Flow_BrainISF_Plasma", k41mAb),
            ('BrainISF', 'CSF'): ("Flow_BrainISF_CSF", k43mAb)
        }

        for Isotope in Isotopes:
            Isotope_str = f"_{Isotope}_" if Isotope else "_"

            for (comp1, comp2), (name_prefix, rate) in flows.items():
                name = f"{name_prefix}_mAb{Isotope_str}"
                
                # Format reactants and products with brackets as required for single species
                reactants = f"[Antibody{Isotope_str}{comp1}]" if comp1 else ""
                products = f"[Antibody{Isotope_str}{comp2}]" if comp2 else ""
                
                self.add_reaction(
                    name=name,
                    reactants=reactants,
                    products=products,
                    rate_type="MA",
                    rate_eqtn=rate
                )

def Antibody_PK_Lin2022_modular(model, Species, No_Isotope_SpeciesList=None):
    if No_Isotope_SpeciesList is None:
        No_Isotope_SpeciesList = ['Antibody']
    config = {
        'Species': Species,
        'No_Isotope_SpeciesList': No_Isotope_SpeciesList
    }
    module = Antibody_PK_Lin2022_modularModule(model, **config)
    return model
