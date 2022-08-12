import sys
sys.path.append("./models")
from lowmaf_model import lowmaf_data
from typing import List

def main(log: List[lowmaf_data]):
    print(log[1]["time"])
    return {"resp": "testing"}

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
                    "mass_airflow_voltage": 2.2,
                    "cl_ol_status": 8
                },
                {
                    "time": 200,
                    "af_correction_short": 12.1,
                    "af_correction_learning": 1,
                    "intake_air_temp": 60,
                    "mass_airflow_voltage": 2.3,
                    "cl_ol_status": 8
                }
            ]
    main(testing_data)