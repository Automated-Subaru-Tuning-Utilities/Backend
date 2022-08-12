from fastapi import FastAPI
from typing import List

import sys
sys.path.append("lowmaf/models/")
from lowmaf import lowmaf_data 

app = FastAPI()

#lowmaf
@app.post("/api/analyze/0/")
async def read_data( log: List[lowmaf_data] ):
    return log
