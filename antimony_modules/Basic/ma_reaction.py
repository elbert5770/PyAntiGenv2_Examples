"""
Basic module with a single MA reaction A -> B.
"""

from pyantigen.generate.module_base import PyAntiGenModule

class BasicMAReaction(PyAntiGenModule):
    """
    Creates a simple MA reaction A -> B.
    """
    def build(self):
        Compartments = ['Comp1']
        for Comp in Compartments:
            # Define reaction properties
            Reaction_name = f"Basic_A_to_B_{Comp}"
            Reactants = f"[A_{Comp}]"
            Products = f"[B_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = "k_A_to_B"

        # Add the reaction to the model
        self.add_reaction(Reaction_name, Reactants, Products, Rate_type, Rate_eqtn_prototype)


class BasicChainReaction(PyAntiGenModule):
    """
    Adds the second step of the chain A -> B -> C.
    With k_B_to_C = 0 (the default in Example_parameters.csv) the
    model behaves exactly like the single-step A -> B examples;
    Example4/Example5 fit k_B_to_C to demonstrate flip-flop
    bimodality.
    """
    def build(self):
        Compartments = ['Comp1']
        for Comp in Compartments:
            Reaction_name = f"Basic_B_to_C_{Comp}"
            Reactants = f"[B_{Comp}]"
            Products = f"[C_{Comp}]"
            Rate_type = "MA"
            Rate_eqtn_prototype = "k_B_to_C"

        self.add_reaction(Reaction_name, Reactants, Products, Rate_type, Rate_eqtn_prototype)
