from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from data_agent.agents.data_agent import data_agent


router = APIRouter()


class QueryRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Natural-language question for the data agent.",
    )


class QueryResponse(BaseModel):
    answer: str
    generated_sql_query:str|None=None
    route: str


@router.get("/api/v1/health")
def health_check():
    return {"status": "ok"}


@router.post("/api/v1/query", response_model=QueryResponse)
def query(request: QueryRequest):
    initial_state = {
        "messages": [HumanMessage(content=request.question)]
    }

    try:
        response = data_agent.invoke(initial_state)

        final_message = response["messages"][-1].content
        route = response["routerResponse"]
        generated_sql_query=response["generated_sql_query"]
        return QueryResponse(
            answer=final_message,
            route=route,
            generated_sql_query=generated_sql_query
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to process the query.",
        ) from exc