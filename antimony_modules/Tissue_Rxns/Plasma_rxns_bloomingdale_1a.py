

from pyantigen.generate.module_base import PyAntiGenModule

class Plasma_RxnsModule(PyAntiGenModule):
    """
    Create Tissue compartmental flow reactions for a given species.
    Uses self.config['Species'] and self.config['No_Isotope_SpeciesList'].
    """
    def build(self):
        Species = self.config.get('Species')
        No_Isotope_SpeciesList = self.config.get('No_Isotope_SpeciesList', [])
        
        Isotopes = [''] if Species in No_Isotope_SpeciesList else self.model.isotopes

        # Tissue flow (unidirectional) - Tissue circulation and drainage

        
        for Isotope in Isotopes:
            Isotope_str = f"_{Isotope}_" if Isotope else "_"
            for Comp in ['Plasma']:
                Reaction_name = f"Elimination_Plasma_{Species}{Isotope_str}{Comp}"
                Reactants = f"[{Species}{Isotope_str}{Comp}]"
                Products = f"[0]"
                Rate_type = "MA"
                Rate_eqtn_prototype = "Kkidney"
                self.add_reaction(Reaction_name, Reactants, Products, Rate_type, Rate_eqtn_prototype)

            for Comp in ['TissueEndosomal','BBB','BCSFB']:
                Reaction_name = f"DegradationWithinEndosome_{Species}{Isotope_str}{Comp}"
                Reactants = f"[{Species}{Isotope_str}{Comp}]"
                Products = f"[0]"
                Rate_type = "MA"
                Rate_eqtn_prototype = "Kdeg"
                self.add_reaction(Reaction_name, Reactants, Products, Rate_type, Rate_eqtn_prototype)


