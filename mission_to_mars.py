
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver

#initiate browser
def initialize_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=True)

#scraping Mars News for latest headline title and body
def scrape():
    browser = initialize_browser()

    mars_data = {}

    mars_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(mars_url)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_data['recent_title'] = soup.find("div",class_="content_title").text
    mars_data['recent_body'] = soup.find("div", class_="article_teaser_body").text

#scrape for JPL Mars Space Images - Featured Image

    pic_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    nasa_link = 'https://www.jpl.nasa.gov'

    browser.visit(pic_url)
    xpath_mars_link = '//*[@id="full_image"]'
    xpath_mars_pic = '//*[@id="fancybox-lock"]/div/div[1]/img'

    #store path of link and then click
    mars_results = browser.find_by_xpath(xpath_mars_link)
    mars_link = mars_results[0]
    mars_link.click()

    #read page with BeautifulSoup to obtain link
    #html = browser.html
    #soup = bs(html, 'html.parser')

    #retrieve partial link
    #pic_link = soup.find("img", class_="fancybox-image")["src"]
    pic_link = browser.find_by_xpath(xpath_mars_pic)

    #create link
    mars_pic_link = nasa_link + pic_link.text
    mars_data["mars_pic_link"] = mars_pic_link

#scrape for Mars Weather information

    mars_weather_link = 'https://twitter.com/marswxreport?lang=en'

    browser.visit(mars_weather_link)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text


    #xpath_mars_weather = '//*[@id="stream-item-tweet-1055479145478737921"]/div[1]/div[2]/div[2]/p'


    #weather_results = browser.find_by_xpath(xpath_mars_weather)
    #weather_body = weather_results[0]
    #mars_weather_body = weather_body.text
    mars_data["mars_weather"] = mars_weather


#use Pandas to scrape Mars facts

    mars_facts_url = 'https://space-facts.com/mars/'
    mars_facts_table = pd.read_html(mars_facts_url)

    #convert table into a dataframe
    mars_facts_df = mars_facts_table[0]

    #convert dataframe into html
    mars_facts_df.to_html('mars_facts.html')


#scrape for titles and pictures of Mars Hemispheres

    mars_high_res_link = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_link = 'https://astrogeology.usgs.gov/'
    hemisphere_image_urls = []

    browser.visit(mars_high_res_link)
    soup = bs(browser.html, "html.parser")
    hemispheres = soup.find_all("div", class_="item")

    for hemisphere in hemispheres:
        
        title = hemisphere.find("a", class_="itemLink").find("img")["alt"]
        title_edit = title[:-19]
        hemisphere_image_urls.append({
            "title": title_edit
        })
        
        hemi_link = hemisphere.find("a", class_="itemLink")
        image_link = hemi_link["href"]
        full_link = f'{base_link}{image_link}'
        hemisphere_image_urls.append({
            "img_url": full_link
        })
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls

    return mars_data