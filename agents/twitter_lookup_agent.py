import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain.agents import (create_react_agent, AgentExecutor)
from langchain import hub
from langchain_core.tools import Tool

from tools.tools import get_profile_url_tavily


def lookup(name:str)-> str:
    llm = ChatOllama(model="llama3")
    template="""given the full name {name_of_person} i want you to find a link to their twitter profile page and extract from it their username.
    Your answer should only be person's username"""
    
    prompt_template = PromptTemplate(inputVariables={"name_of_person"}, template=template)

    tools_for_agent = [
        Tool(
            name= "Crawl Google 4 Twitter profile page",
            func=get_profile_url_tavily,
            description="Useful for when you need to get the Twitter profile page"
        )
    ]

    react_Prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(
        llm=llm,
        tools = tools_for_agent,
        prompt=react_Prompt,
    )

    agent_executor = AgentExecutor(agent = agent, tools = tools_for_agent, verbose=True, handle_parsing_errors=True)

    result = agent_executor.invoke(input = { "input":prompt_template.format_prompt(name_of_person=name)})

    twitter_username = result["output"]
    return twitter_username