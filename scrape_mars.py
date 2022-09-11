from datetime import datetime as dt
from bs4 import BeautifulSoup as BS
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape_mars():
    mars_data = {}
    mars_data['news'] = scrape_news()
    mars_data['image'] = scrape_img()
    mars_data['facts'] = scrape_facts()
    mars_data['hemispheres'] = scrape_hemispheres()
    mars_data['time'] = dt.now()
    return mars_data

def scrape_news():
    url = 'https://redplanetscience.com/'
    with Browser('chrome', **executable_path, headless=True) as browser:
        browser.visit(url)
        html = browser.html
        div = BS(html, 'lxml').find('section', class_="image_and_description_container").find('div', class_='col-md-12')
        title = div.find('div',class_='content_title').text
        body = div.find('div', class_='article_teaser_body').text
    return {'title': title, 'body': body}

def scrape_img():
    url = 'https://spaceimages-mars.com/'
    with Browser('chrome', **executable_path, headless=True) as browser:
        browser.visit(url)
        html = browser.html
        header = BS(html,'html.parser').find('div', class_='header')
        img = header.find('img', class_='headerimage')['src']
        img_url = f'{url}{img}'
    return img_url

def scrape_facts():
    url = 'https://galaxyfacts-mars.com/'
    html = requests.get(url).text
    df = pd.read_html(html, match='Mars - Earth Comparison', header=0)[0]
    df[''] = df['Mars - Earth Comparison']
    table = df.loc[:,['','Mars','Earth']].to_html(index=False, border=1, classes="table table-responsive table-striped table-bordered", justify="inherit")
    return table

def scrape_hemispheres():
    url = 'https://marshemispheres.com/'
    with Browser('chrome', **executable_path, headless=True) as browser:
        list = []
        for i in range(4):
            browser.visit(url)
            links = browser.links.find_by_partial_text('Hemisphere')
            links[i].click()
            browser.links.find_by_text('Open').click()
            html = browser.html
            soup = BS(html)
            title = soup.find('h2', class_='title').text
            img = soup.find('img', class_='wide-image')['src']
            img_url = f'{url}{img}'
            dict = {'title': title, 'img_url': img_url}
            list.append(dict)
    return list