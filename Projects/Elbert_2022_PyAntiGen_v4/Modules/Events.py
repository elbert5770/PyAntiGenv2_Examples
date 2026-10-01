from pyantigen.generate.data_interpolation import generate_antimony_piecewise

def generate_no_events(replicate, df_dict):
    events = '' 
    return events

import numpy as np
from typing import List, Union, Tuple


def event_SILK(experiment, df_dict):

    df = df_dict["SILK"]
    # Q_CSF = r_ic["Q_CSF"]
    # Q_CSF = r_ic["Q_CSF"]
    Q_CSF = 17.39500698 # mL/h
    # V_SP3_0 = r_ic["V_SP3_0"]
    V_SP3_0 = 34.87516696 # mL
    # V_LP = r_ic["V_LP"]
    V_LP = 6 # mL
    # t_CSFdraw = r_ic["t_CSFdraw"]
    t_CSFdraw = 0.1 # h
    # f_SN = r_ic["f_SN"]
    f_SN = 0.1
    events = ''

    event_line = f"at (time >= 0.0 ): Q_Leak = 15.0"
    events += event_line + "\n"

    event_line = f"at (time >= 3.0 ): Q_Leak = 0.0"
    events += event_line + "\n"
 
    event_line = f"at (time > 20.0): Q_Leak = Q_CSF-Q_SN"
    events += event_line + "\n"

   
    event_line = f"at (time >= 30.0): Q_Leak = 0.0"
    events += event_line + "\n"

    
    event_line = f"at (time >= 48.0): Q_Leak = 0.0"
    events += event_line + "\n"

    events += hourly_events() + "\n"
    events += construct_volume_interpolation(Q_CSF,V_SP3_0,V_LP,t_CSFdraw) + "\n"
    events += construct_f13C6Leu_interpolation(df) + "\n"
    print(events)
    return events

def hourly_events():
    events = ''
    for i in range(0, 48):
        event_line = f"at (time >= {i}): Q_SN = 0.0, Q_LP = Q_CSF, Q_refill = Q_CSF - V_LP/t_CSFdraw"
        events += event_line + "\n"
        event_line = f"at (time >= {i} + t_CSFdraw):  Q_refill = Q_CSF"
        events += event_line + "\n"
        event_line = f"at (time >= {i} + V_LP/Q_CSF): Q_SN = f_SN*Q_CSF, Q_LP = Q_Leak, Q_refill = 0"
        events += event_line + "\n"
    return events

def construct_volume_interpolation(Q_CSF,V_SP3_0,V_LP,t_CSFdraw):
    
    slope1 = Q_CSF - V_LP/t_CSFdraw
    time_points = []
    data_points = []
    for i in range(0,48):
        time_points.append(i)
        time_points.append(i + t_CSFdraw)
        time_points.append(i + V_LP/Q_CSF)
        data_points.append(V_SP3_0)
        data_points.append(V_SP3_0 + slope1*t_CSFdraw)
        data_points.append(V_SP3_0)

    return generate_antimony_piecewise(time_points, data_points, data_name="V_SP3", default_before=V_SP3_0, default_after=V_SP3_0)

def construct_f13C6Leu_interpolation(df):
    times = df["time"].values
    data = df["PlasmaLeu"].values
    
    mask = ~(np.isnan(times) | np.isnan(data))
    times = times[mask]
    data = data[mask]

    return generate_antimony_piecewise(times, data, data_name="f_13C6Leu", default_before=0, default_after=0)

