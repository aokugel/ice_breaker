import os

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets_mock
from third_parties.bluesky import scrape_user_tweets as scrape_bluesky_tweets
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from agents.bluesky_lookup_agent import lookup as bluesky_lookup_agent


def ice_break_with(name: str) -> str:
    #linkedin_url = linkedin_lookup_agent(name)
    bluesky_account = bluesky_lookup_agent(name=name)
    print(bluesky_account)
    linkedin_url = "https://www.linkedin.com/in/jeffgerstmann/"
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url, mock=True)
    print(linkedin_data)
    #twitter_data = scrape_user_tweets_mock()
    twitter_data = scrape_bluesky_tweets(username=bluesky_account)
    summary_template = """
        given the Linkedin information {linkedin_info} about a person from I want you to create:
        1. a short summary
        2. two interesting facts about them

        and given the and Twitter information {twitter_info} about this person I want you to tell me what they've been up to recently
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["linkedin_info", "twitter_info"], template=summary_template
    )

    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

    chain = summary_prompt_template | llm | StrOutputParser()
    res = chain.invoke(input={"linkedin_info": linkedin_data,
                              "twitter_info": twitter_data})
    return res

if __name__ == "__main__":

    icebreaker_info = ice_break_with("Jeff Gerstmann")
    print(icebreaker_info)
