from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
import numpy as np
import sys

#lowmaf
sys.path.append("lowmaf/models/")
sys.path.append("lowmaf/")
from lowmaf_model import lowmaf_data 
import lowmaf_calc

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#lowmaf route
@app.post("/api/analyze/0/")
def read_data( log: List[lowmaf_data] ):
    #resp = lowmaf_calc.main(log)
    #resp = dict(resp)
    resp = "Hello from FASTAPI. Your data has been received!"
    return resp

# what @Dominic-W was using
#async def read_data( log: list[lowmaf_data] ):
#    #currently testing
#    data = [item.dict() for item in log]
#    df = pd.DataFrame.from_records(data) #fails
#    return df    
