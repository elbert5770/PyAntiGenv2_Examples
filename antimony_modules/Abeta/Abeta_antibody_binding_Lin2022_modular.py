import sys
import os

from pyantigen.generate.module_base import PyAntiGenModule

class Abeta_antibody_binding_Lin2022_Module(PyAntiGenModule):
    """
    Modular Lin2022 Module for Antibody binding to Abeta species.
    """
    def build(self):
        Species_param = self.config.get('Species')
        No_Isotope_SpeciesList = self.config.get('No_Isotope_SpeciesList', [])
        
        Isotopes_mAb = [''] if 'Antibody' in No_Isotope_SpeciesList else self.model.isotopes
        Isotopes = [''] if Species_param in No_Isotope_SpeciesList else self.model.isotopes

        konPP_monomer = "konPP"
        kmAb0 = "kmAb0"

        konPP_oligomer = "konPP"
        kmAb1 = "kmAb1"

        konPD = "konPD"
        kmAb2 = "kmAb2"

        kclearmAb = "kclearmAb"

        k13mAb = "k13mAb"
        k31mAb = "k31mAb"
        k14mAb = "k14mAb"
        k14mix = "k14mix"
        k41mAb = "k41mAb"
        k41mix = "k41mix"
        k43mAb = "k43mAb"
        k43mix = "k43mix"
        
        bindings = [
            {'target': f"{Species_param}", 'complex_suffix': f"{Species_param}__Antibody", 'name': 'Abeta', 'kon': konPP_monomer, 'koff': kmAb0},
            {'target': f"{Species_param}_Oligomer", 'complex_suffix': f"{Species_param}_Oligomer__Antibody", 'name': 'Aolig', 'kon': konPP_oligomer, 'koff': kmAb1}
        ]

        complex_transports = [
            {'complex_suffix': f"{Species_param}__Antibody", 'name': 'Abeta', 'k14': k14mAb, 'k41': k41mAb, 'k43': k43mAb},
            {'complex_suffix': f"{Species_param}_Oligomer__Antibody", 'name': 'Aolig', 'k14': k14mix, 'k41': k41mix, 'k43': k43mix}
        ]

        for Isotope in Isotopes:
            Isotope_str = f"_{Isotope}_" if Isotope else "_"

            # 1. Soluble Abeta/Aolig species binding across all compartments
            for comp in ['Plasma', 'CSF', 'BrainISF']:
                mAb = f"Antibody{Isotope_str}{comp}"
                for b in bindings:
                    Target = f"{b['target']}{Isotope_str}{comp}"
                    Complex = f"{b['complex_suffix']}{Isotope_str}{comp}"
                    self.add_reaction(
                        name=f"Bind_mAb_{b['name']}{Isotope_str}{comp}",
                        reactants=f"[{mAb}, {Target}]",
                        products=Complex,
                        rate_type="RMA",
                        rate_eqtn=f"[{b['kon']}, {b['koff']}]"
                    )

            # 2. Complex Transport mapped using dictionary flows
            for ct in complex_transports:
                flows = [
                    # (comp1, comp2, name_prefix, is_rma, rates)
                    ('Plasma', '', 'Clear_Plasma', False, kclearmAb),
                    ('Plasma', 'CSF', 'Flow_Plasma_CSF', True, [k13mAb, k31mAb]),
                    ('Plasma', 'BrainISF', 'Flow_Plasma_BrainISF', True, [ct['k14'], ct['k41']]),
                    ('BrainISF', 'CSF', 'Flow_BrainISF_CSF', False, ct['k43'])
                ]

                for comp1, comp2, name_prefix, is_rma, rates in flows:
                    reactants = f"[{ct['complex_suffix']}{Isotope_str}{comp1}]" if comp1 else ""
                    products = f"[{ct['complex_suffix']}{Isotope_str}{comp2}]" if comp2 else ""
                    name = f"{name_prefix}_mAb_{ct['name']}{Isotope_str}"

                    self.add_reaction(
                        name=name,
                        reactants=reactants,
                        products=products,
                        rate_type="RMA" if is_rma else "MA",
                        rate_eqtn=rates
                    )

            # 3. Abeta Plaque binding (BrainISF specific)
            comp = 'BrainISF'
            mAb = f"Antibody{Isotope_str}{comp}"
            Aplaq = f"{Species_param}_Plaque{Isotope_str}{comp}"
            mAb_Aplaq = f"{Species_param}_Plaque__Antibody{Isotope_str}{comp}"
            self.add_reaction(
                name=f"Bind_mAb_Aplaq{Isotope_str}{comp}",
                reactants=f"[{mAb}, {Aplaq}]",
                products=mAb_Aplaq,
                rate_type="RMA",
                rate_eqtn=f"[{konPD}, {kmAb2}]"
            )

def Abeta_antibody_binding_Lin2022_modular(model, Species, No_Isotope_SpeciesList=None):
    if No_Isotope_SpeciesList is None:
        No_Isotope_SpeciesList = ['Antibody']
    config = {
        'Species': Species,
        'No_Isotope_SpeciesList': No_Isotope_SpeciesList
    }
    module = Abeta_antibody_binding_Lin2022_modularModule(model, **config)
    return model
