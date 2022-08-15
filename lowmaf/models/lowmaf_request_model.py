from pydantic import BaseModel

class lowmaf_input(BaseModel):
    time: int 
    af_correction_short: float
    af_correction_learning: float
    intake_air_temp: int
    mass_airflow_voltage: float
    cl_ol_status: int
