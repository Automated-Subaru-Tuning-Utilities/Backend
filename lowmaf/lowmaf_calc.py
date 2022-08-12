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
    return df

# Step 2
# Filter out OL values
# Filter out IAT valed > threshold
def outlier_filter(df, iat_threshold):
    df = df[df["cl_ol_status"] == 8]
    df = df[df["intake_air_temp"] < iat_threshold]
    return df
    
def main(log: List[lowmaf_data]):
    df = pd.DataFrame(log)
    df = dmafdt(df)
    df = outlier_filter(df, 55)
    print(df)

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