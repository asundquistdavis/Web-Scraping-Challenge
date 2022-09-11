from flask import Flask, redirect, render_template
from pymongo import MongoClient
from scrape_mars import scrape_mars

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')

mars_doc = client.mars_db.mars_data

no_data = True
while no_data == True:
    mars_data = scrape_mars(startup=True)
    if mars_data['success'] == True:
        no_data = False

mars_doc.update_one({}, {'$set': mars_data}, upsert=True)

@app.route('/')
def index():
    mars_doc = client.mars_db.mars_data.find_one()
    return render_template('index.html', mars_data=mars_doc)

@app.route('/scrape')
def scrape():
    mars_doc = client.mars_db.mars_data
    mars_data = scrape_mars(startup=False)
    mars_doc.update_one({}, {'$set': mars_data}, upsert=True)
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)