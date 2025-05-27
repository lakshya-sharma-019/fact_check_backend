from fastapi import FastAPI
app = FastAPI()

from pydantic import BaseModel
from typing import List
from datetime import datetime
import json
from fastapi.middleware.cors import CORSMiddleware
import os
from scripts import *
import uvicorn

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Submission(BaseModel):
    user_id: str
    input_text: str

@app.post("/")
def read_root():
    return {"message": "Hello, world!"}
    
@app.post("/submit/now/all/")
def get_grounded_fact_check(submission:Submission):
    response_json= get_fact_check_vertex(submission.input_text)
    with open('response.json', 'w') as f:
        json.dump(response_json, f)
    analysis_markdown=get_analysis_markdown(response_json)
    id_uri_mapping, uri_title_mapping=get_url_mapping(response_json)
    claimwise_supports=get_claimwise_supports(response_json)
    report= {'analysis':analysis_markdown, 
            'id_uri_mapping':id_uri_mapping, 
            'uri_title_mapping':uri_title_mapping, 
            'claimwise_supports':claimwise_supports}
    return report  

