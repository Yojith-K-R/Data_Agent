from langchain.messages import HumanMessage
from langgraph.graph import START, StateGraph, END
from Models.schema import DataAgentState, RouterSchema
from utils.llm_pick import llm_pick

from typing import Literal
from agents.etl_analyst import etlAgent
from utils.llm_pick import llm_pick
from agents.sql_analyst import sql_agent_workflow
from Models.schema import AgentState
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
load_dotenv()

llm=llm_pick('low')

llm_router=llm.with_structured_output(RouterSchema)

# response=llm_router.invoke("I need to extract some data from api and load it into csv")

# print(response.answer)


def routerNode(state:DataAgentState):
    user_question=state.messages[-1].content
    routerResponse=llm_router.invoke(user_question)
    state.routerResponse=routerResponse.answer

    return {
        'routerResponse':routerResponse.answer
    }

def etl_node(state:DataAgentState):
    result = etlAgent.invoke(
                {
                    "messages": [state.messages[-1]]
                }
            )
        
    final_message=result['messages'][-1]
    return {
        'messages':[final_message]
    }



def sql_node(state:DataAgentState):
    initial_state = AgentState(
            user_question=state.messages[-1].content
        )
    
    result = sql_agent_workflow.invoke(initial_state)  
    # print(type(result))
    print(result['messages'])
    print("__________")
    print(result['curated_question'])
    print("__________")
    print(result['generated_sql_query'])
    print("__________")
    print(result['sql_query_execution_result'])
    print("__________")
    print(result['final_answer'])

    final_message=result['messages'][-1]
    return {
        'messages':[final_message]
    }

def checkRoute(state:DataAgentState)->Literal['sql','etl']:
    if state.routerResponse=='etl':
        return 'etl'
    else:
        return 'sql'

graph = StateGraph(DataAgentState)

graph.add_node('routerNode',routerNode)
graph.add_node('etl_node',etl_node)
graph.add_node('sql_node',sql_node)

graph.add_edge(START,'routerNode')
graph.add_conditional_edges('routerNode',checkRoute,{
    'etl':'etl_node',
    'sql':'sql_node'
})

graph.add_edge('etl_node',END)
graph.add_edge('sql_node',END)

data_agent=graph.compile()



if __name__ == "__main__":

    # intialState={
    #     'messages':[HumanMessage(content='Show me the top 10 customers based on total payments')]
        
    # }
    intialState={
        'messages':[HumanMessage(content="I need to extract only the names starting with 'c' from 'extractedData/extracted_data.csv' this  csv file and then save it into the output folder 'transformedData1/transformed.csv'")]
        
    }
    # intialState={
    #     'messages':[HumanMessage(content="What is agent capable of doing")]
        
    # }
    response=data_agent.invoke(intialState)

    print(response)
    print(response['messages'][-1].content)