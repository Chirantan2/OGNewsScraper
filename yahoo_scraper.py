import requests
from bs4 import BeautifulSoup
from scraper import Scraper
import pandas as pd


class Yahoo(Scraper):
    def __init__(self):
        pass

    def scrape(self, company_name: str, keyword: str, page_count: int) -> pd.DataFrame:
        BASE_URL = 'https://news.search.yahoo.com/search?q='

        response = requests.get(BASE_URL+company_name+keyword)
        soup = BeautifulSoup(response.text, 'lxml')
        
        NUMBER_OF_PAGES = page_count

        titles, links, media, time, searchEngine, searchString = [],[],[],[],[],[]

        for i in range(NUMBER_OF_PAGES):
            nws = {}
            all_news = soup.find_all('ul', class_='compArticleList')
            for news in all_news:
                titles.append(news.find('h4').text)
                links.append(news.find('a')['href'])
                media.append(news.find('span', class_='s-source mr-5 cite-co').text)
                time.append(news.find('span', class_='fc-2nd s-time mr-8').text.replace('.', ''))
                searchString.append(company_name+'and'+keyword)
                searchEngine.append('Yahoo')
            if soup.find('a', class_='next') is None:
                with open('index.html', 'w') as f:
                    f.write(soup.prettify())
                continue
            nextResponse = requests.get(soup.find('a', class_='next')['href'])
            soup = BeautifulSoup(nextResponse.content, 'lxml')

        data = {"Title": titles, "Link": links, "MediaAgency":media, "TimeStamp":time, 'SearchEngine': searchEngine, 'SearchString':searchString}
        return pd.DataFrame(data)
