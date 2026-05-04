import requests
import os
from dotenv import load_dotenv
from langchain.tools import tool

load_dotenv('../.secrets')

@tool
def get_news():
    """This api retrieves the top headlines"""
    apikey = os.getenv("GNEWS_KEY")
    category = "business"
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=ca&max=10&apikey={apikey}"
    response = requests.get(url)
    data = response.json()
    articles = data["articles"]
    print(articles)
    return articles
