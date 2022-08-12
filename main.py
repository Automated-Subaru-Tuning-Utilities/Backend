from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

class lowmaf(BaseModel):
    time: int 
    af_correction_short: float
    af_correction_learning: float
    intake_air_temp: int
    mass_airflow_voltage: float
    cl_ol_status: int

app = FastAPI()

@app.post("/api/{parameters}")
async def read_data( parameters:str, log: List[lowmaf] ):
    if (parameters == "lowmaf"):
        return log
    return {
        "parameters": parameters
    }
