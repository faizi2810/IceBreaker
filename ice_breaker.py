import os
from langchain_core.prompts import PromptTemplate 
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from agents.linkedin_lookup_agent import lookup
from third_parties.linkedin import scrape_linkedin_profile


load_dotenv()

def ice_break_with(name: str) -> str:
    linkedin_url = lookup(name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)


    summary_prompt = """
    give the linkedin information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them"""

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_prompt)

    # llm = ChatOpenAI(temperature=0, api_key=os.environ.get('OPENAI_API_KEY'), model="gtp-3.5-turbo")
    llm = ChatOllama(model="llama3")

    chain = summary_prompt_template | llm | StrOutputParser()

    res = chain.invoke(input={"information": linkedin_data})

    print(res)


if __name__ == '__main__':
    print(os.environ.get('OPENAI_API_KEY'))
    ice_break_with("Eden Marco Udemy")

    
    