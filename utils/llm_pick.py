from langchain_openai import ChatOpenAI

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

def llm_pick(Level:str):
    """
    Picks the appropriate LLM (Language Model) based on the specified level.

    Args:
        Level (str): The level of the LLM to pick. Possible values are "Basic", "Intermediate", and "Advanced".

    Returns:
        str: The name of the selected LLM.
    """
    
    if Level.lower() == "low":
        llm= ChatOpenAI(model_name="gpt-5.6-luna", temperature=0)
    elif Level.lower() == "medium":
        llm= ChatOpenAI(model_name="gpt-5.6-terra", temperature=0)
    elif Level.lower() == "high":
        llm= ChatOpenAI(model_name="gpt-5.6-sol", temperature=0)

    else:
        raise ValueError("Invalid level specified. Please choose from 'low', 'medium', or 'high'.")

    return llm


