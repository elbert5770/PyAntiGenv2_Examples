import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import numpy as np


def plot_results(paths, results_dict):
    """
    Plot simulation results for N experiments.

    Args:
        plot_path: Directory to save the plot.
        MODEL_NAME: Model name for title/filename.
        results: List of dicts from Experiment.run_all: each has "result", "data", "label".
    """
    
    plot_path = paths["plot_path"]
    MODEL_NAME = paths["MODEL_NAME"]
    repo_root = paths["repo_root"]
    n = max(len(results_dict), 1)
    color_A = ["blue","green"]
    color_B = ["red","orange"]
    fig = plt.figure(figsize=(10, 16))
    gs  = gridspec.GridSpec(2, 1, figure=fig, hspace=0.3, left=0.1, right=0.65)
    ax_A = fig.add_subplot(gs[0, 0])
    ax_B = fig.add_subplot(gs[1, 0])
    for i, (label, item) in enumerate(results_dict.items()):    
        results = item["results"]
        data_dict = item["data"]
        data = data_dict["PK data"]
        
        time_points = results["time"]
        observed_species = item["observed_species"]
        for j, observed_species_name in enumerate(observed_species):
            print(observed_species_name)
            if observed_species_name == "time":
                continue
                
            if "Antibody" in observed_species_name or "FcRn" in observed_species_name:
                ax = ax_A
            elif "Gadobutrol" in observed_species_name:
                ax = ax_B
            else:
                continue

            obs_name = f'{observed_species_name}'
            ax.plot(time_points, results[obs_name], label=observed_species_name, color=f'C{(j-1) % 10}')
            if "Time" in data.columns and observed_species_name in data.columns:
                ax.plot(data["Time"], data[observed_species_name],   linestyle='--', linewidth=4, color=f'C{(j-1) % 10}')
            
 
    for ax, title, panel_label in zip([ax_A, ax_B], ["Antibody and FcRn", "Gadobutrol"], ['a', 'b']):
        ax.text(-0.05, 1.05, panel_label, transform=ax.transAxes, fontsize=18, fontweight='bold')
        ax.set_title(title)
        ax.set_xlabel("Time",fontsize = 14)
        ax.set_ylabel("Concentration (nM)",fontsize = 14)
        handles, labels = ax.get_legend_handles_labels()
        if handles:
            ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
        ax.set_ylim(1e-1, 1e4)
        ax.set_yscale('log')

    ax_B.set_xlim(0, 200)
    plot_name = os.path.join(plot_path, MODEL_NAME + ".png")
    plt.savefig(plot_name, bbox_inches="tight",dpi=300)
    print(f"Plot saved to: {plot_name}")
    plt.show()

def _plot_profile_likelihood(ax, plot_config, opt, params_estimated, param_names):
    """Plot profile likelihood for parameters."""
    
    # Get parameters to profile
    params_to_profile = plot_config.get('parameters', param_names)
    n_points = plot_config.get('n_points', 30)
    range_factor = plot_config.get('range_factor', 3.0)
    
    colors = ['blue', 'green', 'red', 'orange', 'purple']
    markers = ['o', 's', '^', 'D', 'v']
    
    profile_func = opt.get("stats", {}).get("profile_likelihood")
    if not profile_func:
        print("Warning: no profile_likelihood closure found in opt['stats']")
        return

    result_fun = opt.get("fun", 0)

    for idx, param_name in enumerate(params_to_profile):
        if param_name not in param_names:
            continue
        
        param_idx = param_names.index(param_name)
        param_vals, nll_vals = profile_func(param_idx, n_points=n_points, range_factor=range_factor)
        
        # Normalize
        param_vals_normalized = param_vals / params_estimated[param_idx]
        nll_vals_rel = nll_vals - result_fun
        
        color = colors[idx % len(colors)]
        marker = markers[idx % len(markers)]
        ax.plot(param_vals_normalized, nll_vals_rel, 
               marker=marker, linestyle='-', label=param_name, linewidth=2, color=color)
    
    # Add vertical line at optimal value
    ax.axvline(1.0, color='red', linestyle='--', alpha=0.5, linewidth=1.5, label='Optimal')
    
    ax.set_xlabel(plot_config.get('xlabel', 'Parameter Value (relative to optimal)'))
    ax.set_ylabel(plot_config.get('ylabel', 'Δ NLL (relative to minimum)'))
    ax.set_title(plot_config.get('title', 'Profile Likelihood (Identifiability Check)'))
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    # ax.set_ylim(bottom=0)
    
    # Set xlim if specified
    if 'xlim' in plot_config:
        ax.set_xlim(plot_config['xlim'])
    else:
        ax.set_xlim(0.2, 3.5)