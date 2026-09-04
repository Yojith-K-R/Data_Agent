from fastapi import FastAPI
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from agents.data_agent import data_agent

class QueryRequest(BaseModel):
    question:str

class QueryResponse(BaseModel):
    answer:str
    route:str



app=FastAPI(
    title="Data Agent API",
    version="0.1.0",
)

@app.get("/api/v1/health")
def health_check():
    return {"status":"ok"}

@app.post("/api/v1/query",response_model=QueryResponse)
def query(request:QueryRequest):
    intialState={
        "messages":[HumanMessage(content=request.question)]
    }
    response=data_agent.invoke(intialState)
    final_message=response['messages'][-1].content
    route=response['routerResponse']
    return QueryResponse(answer=final_message,route=route)