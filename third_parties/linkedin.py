import os
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile."""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/faizi2810/1f92232a17111b9645ead46116b61196/raw/63448eb781d48ed6fb949f1fad76fc46eec1c700/linkedin_profile.json"
        response = requests.get(linkedin_profile_url, timeout=10)
    else:
        header_dic = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        params = {
            'url': linkedin_profile_url,
        }
        response = requests.get(api_endpoint,
                                params=params,
                                headers=header_dic)
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }   
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
            
    return data



if __name__ == '__main__':
    linkedin_profile_url = "https://www.linkedin.com/in/muhammad-faizan-ahmad/"
    scrape_linkedin_profile(linkedin_profile_url, True)