"""Experiment registry: one 'replicate' entry per simulation,
simulations are optimized together if in the same opt_group. 
"""
from .Data import *
from .Events import *
from .Loss_config import *
from .Observed_species import *
from .Solver_settings import *
from .Update_parameters import *
from .Update_opt_parameters import *

from dataclasses import dataclass, field

@dataclass
class Experiment:
    replicates: dict = field(default_factory=dict)

    @property
    def opt_groups(self):
        """Return {opt_group: [replicate_key, ...]} by scanning replicates."""
        groups = {}
        for key, rep in self.replicates.items():
            og = rep.get("Opt_group")
            if og is not None:
                groups.setdefault(og, []).append(key)
        return groups


def make_replicate(config, **meta):
    """
    Build a single replicate entry dict from an explicit config dict.

    config keys (all required unless noted):
      "Label"            : str
      "Events"           : callable(replicate, df_dict) -> str
      "Data"             : callable(replicate, data_path) -> Dict of DataFrame or None
      "Observed_species" : callable(RoadRunner_instance or None) -> list[str]
      "Solver_settings"  : callable(replicate) -> dict
      "Update_parameters": callable(RoadRunner_instance, replicate, mode) -> dict
      "Loss_config"      : callable(replicate) -> dict
      "Opt_group"        : str
      
    'callable' functions are contained in separate files with the same name as the key. 
    For example, "Events" is contained in the file "Events.py", "Data" is contained in
    the file "Data.py", etc. 
    
    'replicate' is the output of make_replicate. It contains the dictionary above plus
    any optional keyword arguments. 

    Any arguments required by the 'callable' functions should be passed as keyword arguments.
    
    Keyword arguments are stored in 'replicate' as additional keys.  Example arguments:
      Age = 70, Status = True, Population = "Amyloid_negative", Drug = "Lecanemab", 
      dose_nmol = 10, Schedule = "default", Type = "default", …  

    Example::

        make_replicate(
            {
                "Label":            "Example_1",
                "Events":           generate_no_events,
                "Data":             load_data_Example,
                "Observed_species": observed_Example,
                "Solver_settings":  solver_settings_Example,
                "Update_parameters": update_no_parameters,
                "Loss_config": Example_loss_config,
                "Opt_group": opt_group
            },
        )
    """
    entry = dict(config)
    return {**entry, **meta}

# ***************************************************************************
# USER DEFINED OPTIMIZATION
# ***************************************************************************

def _build_SILK():
    exp = Experiment()


    exp.replicates['SILK'] = make_replicate(
        {
            "Label": "SILK",
            "Events": event_SILK,
            "Data": load_SILK_data,
            "Observed_species": SILK_species,
            "Solver_settings": solver_settings_SILK,
            "Update_parameters":   update_no_parameters,
            "Loss_config":         no_optimization,
        }
    )
    
    return exp
    

EXPERIMENTS_SILK = _build_SILK()

# ***************************************************************************
# END USER DEFINED EXPERIMENTS
# ***************************************************************************

# ---------------------------------------------------------------------------
# Registry accessors
# ---------------------------------------------------------------------------

def get_EXPERIMENTS():
    """Returns a dict mapping experiment name -> Experiment."""
    return {k: v for k, v in globals().items() if k.startswith('EXPERIMENT_')}

def get_EXPERIMENT(name):
    """Returns a single Experiment by name."""
    return globals().get(name)
