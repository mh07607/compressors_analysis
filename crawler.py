import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

def get_random_wikipedia_article(url):
    # Send a GET request to the random Wikipedia article URL
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Extract the title and URL of the random article
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1', id='firstHeading').text
        article_url = response.url
        
        return title, article_url
    else:
        # If the request was not successful, return None
        return None, None

def get_random_wikipedia_articles(num_articles, urls):
    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "random",
        "rnnamespace": 0,  # Limit to main namespace (articles)
        "rnlimit": num_articles  # Number of random articles to retrieve
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "error" in data:
        raise Exception(f"Error fetching random articles: {data['error']['info']}")

    # random_articles = []    
    for page in data["query"]["random"]:
        title = page["title"]
        url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
#         random_articles.append(title)
        urls.append(url)


def crawl_wikipedia_article(article_url):
    # Send a GET request to the Wikipedia article URL
    response = requests.get(article_url)    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the main content of the page
        main_content = soup.find(id='mw-content-text')
        text_data = main_content.get_text()
        return text_data
    else:
        # If the request was not successful, return None
        return None

# Number of random Wikipedia articles to crawl
sizes = [7500, 10000, 15000, 20000]
# Number of parallel requests

for num_articles in sizes:    
    content = ""
    urls = []
    # wikipedia has limitied number of random urls fetching to 500
    for _ in range(num_articles//500):
        get_random_wikipedia_articles(500, urls)                

    print(len(urls))

    with ThreadPoolExecutor(max_workers=10) as executor:
        # Fetch the content of multiple articles concurrently
        results = list(tqdm(executor.map(crawl_wikipedia_article, urls), 
                            total=len(urls), 
                            desc=f"Crawling {num_articles} articles"))

    content = ""
    for result in results:            
        if result is not None:
            content += result              
    
    # Write content to file
    with open(f"data/{num_articles}.txt", "a", encoding="utf-8") as file:
        file.write(content)        

