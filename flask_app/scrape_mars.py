#do the imports
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

#set-up the browser
#################################################
# Mac
#################################################
# Set Executable Path & Initialize Chrome Browser
#executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
#browser = Browser("chrome", **executable_path, headless=False)

#################################################
# Windows
#################################################
# Set Executable Path & Initialize Chrome Browser
#executable_path = {"executable_path": "chromedriver.exe"}
#browser = Browser("chrome", headless=True, **executable_path)

#make a function for scraping
#Scrape the news
#Goto to the NASA url
def mars_news(browser):
    nasa_url = 'https://mars.nasa.gov/news/'
    try:
        browser.visit(nasa_url)
        # get the html
        nasa_html = browser.html

        # parse html in bs
        soup = bs(nasa_html, 'html.parser')

        # grab the first instance of news
        news_title = soup.find('div', class_='content_title').find('a').text
        news_p = soup.find('div', class_='article_teaser_body').text
    except:
        return None
    return news_title, news_p

#Scrape the JPL image
#goto JPL
def jpl_img(browser):
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    try:
        browser.visit(jpl_url)
        #get the html
        jpl_html = browser.html

        # parse html
        soup = bs(jpl_html, 'html.parser')

        # Retrieve background-image url from style tag. The image url is a relative path with some panethses and quotes.
        featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

        # jpl url
        main_url = 'https://www.jpl.nasa.gov'

        # put the whole url together
        featured_image_url = main_url + featured_image_url
    except:
        return None
    return featured_image_url

def mars_weather(browser):
    #Mars weather on twitter. This might be the first time I've intentially visited twitter.
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    try:
        browser.visit(weather_url)
        weather_html=browser.html

        soup = bs(weather_html, 'html.parser')

        #get the tweets, pretty easy they must want this to happen
        tweets = soup.find_all('div',class_='js-tweet-text-container')

        #find the first entry with the weather data. a/o the running this the last weather update was 9/15
        #they seem to start w/ Insight sol
        for tweet in tweets: 
            weather_tweet = tweet.find('p').text
            if 'InSight sol' in weather_tweet:
                m_weather=weather_tweet
                break
            else: 
                pass
    except:
        return None
    return m_weather

def mars_facts(browser):
    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'
    try:
        mars_facts_df = pd.read_html(facts_url)[0]
        mars_facts_df = mars_facts_df.rename(index=str, columns={0: "Description", 1: "Value"})
        mars_facts_html = mars_facts_df.to_html(index=False,index_names='False')
    except:
        return None
    return(mars_facts_html)
    

def hemi_imgs(browser):
    #Hemisphere pics
    hemi_url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    try:
        browser.visit(hemi_url)
        #start a dict list for wrangling the images
        hemi_urls = []

        # return lisr of all the image links
        links = browser.find_by_css("a.product-item h3")
        #loop through the image links
        for item in range(len(links)):
            hemis = {}
            #this find by css thing is easier on this page
            browser.find_by_css("a.product-item h3")[item].click()
            #read the docs for the browser class, maybe go back to the previous searches to clean them up too
            #this returns 
            sample_element = browser.find_link_by_text("Sample").first
            #get the title, i.e. the hemisphere
            hemis["title"] = browser.find_by_css("h2.title").text
            
            #get the image url
            hemis["img_url"] = sample_element["href"]
            #add the image urls to a dict
            hemi_urls.append(hemis)
            #click back to go to the next image
            browser.back()
    except:
        return None
    return(hemi_urls)



# main function call to collect data

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_p = mars_news(browser)
    img_url = jpl_img(browser)
    m_weather = mars_weather(browser)
    facts = mars_facts(browser)
    hemi_img_urls = hemi_imgs(browser)


    data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": img_url,
        "weather": m_weather,
        "facts": facts,
        "hemispheres": hemi_img_urls,

    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape())
