from fastapi import APIRouter
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

from data_agent.agents.data_agent import data_agent


router = APIRouter()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    route: str


@router.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@router.post("/api/v1/query", response_model=QueryResponse)
def query(request: QueryRequest):
    initial_state = {
        "messages": [HumanMessage(content=request.question)]
    }

    response = data_agent.invoke(initial_state)

    final_message = response["messages"][-1].content
    route = response["routerResponse"]

    return QueryResponse(
        answer=final_message,
        route=route,
    )