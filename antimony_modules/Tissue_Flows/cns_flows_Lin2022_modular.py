import sys
import os

from pyantigen.generate.module_base import PyAntiGenModule

class CNS_flows_Lin2022_Module(PyAntiGenModule):
    """
    Modular Lin2022 Module for transport flows across Plasma, CSF, and BrainISF.
    """
    def build(self):
        Species_param = self.config.get('Species')
        No_Isotope_SpeciesList = self.config.get('No_Isotope_SpeciesList', [])
        Isotopes = [''] if Species_param in No_Isotope_SpeciesList else self.model.isotopes

        species_data = [
            {'name': 'Abeta', 'rate_suffix': 'Abeta', 'prefix': f"{Species_param}"},
            {'name': 'Aolig', 'rate_suffix': 'Aolig', 'prefix': f"{Species_param}_Oligomer"},
            {'name': 'BACEs', 'rate_suffix': 'BACE',  'prefix': "SolubleBACE"}
        ]

        # Bidirectional flow combinations (RMA) using arrays
        # (Compartment1, Compartment2, fwd_idx, rev_idx)
        rma_flows = [
            ('Plasma', 'CSF', '13', '31'),
            ('Plasma', 'BrainISF', '14', '41')
        ]

        for Isotope in Isotopes:
            Isotope_str = f"_{Isotope}_" if Isotope else "_"

            for sp in species_data:
                # 1. RMA flows for Plasma <-> CSF and Plasma <-> BrainISF
                for comp1, comp2, fwd, rev in rma_flows:
                    self.add_reaction(
                        name=f"Flow_{fwd}_{rev}_{sp['name']}{Isotope_str}",
                        reactants=f"[{sp['prefix']}{Isotope_str}{comp1}]",
                        products=f"[{sp['prefix']}{Isotope_str}{comp2}]",
                        rate_type="RMA",
                        rate_eqtn=[f"k{fwd}{sp['rate_suffix']}", f"k{rev}{sp['rate_suffix']}"]
                    )

                # 2. MA flow for BrainISF -> CSF (k43)
                self.add_reaction(
                    name=f"Flow_43_{sp['name']}{Isotope_str}",
                    reactants=f"[{sp['prefix']}{Isotope_str}BrainISF]",
                    products=f"[{sp['prefix']}{Isotope_str}CSF]",
                    rate_type="MA",
                    rate_eqtn=f"k43{sp['rate_suffix']}"
                )

def cns_flows_Lin2022_modular(model, Species, No_Isotope_SpeciesList=None):
    if No_Isotope_SpeciesList is None:
        No_Isotope_SpeciesList = ['Antibody']
    config = {
        'Species': Species,
        'No_Isotope_SpeciesList': No_Isotope_SpeciesList
    }
    module = CNS_flows_Lin2022_modularModule(model, **config)
    return model
