from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List
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
async def read_data( log: List[lowmaf_data] ):
    #resp = lowmaf_calc.main(log)
    return log
