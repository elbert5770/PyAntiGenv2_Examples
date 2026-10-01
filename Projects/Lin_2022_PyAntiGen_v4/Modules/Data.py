import pandas as pd
import os


def load_no_data(replicate, data_path):
    data_dict = {}  
    return data_dict


def load_Lin_data(experiment, data_path):
    experiment_path = os.path.join(data_path, 'sim1_data_small.csv')
    df = pd.read_csv(experiment_path)
    data_dict = {
        "Lin_data": df
    }
    return data_dict



