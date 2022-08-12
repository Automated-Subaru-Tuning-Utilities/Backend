import sys
import numpy as np 
import pandas as pd

sys.path.append("./models")
from lowmaf_model import lowmaf_data
from typing import List

# step 1
# construct dmaf/dt column
# filter out values >.3
def dmafdt(df):
    # create dmaf/dt column
    df.loc[0, "dmafdt"] = 0.0
    for i in range(1, len(df)):
        time1 = df.loc[i-1, "time"]
        time2 = df.loc[i, "time"]
        maf1 = df.loc[i-1, "mass_airflow_voltage"]
        maf2 = df.loc[i, "mass_airflow_voltage"]
        df.loc[i, "dmafdt"] = abs( ((1000)*(maf2-maf1))/(time2-time1) )
    # filter out too large values
    df = df[df["dmafdt"] < .31]
    df.reset_index(drop=True, inplace=True) 
    return df

# Step 2
# Filter out OL values
# Filter out IAT valed > threshold
def outlier_filter(df, iat_threshold):
    df = df[df["cl_ol_status"] == 8]
    df = df[df["intake_air_temp"] < iat_threshold]
    df.reset_index(drop=True, inplace=True) 
    return df

# Step 3
# Calculate Overall correction = af_correction_short + af_correction_learning
def overall_correction(df):
    df.loc[0, "correction"] = 0.0
    for i in range(1 , len(df)):
        df.loc[i, "correction"] = df.loc[i, "af_correction_short"] + df.loc[i, "af_correction_learning"]
    return df

#Step 4, matches corrections observed with cooresponding mafv entry
# calculates a mean of corrections observed for each entry
def match_maf(df):
    maf_voltages = [
                    [0.00],
                    [0.94],
                    [0.98],
                    [1.02],
                    [1.05],
                    [1.09],
                    [1.13],
                    [1.17],
                    [1.21],
                    [1.25],
                    [1.29],
                    [1.33],
                    [1.37],
                    [1.41],
                    [1.48],
                    [1.56],
                    [1.64],
                    [1.72],
                    [1.80],
                    [1.87],
                    [1.95],
                    [2.03],
                    [2.11],
                    [2.19],
                    [2.27],
                    [2.34],
                    [2.42],
                    [2.54],
                    [2.66],
                    [2.77],
                    [2.89],
                    [3.01],
                    [3.12]
                ]
    for i in range (0, len(maf_voltages)-1):
        # print(i)
        vals = df[(df["mass_airflow_voltage"] > maf_voltages[i][0]) & (df["mass_airflow_voltage"] < maf_voltages[i+1][0])]
        mean = vals["correction"].mean()
        maf_voltages[i].append(mean)
    return maf_voltages

def main(log: List[lowmaf_data]):
    df = pd.DataFrame(log)
    df = dmafdt(df)
    df = outlier_filter(df, 55)
    df = overall_correction(df)
    result = match_maf(df)
    return result

if __name__ == "__main__":
    testing_data = [
                {
                    "time": 0,
                    "af_correction_short": -4.5,
                    "af_correction_learning": 0.5,
                    "intake_air_temp": 44,
                    "mass_airflow_voltage": 2.1,
                    "cl_ol_status": 8
                },
                {
                    "time": 500,
                    "af_correction_short": 15.5,
                    "af_correction_learning": 0.5,
                    "intake_air_temp": 48,
                    "mass_airflow_voltage": 2.2,
                    "cl_ol_status": 8
                },
                {
                    "time": 1000,
                    "af_correction_short": 12.1,
                    "af_correction_learning": 1,
                    "intake_air_temp": 49,
                    "mass_airflow_voltage": 2.8,
                    "cl_ol_status": 8
                },
                {
                    "time": 1500,
                    "af_correction_short": 12.1,
                    "af_correction_learning": 1,
                    "intake_air_temp": 47,
                    "mass_airflow_voltage": 2.95,
                    "cl_ol_status": 8
                },
                {
                    "time": 2000,
                    "af_correction_short": 12.1,
                    "af_correction_learning": 1,
                    "intake_air_temp": 50,
                    "mass_airflow_voltage": 2.75,
                    "cl_ol_status": 8
                },
                {
                    "time": 2500,
                    "af_correction_short": 12.1,
                    "af_correction_learning": 1,
                    "intake_air_temp": 60,
                    "mass_airflow_voltage": 2.76,
                    "cl_ol_status": 10
                },
                {
                    "time": 3000,
                    "af_correction_short": 12.1,
                    "af_correction_learning": 1,
                    "intake_air_temp": 52,
                    "mass_airflow_voltage": 2.78,
                    "cl_ol_status": 8
                }

            ]
    main(testing_data)