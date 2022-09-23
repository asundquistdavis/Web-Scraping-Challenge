# Web-Scraping-Challenge
## Overview
This challenge uses Python libraries to scrape news, facts and images of Mars and on a dynamic website. The purpose of the challenge is to practice web scraping with BeautifulSoup, Requests, Pandas and Splinter and dynamic hosting with Flask. The data is stored in a non-relational MongDB database. The websites used to get the data can be found here: [Martian News](https://redplanetscience.com/), [Mars Featured Image](https://spaceimages-mars.com/), [Mars Facts](https://galaxyfacts-mars.com/) and [Mars Hemispheres](https://marshemispheres.com/)
## Contents
- app.py: runs dynamic website with flask app by using scraping functions to gather data
- mission_to_mars.ipynb: used to develop scraping strategy used in scrape_mars.py
- scrape_mars.py: defines the scraping functions used in app.py
## Methodology
Getting necessary data for the website involves scraping data from several websites. The appropriate scraping strategy for each site was found using the jupyter notebook and the chrome inspector. The mars news data and mars feature image are dynamic meaning that visiting those sites could produce different results each time. The pictures of the mars hemispheres and the facts do not change in time and repeated scraping produces the same data. Because of this, the app only scrapes these sites once, on startup, and saves the data so it can be reused. The dynamic data, however, is scraped everytime the user requests new data. A more sophisticated implementation of the app could simply scrape and save all necessary data once per day (overnight) and simply load the saved data upon each request. This would be much faster at the trade off of storing some more data.

MongoDB is used to store the data. Ultimately, a dictionary is passed to the html page to load all of the data. Since MongoDB can easily store collections data of dictionary/JSON like objects, it is favorable to something like SQL, which would return rows of items (elements) with one list of keys (columns). Another reason for using MongoDB is that the database really only needs to store one instance of the data and just update it every time the scrape function is called. MongoDB allows for easy usperting of data. The same could be implemented with SQL, however, it would at the least, not have the same readability and probably would not have the same performance.
##W Website Preview
![Website image 1](mars_scrape_1.png)
![Website image 2](mars_scrape_2.png)