import os
import requests

def hello_world():
    print("hello world")

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles, 
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = 'https://gist.githubusercontent.com/aokugel/7ec52c573b2f64b56eb5fd0def25b92f/raw/4092872b46aec1733c66e36074d8c6b03ed0649b/gistfile1.txt'
        response = requests.get(
            linkedin_profile_url,
            timeout=10
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header_dic = {"Authorization" : f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=header_dic,
            timeout=10
        )

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


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(linkedin_profile_url="", mock=True)
    )