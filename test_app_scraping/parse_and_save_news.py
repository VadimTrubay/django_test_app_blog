import os
import requests
import psycopg2
import logging
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_URL = os.getenv('API_URL')

DB_NAME = os.getenv('DATABASE_NAME')
DB_USER = os.getenv('DATABASE_USER')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD')
DB_HOST = os.getenv('DATABASE_HOST')
DB_PORT = os.getenv('DATABASE_PORT')

# URL = os.getenv('URL')
URL = 'https://news.ycombinator.com/'

LOG_FILE = 'news_parser.log'
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def create_table():
    """
    The create_table function creates a table in the database if it does not already exist.
    The function takes no arguments and returns nothing.
    
    :return: Nothing
    :doc-author: Trelent
    """
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news_articles (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')
    conn.commit()
    cursor.close()
    conn.close()


def parse_news():
    """
    The parse_news function takes no arguments and returns a list of tuples.
    Each tuple contains the title of an article and its URL.
    
    :return: A list of tuples
    :doc-author: Trelent
    """
    try:
        response = requests.get(URL)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('span.titleline')
        news_list = []
        for article in articles:
            title_element = article.find('a').text
            url = article.find('a')['href']
            news_list.append((title_element, url))
        return news_list

    except requests.RequestException as e:
        logging.error(f'Error fetching data from {URL}: {str(e)}')
        return None


def save_to_database(news_list):
    """
    The save_to_database function takes a list of tuples as an argument.
    Each tuple contains the title and url of a news article.
    The function then connects to the database, creates a cursor, and inserts each tuple into the database.
    
    :param news_list: Pass the list of news articles to be saved to the database
    :return: None
    :doc-author: Trelent
    """
    if news_list is None:
        return
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cursor = conn.cursor()

        for title, url in news_list:
            cursor.execute('INSERT INTO news_articles (title, url) VALUES (%s, %s)', (title, url))

        conn.commit()
        logging.info(f'Successfully saved {len(news_list)} news articles to the database.')

    except psycopg2.Error as e:
        logging.error(f'Error inserting data into the database: {str(e)}')

    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    logging.info('Script execution started.')
    create_table()
    news_list = parse_news()
    if news_list:
        save_to_database(news_list)
    logging.info('Script execution completed.')
