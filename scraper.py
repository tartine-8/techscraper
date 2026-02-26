import argparse
import asyncio
import httpx
import os
import random

from dotenv import load_dotenv
from pymongo import UpdateOne
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from selectolax.parser import HTMLParser
from tqdm.asyncio import tqdm
from datetime import datetime
import dateutil.parser

sem = asyncio.Semaphore(50)

# scraping process
async def scrape_page(client, page_id):
    async with sem:
        await asyncio.sleep(random.uniform(0.1, 0.5))
        url = f'https://techcrunch.com/latest/page/{page_id}/'
        try:
            # reaching for a specific page
            resp = await client.get(url, timeout=20.0)
            if resp.status_code != 200:
                return []
            tree = HTMLParser(resp.text)
            articles = []
            
            # geting all articles cards from the web page
            for card in tree.css('ul.wp-block-post-template div.loop-card'):
                # parsing the data of one card
                title_node = card.css_first('h3.loop-card__title a')
                if not title_node: continue
                
                link = title_node.attributes.get('href')
                if '/video/' in link: continue
                
                cat_node = card.css_first('a.loop-card__cat, span.loop-card__cat')
                cat = cat_node.text().strip() if cat_node else 'none'
                
                authors = [a.text().strip() for a in card.css('a.loop-card__author')]
                
                time_node = card.css_first('time.loop-card__time')
                if not time_node: continue
                timestamp = dateutil.parser.isoparse(time_node.attributes.get('datetime'))
                
                # creating a result data object from the parsed data
                articles.append({
                    'title': title_node.text().strip(),
                    'category': cat,
                    'authors': authors if authors else ['none'],
                    'link': link,
                    'timestamp': timestamp
                })
            return articles
        except Exception as e:
            return []
       
# uploading the scraped data to update mongodb 
def upload_to_mongodb(articles, chunk_size=5000):
    # connecting to the mongodb cluster
    load_dotenv()
    uri = os.getenv('MONGO_URI')
    client = MongoClient(uri, server_api=ServerApi('1'))
    db = client['tech_scraper_db']
    articles_col = db['articles']
    
    # set of operations to do
    operations = [
        UpdateOne({'link': a['link']}, {'$set': a}, upsert=True)
        for a in articles
    ]
    
    # uploading by chunks so it remains manageable even when the user scrape a lot of data at once
    for i in range(0, len(operations), chunk_size):
        batch = operations[i:i+chunk_size]
        articles_col.bulk_write(batch, ordered=False)

# main method to parallelize the scraping process
async def main(total_pages=10, start_page=1, batch_size=500):
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=20)
    async with httpx.AsyncClient(limits=limits, follow_redirects=True) as client:
        for i in range(start_page, total_pages + start_page, batch_size):
            start = i
            end = min(i + batch_size, start_page + total_pages + 1)
            
            tasks = [scrape_page(client, p) for p in range(start, end)]
            results = await tqdm.gather(*tasks, desc=f'scraping pages {start}-{end-1}')
            flatten = [item for sublist in results for item in sublist]
            if flatten:
                upload_to_mongodb(flatten)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='a simple scraper')
    parser.add_argument('--pages', type=int, default=10, help='number of pages to scrape')
    parser.add_argument('--start', type=int, default=1, help='the starting page to scrape from')
    args = parser.parse_args()
    asyncio.run(main(total_pages=args.pages, start_page=args.start))