import os
import sys

from pyantigen.engine.Model_simulate import setup_simulation
from pyantigen.engine.Model_optimize import setup_optimization_from_groups
from Modules.Plots import *
from Modules.Experiment import get_EXPERIMENT
from Modules.Optimizer_settings import get_OPTIMIZATION
from AntiGen_paths import MODEL_NAME, REPO_ROOT
from Model_generate import update_antimony_model

EXPERIMENT_dict = {
    "Bloomingdale": {'EXPERIMENT': get_EXPERIMENT('EXPERIMENTS_Bloomingdale'), 'plot': plot_results, 'opt_settings_key': 'Bloomingdale'},
}

_FULL_DIAGNOSTICS = {
    "wald_analysis": True,
    "slice_analysis": True,
    "profile_likelihood_analysis": True,
    "sobol_analysis": True,
    "sobol_N": 128,
}

_SLICE_ONLY = {
    "wald_analysis": False,
    "slice_analysis": True,
    "profile_likelihood_analysis": False,
    "sobol_analysis": False,
}

_PROFILE_ONLY = {
    "wald_analysis": True,
    "slice_analysis": False,
    "profile_likelihood_analysis": True,
    "sobol_analysis": False,
}

_SOBOL_ONLY = {
    "wald_analysis": False,
    "slice_analysis": False,
    "profile_likelihood_analysis": False,
    "sobol_analysis": True,
}



OPTIMIZATION_REGISTRY = {

}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Tellurium/RoadRunner Simulation and Optimization Runner")
    parser.add_argument("--optimize", type=str, choices=list(OPTIMIZATION_REGISTRY.keys()),
                        help="Optimization mode")
    parser.add_argument("--simulate", type=str, choices=list(EXPERIMENT_dict.keys()),
                        help="Simulation mode")

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.error("No arguments provided.")

    update_antimony_model()


# ---  Optimization ------------------------------------
    if args.optimize:
        opt_info = OPTIMIZATION_REGISTRY[args.optimize]
        model_name_to_use = MODEL_NAME

        run_settings = {
            "run_steady_state_first": False,
            "Verbose": True,
            "save_SBML?": False,
            "MODEL_NAME": model_name_to_use,
            "REPO_ROOT": REPO_ROOT,
            "slice_analysis": False,
        }
        run_settings.update(opt_info.get("diagnostics", {}))

        # Retrieve experiment object & optimization spec(s)
        exp_obj = get_EXPERIMENT(opt_info["experiment"])
        opt_keys = opt_info["opt_key"]
        if isinstance(opt_keys, str):
            opt_keys = [opt_keys]

        experiment_arg = {
            "EXPERIMENT": exp_obj,
            "plot": None,  # Bypassed during optimization run
        }

        for opt_key in opt_keys:
            opt_spec = get_OPTIMIZATION(opt_key)
            print(f"Starting domain optimization for: {args.optimize} [{opt_key}]")
            setup_optimization_from_groups(run_settings, opt_spec, experiment_arg)

# --- Simulation ---------------------------------------------
    elif args.simulate:
        run_name = args.simulate
        fig_config = EXPERIMENT_dict[run_name]
        model_name_to_use = MODEL_NAME


        run_settings = {
            "run_steady_state_first": False,
            "Verbose": True,
            "save_SBML?": False,
            "MODEL_NAME": model_name_to_use,
            "REPO_ROOT": REPO_ROOT,
        }

        setup_simulation(run_settings, fig_config)
    
    print("Run_settings: ", run_settings)
    

