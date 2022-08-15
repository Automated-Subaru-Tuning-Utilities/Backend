import sys
import numpy as np 
import pandas as pd

sys.path.append("./models")
from lowmaf_model import lowmaf_data
from maf_voltages import maf_voltages

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

# Step 4, matches corrections observed with cooresponding mafv entry
# calculates a mean of corrections observed for each entry
# maf_voltages imported from ./models/maf_voltages.py
def match_maf(df):
    for i in range (0, len(maf_voltages)-1):
        vals = df[(df["mass_airflow_voltage"] > maf_voltages[i][0]) & (df["mass_airflow_voltage"] < maf_voltages[i+1][0])]
        mean = vals["correction"].mean()
        mean = np.around(mean, decimals=5)
        if (np.isnan(mean)):
            mean = 0
        maf_voltages[i].append(mean)
    return maf_voltages

def main(data):
    df = pd.DataFrame([item.dict() for item in data])
    df = dmafdt(df)
    df = outlier_filter(df, 55)
    df = overall_correction(df)
    result = match_maf(df)
    print("Results: ")
    print(result)
    return result

if __name__ == "__main__":
    print("use this section for testing")