from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

driver = None

def get_webdriver():
    global driver
    if driver is None:
        chrome_options = Options()
        chrome_options.add_argument("--headless") # Run in background
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def can_handle(command):
    return any(keyword in command.lower() for keyword in ["browse to", "summarize page", "find on page"])

def execute(command):
    try:
        browser = get_webdriver()
        if "browse to" in command.lower():
            url = command.lower().split("browse to")[1].strip()
            if not url.startswith("http"):
                url = "https://" + url
            browser.get(url)
            return f"Successfully browsed to {url}. Current page title: {browser.title}"
        elif "summarize page" in command.lower():
            soup = BeautifulSoup(browser.page_source, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join([p.get_text() for p in paragraphs if p.get_text().strip()][:5]) # Summarize first 5 paragraphs
            return f"Summary of current page: {text}..."
        elif "find on page" in command.lower():
            query = command.lower().split("find on page")[1].strip()
            if query in browser.page_source:
                return f"Found '{query}' on the current page."
            return f"Could not find '{query}' on the current page."
        else:
            return "Web agent command not understood. Try 'browse to [url]', 'summarize page', or 'find on page [query]'."
    except Exception as e:
        return f"Error with web agent: {e}"

