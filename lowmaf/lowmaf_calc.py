import sys
import numpy as np 
import pandas as pd

sys.path.append("./models")
from lowmaf_api_model import lowmaf_input
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
    # we go from index = 0 to index = len -1 in the loop because we need a special case for the first and last indicies
    # check length once for optimization (although compiler might do this)
    maf_voltages_length = len(maf_voltages) - 1
    # for index 0, we check values >=0 and <.94
    # this is due to the way that ECUflash handles interpolation
    vals = df[(df["mass_airflow_voltage"] >= 0) & (df["mass_airflow_voltage"] < maf_voltages[0]["MafVoltage"])]
    freq = len(vals)
    if (freq > 0):
        mean = vals["correction"].mean()
        mean = np.around(mean, decimals=5)
        maf_voltages[0]["Correction"] = mean
        maf_voltages[0]["Frequency"] += freq
    for i in range (1, maf_voltages_length):
        vals = df[(df["mass_airflow_voltage"] >= maf_voltages[i]["MafVoltage"]) & (df["mass_airflow_voltage"] < maf_voltages[i+1]["MafVoltage"])]
        freq = len(vals)
        if (freq > 0):
            mean = vals["correction"].mean()
            mean = np.around(mean, decimals=5)
            maf_voltages[i]["Correction"] = mean
            maf_voltages[i]["Frequency"] += freq
    # special case for last index
    # we check values >4.69 and <= 5.0
    vals = df[(df["mass_airflow_voltage"] > maf_voltages[len(maf_voltages)-1]["MafVoltage"]) & (df["mass_airflow_voltage"] <= 5.0)]
    freq = len(vals)
    if (len(vals) > 0):
        mean = vals["correction"].mean()
        mean = np.around(mean, decimals=5)
        maf_voltages[maf_voltages_length]["Correction"] = mean
        maf_voltages[maf_voltages_length]["Frequency"] += freq

    return maf_voltages

def main(data: list[lowmaf_input]):
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