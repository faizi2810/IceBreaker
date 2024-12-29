import os
from langchain_core.prompts import PromptTemplate 
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

from third_parties.linkedin import scrape_linkedin_profile


load_dotenv()

if __name__ == '__main__':
    print(os.environ.get('OPENAI_API_KEY'))


    summary_prompt = """
    give the linkedin information {information} about a person from I want you to create:
    1. a short summary
    2. two interesting facts about them"""

    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_prompt)

    # llm = ChatOpenAI(temperature=0, api_key=os.environ.get('OPENAI_API_KEY'), model="gtp-3.5-turbo")
    llm = ChatOllama(model="llama3")

    chain = summary_prompt_template | llm | StrOutputParser()

    linkedin_data = scrape_linkedin_profile("https://www.linkedin.com/in/muhammad-faizan-ahmad/", True)

    res = chain.invoke(input={"information": linkedin_data})

    print(res)