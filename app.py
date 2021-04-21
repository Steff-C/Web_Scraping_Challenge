from flask import Flask, render_template, request
from flask_pymongo import PyMongo  
import scrape_mars
import os
import sys
import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Create route 
@app.route("/")
def home():
    
    mars_info = mongo.db.mars_info.find_one()

   
    return render_template("index.html", mars_info=mars_info)


@app.route("/scrape")
def scrape():
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.mars_scrape_facts()
    mars_data = scrape_mars.scrape_mars_hemisphere()
    mars_info.update({}, mars_data, upsert=True)

    return request("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
