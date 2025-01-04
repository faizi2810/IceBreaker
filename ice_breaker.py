import os
from langchain_core.prompts import PromptTemplate 
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from agents.linkedin_lookup_agent import lookup as likedin_lookup_agent
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from output_parsers import Summary, summaryOutputParser


load_dotenv()

def ice_break_with(name: str) -> str:
    linkedin_url = likedin_lookup_agent(name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)

    twitter_username = twitter_lookup_agent(name)
    tweets = scrape_user_tweets(username=twitter_username, mock=True)


    summary_prompt = """
    give the information about a person from Linkedin {information} and twitter posts {twitter_posts} I want you to create:
    1. a short summary
    2. two interesting facts about them
    
    Use both information from Linkedin and Twitter.
    \n{format_instructions}
    """
    

    summary_prompt_template = PromptTemplate(input_variables=["information"],
                                            template=summary_prompt,
                                            partial_variables= {
                                                "format_instructions": summaryOutputParser.get_format_instructions()
                                            })

    # llm = ChatOpenAI(temperature=0, api_key=os.environ.get('OPENAI_API_KEY'), model="gtp-3.5-turbo")
    llm = ChatOllama(model="llama3")

    # chain = summary_prompt_template | llm | StrOutputParser
    chain = summary_prompt_template | llm | summaryOutputParser

    res: Summary = chain.invoke(input={"information": linkedin_data, "twitter_posts": tweets})

    return res, linkedin_data.get("profile_pic_url")


if __name__ == '__main__':
    print(os.environ.get('OPENAI_API_KEY'))
    ice_break_with("Eden Marco Udemy")

    
    