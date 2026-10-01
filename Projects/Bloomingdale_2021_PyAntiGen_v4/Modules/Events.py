from pyantigen.generate.data_interpolation import generate_antimony_piecewise

def generate_no_events():
    events = '' 
    return events

def generate_IV_dose(experiment, df_dict):
    dose = experiment["dose"]
    pt_weight = experiment["pt_weight"]
    mol_wt = experiment["mol_wt"]
    events = 'at (time > 0): Antibody_Plasma = ' + str(dose[0]*pt_weight*1000*1000/mol_wt)
    events += '\n' + 'at (time > 0): Gadobutrol_CSF = 1000'
    return events



