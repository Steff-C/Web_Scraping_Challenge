from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests as req
import time
import os
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# set up splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

mars_info = {}

# NASA MARS NEWS 
def scrape_mars_news():
    # Initialize browser
    browser = init_browser()

    # NASA Mars News
    # Visit the NASA Mars News Site
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)

    # HTML object and parse with Beautiful Soup
    html = browser.html
    soup = bs(html, 'html.parser')

    # Extract latest news title and paragraph text
    article = soup.find("div", class_="list_text")
    news_title = article.find("div", class_="content_title").text
    news_paragraph = article.find("div", class_="article_teaser_body").text

    # Enter results into Dictionary
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_paragraph
    
    browser.quit()
    
    return mars_info

    

# JPL Mars Space Images - Featured Image--
def scrape_mars_image():
    #Initialize browser
    browser = init_browser()

    img_url = "https://spaceimages-mars.com/image/featured/mars1.jpg"
    browser.visit(img_url)

    # HTML object and parse with Beautiful Soup
    html_image = browser.html
    soup = bs(html_image, "html.parser")

    # Get background image url using style tag
    image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Connect image url to the website's main url
    main_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    featured_image_url = main_url + image_url

    # Display link to featured image url
    featured_image_url

    # Enter results into Dictionary
    mars_info['image_url'] = image_url

    browser.quit()

    return mars_info

# Mars Facts 
def mars_scrape_facts():
   
    browser = init_browser()

 
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)

    #
    tables = pd.read_html(facts_url)
    df = tables[1]

    df.columns = ['Fact', 'Description']
    html_table = df.to_html(table_id="tablepress-p-mars", justify="left", index=False)
    df.to_dict(orient='records')
    df

    # Enter results into dictionary
    mars_info['mars_table'] = html_table

    browser.quit()

    return mars_info

# Mars Hemispheres 
def scrape_mars_hemisphere():
  
    browser = init_browser()

   
    hemisphere_url = '"https://marshemispheres.com/"
    browser.visit(hemisphere_url)

  
    html_hemisphere = browser.html
    soup = bs(html_hemisphere, "html.parser")

    
    items = soup.find_all('div', class_='item')

 
    hemisphere_image_urls = []

    hemisphere_main_url = "https://marshemispheres.com/"

  
    for i in items:
        title = i.find('h3').text
        item_img_url = i.find('a', class_='itemLink product-item')['href']
        browser.visit(hemisphere_main_url + item_img_url)
  
        item_img_url = browser.html
        soup = bs(item_img_url, "html.parser")
        
        img_url = hemisphere_main_url + soup.find('img', class_='wide-image')['src']

        hemisphere_image_urls.append({  "title" : title, "img_url" : img_url  })

        hemisphere_image_urls

    mars_info['hemisphere_image_urls'] = hemisphere_image_urls

    browser.quit()

    return mars_info