import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from .tools import (
    get_station_data, 
    get_s1_data, get_altitude_data, 
    get_b1_data, 
    get_gps_latlng_data, 
    get_s2_data, 
    get_s3_data, 
    get_slide1_data, 
    get_slide2_data, 
    get_speed_data,
    query_influxdb
)
from Services.Chat import ChatService
from Security.jwt import get_current_user
from Models import get_db

load_dotenv()

def get_agent():
    """
    Initializes and returns a LangChain agent with the specified LLM provider.
    The agent is configured with a system prompt and a set of tools for UAV management.
    """
    llm_provider = os.getenv("LLM_PROVIDER", "ollama").lower()

    if llm_provider == "ollama":
        ollama_host = os.getenv("OLLAMA_HOST", "http://ollama_facsec")
        ollama_port = os.getenv("OLLAMA_PORT", "11434")
        llm = ChatOllama(
            base_url=f"{ollama_host}:{ollama_port}",
            model=os.getenv("OLLAMA_MODEL", "llama2")
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {llm_provider}")

    tools = [get_station_data, get_s1_data, get_altitude_data, get_b1_data, get_gps_latlng_data, get_s2_data, get_s3_data, get_slide1_data, get_slide2_data, get_speed_data, query_influxdb]

    db: Session = next(get_db())
    current_user: UserModel = Depends(get_current_user)
    chat_context = ChatService.get_conversations_by_user(current_user.id, db)

    context = ""
    for conversation in chat_context:
        for message in conversation.messages:
            context += f"User: {message.user_prompt}\nAI: {message.response}\n\n"


    system_prompt = """
        You are a helpful assistant for the UAV management system named "Mission Control Copilot".
        You have access to a set of tools to answer user questions about UAVs.
        Always be polite and helpful.
        When asked a question, use the available tools to find the answer.
        If you can't find the answer, just say that you don't have enough information.

        Previous Conversations:
        {context}  # Include the previous conversation context here
    """

    # Create agent with correct parameter order
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )

    return agent