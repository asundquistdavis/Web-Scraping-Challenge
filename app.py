from flask import Flask, redirect, render_template
from pymongo import MongoClient
from scrape_mars import scrape_mars

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017')

@app.route('/')
def index():
    mars_data = client.mars_db.mars_data.find_one()
    if mars_data == None:
        return render_template('index.html')
    else:
        return render_template('index.html', mars_data=mars_data)

@app.route('/scrape')
def scrape():
    mars_data = client.mars_db.mars_data.find_one()
    mars_data.update_one({}, {'$set': scrape_mars(starutup=False)}, upsert=True)
    return redirect('/', code=302)

if __name__ == '__main__':
    app.run(debug=True)