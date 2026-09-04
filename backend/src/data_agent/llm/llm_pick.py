from langchain_openai import ChatOpenAI

from dotenv import load_dotenv


load_dotenv()


def llm_pick(level: str):
    """
    Pick the appropriate LLM based on the requested level.

    Args:
        level: "low", "medium", or "high".

    Returns:
        Configured ChatOpenAI instance.
    """

    if level.lower() == "low":
        llm = ChatOpenAI(
            model_name="gpt-5.6-luna",
            temperature=0,
            reasoning_effort="none",
        )

    elif level.lower() == "medium":
        llm = ChatOpenAI(
            model_name="gpt-5.6-terra",
            temperature=0,
            reasoning_effort="none",
        )

    elif level.lower() == "high":
        llm = ChatOpenAI(
            model_name="gpt-5.6-sol",
            temperature=0,
            reasoning_effort="none",
        )

    else:
        raise ValueError(
            "Invalid level specified. Please choose from "
            "'low', 'medium', or 'high'."
        )

    return llm

