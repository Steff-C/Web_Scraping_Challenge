from bs4 import BeautifulSoup as bs
import requests as req
from splinter import Browser
#from selenium import webdriver
import time
import os
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "driver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

# Create Mission to Mars dictionary 
mars_info = {}

# NASA MARS NEWS ---------------------------------------------------
def scrape_mars_news():
    # Initialize browser
    browser = init_browser()

    # NASA Mars News------------------------------------------------------------
    # Visit the NASA Mars News Site
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # HTML object and parse with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Extract latest news title and paragraph text
    article = soup.find("div", class_="list_text")
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_="article_teaser_body").text

    # Enter results into Dictionary
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p
    
    browser.quit()
    
    return mars_info

    

# JPL Mars Space Images - Featured Image----------------------------------------
def scrape_mars_image():
    #Initialize browser
    browser = init_browser()

    img_url = "https://spaceimages-mars.com/image/featured/mars1.jpg"
    browser.visit(img_url)

    html_image = browser.html
    soup = bs(html_image, "html.parser")

    image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    main_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    featured_image_url = main_url + image_url

    featured_image_url

    mars_info['image_url'] = image_url

    browser.quit()

    return mars_info


# Mars Facts ---------------------------
def mars_scrape_facts():
    #Initialize Browser
    browser = init_browser()

    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)

    tables = pd.read_html(facts_url)
    df = tables[1]

    df.columns = ['Fact', 'Description']
    html_table = df.to_html(table_id="tablepress-p-mars", justify="left", index=False)
    df.to_dict(orient='records')
    df

    mars_info['mars_table'] = html_table

    browser.quit()

    return mars_info

# Mars Hemispheres ---------------
def scrape_mars_hemisphere():
    # Initialize browser
    browser = init_browser()

    # Visit the USGS Astrogeology site to obtain high resolution images for each of Mar's hemispheres
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)

    # HTML object and parse with Beautiful Soup
    html_hemisphere = browser.html
    soup = bs(html_hemisphere, "html.parser")

    # Find all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create a list for hemisphere urls
    hemisphere_image_urls = []

    hemisphere_main_url = "https://marshemispheres.com/"

    # Loop through all the items
    for i in items:
        # Add title
        title = i.find('h3').text
        # Add image link
        item_img_url = i.find('a', class_='itemLink product-item')['href']
        # Go to image link
        browser.visit(hemisphere_main_url + item_img_url)

        # HTML object of website and parse with Beautiful Soup
        item_img_url = browser.html
        soup = bs(item_img_url, "html.parser")

        # Find the link and present information into a list of dictionaries
        img_url = hemisphere_main_url + soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({  "title" : title, "img_url" : img_url  })

        # Display the hemisphere dictionary list
        hemisphere_image_urls

    mars_info['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return mars_info

