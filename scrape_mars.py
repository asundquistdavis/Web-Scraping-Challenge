# imports and configs
from datetime import datetime as dt
from bs4 import BeautifulSoup as BS
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pandas as pd
executable_path = {'executable_path': ChromeDriverManager().install()}

def scrape_mars(startup=False):

    # initiallize a dictionary to store document
    mars_data = {}
    
    # call the scrape functions and store data in dictionary
    try:
        mars_data['news'] = scrape_news()
        mars_data['image'] = scrape_img()
        
        # if it is the start up run, scrape the facts table and hemispheres images
        # these are static, so they are only called once at start up and then skipped each other time
        if startup == True:
            # mars_data['facts'] = dt.now() # this line is for testing startup functionality
            mars_data['facts'] = scrape_facts()
            mars_data['hemispheres'] = scrape_hemispheres()

        # get the current timestamp and save in dictionary
        mars_data['time'] = dt.now()
    
        # scrape was successful
        mars_data['success'] = True
    
    except:

        # scrape was NOT successful
        mars_data['success'] = False

    # return the dictionary
    return mars_data

# *** define four functions, each one scrapes a diffent peice of data ***

def scrape_news():

    # *** Strategy ***
    # have splinter visit redplanetscience and call html
    # have bs4 read html and find the 'section' element with class="image_and_dexription_container"
    # then get the first 'div' under that - this is the target news story
    # save the element with class="content_title" as title
    # save the element with class="article_teaser_body" as body

    url = 'https://redplanetscience.com/'
    with Browser('chrome', **executable_path, headless=True) as browser:
        browser.visit(url)
        html = browser.html
        div = BS(html, 'lxml').find('section', class_="image_and_description_container").find_all('div', class_='col-md-12')[0]
        title = div.find('div', class_='content_title').text
        date = div.find('div', class_='list_date').text
        body = div.find('div', class_='article_teaser_body').text
    return {'title': title, 'date': date, 'body': body}

def scrape_img():

    # *** Strategy ***
    # have splinter visit spaceimages-mars.com and call html
    # have bs4 read html and find the 'div' element with class="header" - this is the main image
    # get the 'src' attribute from the 'img' element with class="headerimage" and save as img
    # concatanate the website url and the img path to get the img_url

    url = 'https://spaceimages-mars.com/'
    with Browser('chrome', **executable_path, headless=True) as browser:
        browser.visit(url)
        html = browser.html
        header = BS(html,'html.parser').find('div', class_='header')
        img = header.find('img', class_='headerimage')['src']
        img_url = f'{url}{img}'
    return img_url

def scrape_facts():

    # *** Strategy ***
    # get html from galaxyfacts-mars.com using requests
    # have pandas scrape table(s) from html with text 'Mars - Earth Comparison'
    # clean up column names
    # have pandas generate html table for the dataframe and include bootstrap classes - 'table table-responsive'

    url = 'https://galaxyfacts-mars.com/'
    html = requests.get(url).content
    df = pd.read_html(html, match='Mars - Earth Comparison', header=0)[0]
    df[''] = df['Mars - Earth Comparison']
    table = df.loc[:,['','Mars','Earth']].to_html(index=False, border=1, classes="table table-responsive table-striped table-bordered", justify="inherit")
    return table

def scrape_hemispheres():
    
    # *** Strategy ***
    # have splinter visit marshemispheres.com, four times
    # have splinter get all the links with partial text 'hemisphere'
    # and click on a different one each time
    # on new page, click the link that says 'Open' and call the html
    # have bs4 read html and find the 'h2' element with class="title"
    # then get the 'src' attribute of the 'img' element with class='wide-image' and save it as img
    # concatenate the page root page url with the img path and save as the img_url

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