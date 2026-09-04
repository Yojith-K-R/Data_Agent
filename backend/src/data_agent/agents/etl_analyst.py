from langchain.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import START, StateGraph, END
from langgraph.prebuilt import ToolNode
from models.schema import ETLAgentSchema
from etl.etl_tools import ETLTools
from llm.llm_pick import llm_pick
from pathlib import Path


@tool
def extract_load_tool(url:str,format:str,output_folder:str="extractedData")->str:
    """
    This tool extracts the data from the API (url) and loads it into the
    the desired location (output_folder).

    Args:
        url (str): The API endpoint from which to extract data.
        output_folder (str): The folder where the extracted data will be saved.
        format (str): The format in which to save the extracted data (csv, json, parquet).
    
    Returns:
        str: A message indicating the success or failure of the operation.

    """
    etlTool=ETLTools()
    result=etlTool.extract_load(url,output_folder,format)

    return result


@tool
def transform_load_context_tool(output_folder:str,output_format:str,user_question:str,input_file_path:str="extractedData/extracted_data.csv",)->str:
    """
    This tool transforms the data from the specified file and loads it into the
    desired location (output_folder).

    Args:
        input_file_path (str): The path to the file containing the data to be transformed.
        output_folder (str): The folder where the transformed data will be saved.
        output_format (str): The format in which to save the transformed data (csv, json, parquet).
    
    Returns:
        str: A message indicating the success or failure of the operation.

    """

    etlTool=ETLTools()
    input_file_final=Path(__file__).resolve().parent.parent/"data"/"ETL"/input_file_path
    top_3_rows= etlTool.transform_load_context(input_file_path)
    # print(f"Top 3 rows\n{top_3_rows}")

    output_folder_final=Path(__file__).resolve().parent.parent/"data"/"ETL"/output_folder

    # print(f"output folder final {output_folder_final}")

    prompt = f"""
            You are a Python Data Analyst who uses Pandas to analyze data. 
            You need to provide only the Pandas Code that will help to perform the right ETL operations on the data stored in the file : {input_file_final}
            as per the user's question. Do not provide any explanation or comments, only
            the code should be provided. The code should be in a format that can be executed 
            in a Python environment with Pandas installed. 
            Don't write anything else than Pandas Code. \n
            
            Create the Pandas Dataframe from the data stored in the file : {input_file_final} and then 
            write the code to transform and save the data at {output_folder_final}.
            Here's the user's question: {user_question}\n
            Here's the context of the data you will be analyzing: {top_3_rows}\n

        """


    llm=llm_pick("medium")

    response = llm.invoke(prompt).content 

    # Optional Cleaning
    pandas_code = response.strip().strip('```').strip().lstrip('python').strip()

    # Execute the Pandas code
    results = etlTool.execute_code(pandas_code)

    return f"The data is transformed and saved at {output_folder_final} in {output_format} format. \n\n Pandas Code Executed: \n {pandas_code} \n\n Execution Result: \n {results}"


tools=[extract_load_tool,transform_load_context_tool]

llm=llm_pick('high')
llm_with_tools = llm.bind_tools(tools)


# ==========================================
# AGENT NODE
# ==========================================

def agent_node(state: ETLAgentSchema):

    response = llm_with_tools.invoke(
        state.messages
    )

    # print(state.messages)

    return {
        "messages": [response]
    }

# ==========================================
# TOOL NODE
# ==========================================

tool_node = ToolNode(tools)


# ==========================================
# CONDITIONAL ROUTING
# ==========================================

def should_continue(state: ETLAgentSchema):

    last_message = state.messages[-1]

    if last_message.tool_calls:
        return "tools"

    return "end"

# ==========================================
# GRAPH
# ==========================================

graph = StateGraph(ETLAgentSchema)


# Add nodes

graph.add_node(
    "agent",
    agent_node
)

graph.add_node(
    "tools",
    tool_node
)


# START → AGENT

graph.add_edge(
    START,
    "agent"
)


# AGENT → TOOLS or END

graph.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        "end": END
    }
)


# TOOLS → AGENT

graph.add_edge(
    "tools",
    "agent"
)


# Compile

etlAgent = graph.compile()


if __name__ == "__main__":
    # ==========================================
    # RUN
    # ==========================================

    # result = etlAgent.invoke(
    #     {
    #         "messages": [HumanMessage(content="I want to extract the data from the API endpoint 'https://pokeapi.co/api/v2/pokemon' and save it to 'extractedData' folder as csv file")]
    #     }
    # )
    result = etlAgent.invoke(
        {
            "messages": [HumanMessage(content="I need to extract only the names starting with 'c' from 'extractedData/extracted_data.csv' this  csv file and then save it into the output folder 'transformedData/transformed.csv'")]
        }
    )

    print()


    for msg in result['messages']:
        print(type(msg))
        print(msg.content)
        try:
            print(msg.tool_calls)

        except:
            print("No tool calls present")
        print()


