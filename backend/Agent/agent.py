import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
# from Agent.tools import get_uavs, get_uav_by_id, get_uavs_by_user, get_available_uavs

load_dotenv()

def get_agent():
    """
    Initializes and returns a LangChain agent with the specified LLM provider.
    The agent is configured with a system prompt and a set of tools for UAV management.
    """
    llm_provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if llm_provider == "gemini":
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", convert_system_message_to_human=True)
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")

    # tools = [get_uavs, get_uav_by_id, get_uavs_by_user, get_available_uavs]

    system_prompt = """
        You are a helpful assistant for the UAV management system named "Mission Control Copilot".
        You have access to a set of tools to answer user questions about UAVs.
        Always be polite and helpful.
        When asked a question, use the available tools to find the answer.
        If you can't find the answer, just say that you don't have enough information.
    """

    # Create agent with correct parameter order
    agent = create_agent(
        model=llm,
        # tools=tools,
        system_prompt=system_prompt
    )

    return agent