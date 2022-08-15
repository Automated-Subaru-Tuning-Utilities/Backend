from fastapi import FastAPI
import pandas as pd
import numpy as np
import sys

#lowmaf
sys.path.append("lowmaf/models/")
sys.path.append("lowmaf/")
from lowmaf_model import lowmaf_data 
import lowmaf_calc

app = FastAPI()

#lowmaf route
@app.post("/api/analyze/0/")
async def read_data( log: list[lowmaf_data] ):
    #currently testing
    data = [item.dict() for item in log]
    df = pd.DataFrame.from_records(data) #fails
    return df    
