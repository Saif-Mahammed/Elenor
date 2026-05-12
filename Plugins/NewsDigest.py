import requests
from bs4 import BeautifulSoup

def can_handle(command):
    return "news digest" in command.lower() or "top headlines" in command.lower()

def execute(command):
    try:
        url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en" # Google News RSS for top headlines
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        articles = soup.find_all('item')
        
        digest = "Here are the top headlines:
"
        for i, article in enumerate(articles[:5]): # Get top 5 headlines
            title = article.find('title').text
            link = article.find('link').text
            digest += f"{i+1}. {title}
" # Link: {link}
"
        return digest
    except Exception as e:
        return f"Error fetching news digest: {e}"

