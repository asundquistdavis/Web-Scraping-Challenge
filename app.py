# imports
from flask import Flask, redirect, render_template
from pymongo import MongoClient
from scrape_mars import scrape_mars

# initialize the app
app = Flask(__name__)

# set up MongoDB and call the mars data document
client = MongoClient('mongodb://localhost:27017')
mars_doc = client.mars_db.mars_data

# scape all data (startup=True) and repeat until successfull - this ensures that data is present on load 
no_data = True
while no_data == True:
    mars_data = scrape_mars(startup=True)
    if mars_data['success'] == True:
        no_data = False

# upsert the scraped data to the website
mars_doc.update_one({}, {'$set': mars_data}, upsert=True)

# define index route - displays all data + button to scrape new data
@app.route('/')
def index():
    mars_doc = client.mars_db.mars_data.find_one()
    return render_template('index.html', mars_data=mars_doc)

# scrape route - target of button on index.html - calls the functions to scrape just the dynamic data (startup=False)
@app.route('/scrape')
def scrape():
    mars_doc = client.mars_db.mars_data
    mars_data = scrape_mars(startup=False)
    mars_doc.update_one({}, {'$set': mars_data}, upsert=True)
    return redirect('/', code=302)

# run the app when app.py is run
if __name__ == '__main__':
    app.run(debug=True)