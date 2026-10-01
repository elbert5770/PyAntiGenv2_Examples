import pandas as pd
import os


def load_no_data(experiment, data_path):
    data_dict = {}  
    return data_dict


def load_PK_data(experiment, data_path):
    experiment_path = os.path.join(data_path, 'PK_Predictions.csv')
    df = pd.read_csv(experiment_path)
    data_dict = {
        "PK data": df
    }
    return data_dict







