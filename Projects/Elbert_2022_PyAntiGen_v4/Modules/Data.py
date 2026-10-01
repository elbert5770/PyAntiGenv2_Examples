import pandas as pd
import os


def load_no_data(replicate, data_path):
    data_dict = {}  
    return data_dict


def load_SILK_data(experiment, data_path):
    experiment_path = os.path.join(data_path, 'Elbert_2022_all_data.csv')
    df = pd.read_csv(experiment_path)
    data_dict = {
        "SILK": df
    }
    return data_dict


