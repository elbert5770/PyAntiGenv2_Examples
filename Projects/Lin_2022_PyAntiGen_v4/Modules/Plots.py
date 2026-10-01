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

    # We will generate two plots: one log-scaled and one linear-scaled.
    scales = [
        {"scale": "log", "suffix": "_log.png", "ylabel": "Amount (nmol) [Log Scale]", "adjust_right": 0.7},
        {"scale": "linear", "suffix": ".png", "ylabel": "Amount (nmol) [Linear Scale]", "adjust_right": 0.7}
    ]
    
    for spec in scales:
        plt.figure(figsize=(12, 8))
        ax = plt.gca()
        
        for label, item in results_dict.items():
            result = item["results"]
            data_dict = item["data"]
            df = data_dict["Lin_data"]
            
            plt.plot(result['time'], result['totalmAbPlasma'], color='pink')
            plt.plot(result['time'], result['totalmAbCSF'], color='green')
            plt.plot(result['time'], result['totalAbetaPlasma'], color='red')
            plt.plot(result['time'], result['totaloligPlasma'], color='orange')
            plt.plot(result['time'], result['totalAbetaBrainISF'], color='purple')
            plt.plot(result['time'], result['totaloligISF'], color='magenta')
            plt.plot(result['time'], result['totalPlaque'], color='cyan')
            plt.plot(result['time'], result['AB42_Plasma'], color='black')
            plt.plot(result['time'], result['AB42__Antibody_Plasma'], color='blue')
            plt.plot(result['time'], result['AB42_Oligomer_Plasma'], color='green')
            plt.plot(result['time'], result['AB42_Oligomer__Antibody_Plasma'], color='red')
            plt.plot(result['time'], result['AB42_CSF'], color='black')
            plt.plot(result['time'], result['AB42__Antibody_CSF'], color='blue')
            plt.plot(result['time'], result['AB42_Oligomer_CSF'], color='green')
            plt.plot(result['time'], result['AB42_Oligomer__Antibody_CSF'], color='red')
            plt.plot(result['time'], result['AB42_BrainISF'], color='black')
            plt.plot(result['time'], result['AB42__Antibody_BrainISF'], color='blue')
            plt.plot(result['time'], result['AB42_Oligomer_BrainISF'], color='green')
            plt.plot(result['time'], result['AB42_Oligomer__Antibody_BrainISF'], color='red')
        
            plt.plot(df['Time'], df['totalmAbPlasma'],  linestyle='dashed', linewidth='4',color='pink', label='Total Antibody Plasma')
            plt.plot(df['Time'], df['totalmAbCSF'],  linestyle='dashed', linewidth='4', color='green',  label='Total Antibody CSF')
            plt.plot(df['Time'], df['totalAbetaPlasma'],  linestyle='dashed', linewidth='4', color='red', label='Total Abeta Plasma')
            plt.plot(df['Time'], df['totaloligPlasma'],  linestyle='dashed', linewidth='4', color='orange', label='Total Oligomer Plasma')
            plt.plot(df['Time'], df['totalAbetaBrainISF'],  linestyle='dashed', linewidth='4', color='purple', label='Total Abeta BrainISF')
            plt.plot(df['Time'], df['totaloligISF'],  linestyle='dashed', linewidth='4', color='magenta', label='Total Oligomer BrainISF')
            plt.plot(df['Time'], df['totalPlaque'],  linestyle='dashed', linewidth='4', color='cyan', label='Total Plaque')
            plt.plot(df['Time'], df['ABplasma'],  linestyle='dashed', linewidth='4', color='black', label='Abeta_Plasma')
            plt.plot(df['Time'], df['ABAbplasma'],  linestyle='dashed', linewidth='4', color='blue', label='Abeta__Antibody_Plasma')
            plt.plot(df['Time'], df['ABOplasma'],  linestyle='dashed', linewidth='4', color='green', label='Abeta_Oligomer_Plasma')
            plt.plot(df['Time'], df['ABOAbplasma'],  linestyle='dashed', linewidth='4', color='red', label='Abeta_Oligomer__Antibody_Plasma')
            plt.plot(df['Time'], df['ABcsf'],  linestyle='dashed', linewidth='4', color='black', label='Abeta_CSF')
            plt.plot(df['Time'], df['ABAbcsf'],  linestyle='dashed', linewidth='4', color='blue', label='Abeta__Antibody_CSF')
            plt.plot(df['Time'], df['ABOcsf'],  linestyle='dashed', linewidth='4', color='green', label='Abeta_Oligomer_CSF')
            plt.plot(df['Time'], df['ABOAbcsf'],  linestyle='dashed', linewidth='4', color='red', label='Abeta_Oligomer__Antibody_CSF')
            plt.plot(df['Time'], df['ABbisf'],  linestyle='dashed', linewidth='4', color='black', label='Abeta_BrainISF')
            plt.plot(df['Time'], df['ABAbbisf'],  linestyle='dashed', linewidth='4', color='blue', label='Abeta__Antibody_BrainISF')
            plt.plot(df['Time'], df['ABObisf'],  linestyle='dashed', linewidth='4', color='green', label='Abeta_Oligomer_BrainISF')
            plt.plot(df['Time'], df['ABOAbbisf'],  linestyle='dashed', linewidth='4', color='red', label='Abeta_Oligomer__Antibody_BrainISF')
        
        if spec["scale"] == "log":
            plt.ylim(1e-6, 1e4)
            plt.yscale('log')
            
        plt.xlabel('Time (seconds)', fontsize=16)
        plt.ylabel(spec["ylabel"], fontsize=16)
        plt.xticks(fontsize=14)
        plt.yticks(fontsize=14)
        ax.ticklabel_format(axis='x', style='sci', scilimits=(0,0), useMathText=True)
        ax.xaxis.get_offset_text().set_fontsize(14)
        ax.yaxis.get_offset_text().set_fontsize(14)
        plt.title("Simulation Results for " + MODEL_NAME, fontsize=16)
        plt.tight_layout()
    
        plt.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
        plt.subplots_adjust(right=spec["adjust_right"])
        plot_name = os.path.join(plot_path, MODEL_NAME + spec["suffix"])
        plt.savefig(plot_name, bbox_inches="tight", dpi=300 if spec["scale"] == "log" else 300)
        print(f"Plot saved to: {plot_name}")
        plt.show()

