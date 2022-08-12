import sys
import numpy as np 
import pandas as pd

sys.path.append("./models")
from lowmaf_model import lowmaf_data
from typing import List

# step 1
# construct dmaf/dt column
def dmafdt(df):
    df.loc[0, "dmafdt"] = 0.0
    for i in range(1, len(df)):
        time1 = df.loc[i-1, "time"]
        time2 = df.loc[i, "time"]
        maf1 = df.loc[i-1, "mass_airflow_voltage"]
        maf2 = df.loc[i, "mass_airflow_voltage"]
        df.loc[i, "dmafdt"] = ((1000)*(maf2-maf1))/(time2-time1)
    print(df["dmafdt"])

def main(log: List[lowmaf_data]):
    df = pd.DataFrame(log)
    dmafdt(df)

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
                    "time": 100,
                    "af_correction_short": 15.5,
                    "af_correction_learning": 0.5,
                    "intake_air_temp": 48,
                    "mass_airflow_voltage": 2.5,
                    "cl_ol_status": 8
                },
                {
                    "time": 200,
                    "af_correction_short": 12.1,
                    "af_correction_learning": 1,
                    "intake_air_temp": 60,
                    "mass_airflow_voltage": 2.8,
                    "cl_ol_status": 8
                }
            ]
    main(testing_data)