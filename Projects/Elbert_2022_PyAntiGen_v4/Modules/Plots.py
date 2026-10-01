import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import numpy as np


def plot_SILK_results(paths, results_dict):
    """
    Plot simulation results for N experiments.

    Args:
        plot_path: Directory to save the plot.
        MODEL_NAME: Model name for title/filename.
        results: List of dicts from Experiment.run_all: each has "result", "data", "label".
    """
    result = results_dict["SILK"]["results"]
    SF38 = result["SF38"]
    SF40 = result["SF40"]
    SF42 = result["SF42"]
    plot_path = paths["plot_path"]
    MODEL_NAME = paths["MODEL_NAME"]
    repo_root = paths["repo_root"]
    n = max(len(results_dict), 1)
    color_A = ["blue","green","red"]
    color_B = ["green","purple"]
    color_C = ["blue","green","purple","orange"]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5), sharex=True)
    fig_flow, ax_flow = plt.subplots(figsize=(10, 5))
    for i, (label, item) in enumerate(results_dict.items()):
        
        result = item["results"]
        data_dict = item["data"]
        df = data_dict["SILK"]
        
        time_points = result["time"]
        
# Plot 1: MFL
        ax1.plot(result['time'], SF38*result['[AB38_13C6Leu_SP3]']/(result['[AB38_13C6Leu_SP3]']+result['[AB38_SP3]']), label=r'A$\beta$38 PyAntiGen',color='blue')
        ax1.plot(result['time'], SF40*result['[AB40_13C6Leu_SP3]']/(result['[AB40_13C6Leu_SP3]']+result['[AB40_SP3]']), label=r'A$\beta$40 PyAntiGen',color='green')
        ax1.plot(result['time'], SF42*result['[AB42_13C6Leu_SP3]']/(result['[AB42_13C6Leu_SP3]']+result['[AB42_SP3]']), label=r'A$\beta$42 PyAntiGen',color='red')
            
        ax1.scatter(df['time'], df['AB38_MFL'] , color='blue', label=r'A$\beta$38 data', alpha=0.6)
        ax1.scatter(df['time'], df['AB40_MFL'] , color='green', label=r'A$\beta$40 data', alpha=0.6)
        ax1.scatter(df['time'], df['AB42_MFL'] , color='red', label=r'A$\beta$42 data', alpha=0.6)
        ax1.scatter(df['time'], df['AB38_MFL_pred'] , marker='x', color='blue', label=r'A$\beta$38 2022', alpha=0.6)
        ax1.scatter(df['time'], df['AB40_MFL_pred'] , marker='x', color='green', label=r'A$\beta$40 2022', alpha=0.6)
        ax1.scatter(df['time'], df['AB42_MFL_pred'] , marker='x', color='red', label=r'A$\beta$42 2022', alpha=0.6)
        
        # Plot 2: Abconc
        ax2.scatter(df['time'], df['Abconc']/df['Abconc'][3], marker='o', color='black', label=r'A$\beta$ Conc. Data', alpha=0.6)
        ax2.scatter(df['time'], df['Abconc_pred'], marker='x', color='black', label=r'A$\beta$ Conc. 2022', alpha=0.6)
        ab40_total = (result['AB40_SP3'] + result['AB40_13C6Leu_SP3'])/result['V_SP3']
        ax2.plot(result['time'], ab40_total/ab40_total[0] , label=r'A$\beta$ Conc. PyAntiGen', color='purple')
        # ax2.plot(result['time'], result['[AB40_BrainISF]'] + result['[AB40_13C6Leu_BrainISF]'] , label='AB40 BrainISF', color='green')
        # ax2.plot(result['time'], result['[AB40_CV]'] + result['[AB40_13C6Leu_CV]'] , label='AB40 CV', color='red')
        # ax2.plot(result['time'], result['[AB40_SAS]'] + result['[AB40_13C6Leu_SAS]'] , label='AB40 SAS', color='blue')
        # ax2.plot(result['time'], result['[AB40_SP1]'] + result['[AB40_13C6Leu_SP1]'] , label='AB40 SP1', color='orange')
        # ax2.plot(result['time'], result['[AB40_SP2]'] + result['[AB40_13C6Leu_SP2]'] , label='AB40 SP2', color='yellow')
        # ax2.plot(result['time'], result['[AB40_SP3]'] + result['[AB40_13C6Leu_SP3]'] , label='AB40 SP3', color='black')
        
        # Plot 3: Q and V
        ax_flow.plot(result['time'], result['Q_Leak'], label=r'$Q_{Leak}$',color='blue')
        ax_flow.plot(result['time'], result['Q_LP'], label=r'$Q_{LP}$',color='green')
        # ax_flow.plot(result['time'], result['Q_refill'], label='Q_refill',color='red')
        ax_flow.plot(result['time'], result['Q_SN'], label=r'$Q_{SN}$',color='purple')
        ax_flow.plot(result['time'], result['V_SP3'], label=r'$V_{lumbar}$',color='orange')

    ax1.set_ylabel('Mol Fraction Labeled', fontsize=14)
    ax1.set_xlabel('Time (hours)', fontsize=14)
    ax2.set_ylabel('Concentration', fontsize=14)
    ax2.set_xlabel('Time (hours)', fontsize=14)
   
    for ax in (ax1, ax2):
        ax.set_xlim(0, 50)
        ax.grid(True, alpha=0.2)
        handles, labels_leg = ax.get_legend_handles_labels()
        by_label = dict(zip(labels_leg, handles))
        if by_label:
            ax.legend(by_label.values(), by_label.keys(), fontsize=9, ncol=1)

    fig.tight_layout()
    plot_name = os.path.join(plot_path, MODEL_NAME + ".png")
    fig.savefig(plot_name, bbox_inches="tight", dpi=300)
    print(f"Plot saved to: {plot_name}")
    
    ax_flow.set_xlabel('Time (hours)', fontsize=14)
    ax_flow.set_ylabel('Flow (mL/h) or Volume (mL)', fontsize=14)
    ax_flow.set_xlim(0, 48)
    ax_flow.grid(True, alpha=0.2)
    handles, labels_leg = ax_flow.get_legend_handles_labels()
    by_label = dict(zip(labels_leg, handles))
    if by_label:
        ax_flow.legend(by_label.values(), by_label.keys(), fontsize=14, ncol=2, loc='center left', bbox_to_anchor=(0.65, 0.75))
        
    fig_flow.tight_layout()
    plot_name_flow = os.path.join(plot_path, MODEL_NAME + "_Flows.png")
    fig_flow.savefig(plot_name_flow, bbox_inches="tight", dpi=300)
    print(f"Plot saved to: {plot_name_flow}")

    plt.show()