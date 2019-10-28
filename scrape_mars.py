from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time
import pymongo


# In[2]:

def scrape():

    full_scrape = {}

    # Splinter connection to chromedriver
    executable_path = {'executable_path' : '/home/leon/Documents/Personal/Bootcamp/Week12 - Web Scrapping/Mission-to-Mars/chromedriver'}
    browser = Browser("chrome", **executable_path, headless=False)


    # # NASA Mars News
    #
    # Section to scrap the NASA Mars webpage.

    # In[3]:


    url_mars = "https://mars.nasa.gov"
    mars_news = "/news"
    browser.visit(url_mars + mars_news)


    # In[4]:


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    li_slide = soup.find_all('li', class_="slide")

    date = []
    title = []
    url_news = []
    url_img = []
    description = []

    #Important!!!
    for item in li_slide:
        title.append(item.find("div", class_="content_title").text)
        url_news.append(url_mars + item.find("div", class_="content_title").a['href'])
        url_img.append(url_mars + item.find("div", class_="list_image").img['src'])
        date.append(item.find("div", class_="list_date").text)
        description.append(item.find("div", class_="article_teaser_body").text)

    full_scrape['NASA Mars News'] = {}
    full_scrape['NASA Mars News']['title'] = title
    full_scrape['NASA Mars News']['url_news'] = url_news
    full_scrape['NASA Mars News']['url_img'] = url_img
    full_scrape['NASA Mars News']['date'] = date
    full_scrape['NASA Mars News']['description'] = description

    # In[5]:


    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)


    # In[6]:


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    day_descr = soup.find("h1", class_="media_feature_title").get_text(strip=True)

    try:
        browser.click_link_by_partial_text('FULL IMAGE')
    except:
        print('Already on page')

    time.sleep(3)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    day_img = soup.find('img', class_="fancybox-image")['src']

    day_img_url = 'https://www.jpl.nasa.gov/' + day_img

    full_scrape['JPL Mars Space Images'] = {}
    full_scrape['JPL Mars Space Images']['img_description'] = day_descr
    full_scrape['JPL Mars Space Images']['img_url'] = day_img_url

    # # Mars Weather

    # In[7]:


    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)


    # In[8]:


    html = browser.html

    soup = BeautifulSoup(html, 'html.parser')

    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
    mars_weather

    full_scrape['Mars Weather'] = {}
    full_scrape['Mars Weather']['weather'] = mars_weather

    # # Mars Facts

    # In[9]:


    url_facts = 'https://space-facts.com/mars/'

    fact = pd.read_html(url_facts)

    # fact[0].to_html("templates/table1.html")
    mars_earth = fact[0]
    mars_earth = mars_earth.set_index('Mars - Earth Comparison')
    mars_earth.to_html("templates/mars_earth.html")

    # In[10]:


    # fact[1].to_html("templates/table2.html")
    mars_facts = fact[1]
    mars_facts = mars_facts.set_index(0)
    mars_facts.to_html("templates/mars_facts.html")


    # # Mars Hemispheres

    # In[11]:


    url_hemispheres = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemispheres)


    # In[12]:


    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    a = soup.find_all("div", class_='description')

    for i in a:
        d = {}
        d['title'] = i.h3.text

    #     link.append(i.a['href'])
    #     title.append(i.h3.text)

        try:
            browser.click_link_by_partial_text(i.h3.text)
        except:
            print('Already on page')

        time.sleep(3)

        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        d['img_url'] = 'https://astrogeology.usgs.gov' + soup.find('img', class_='wide-image')['src']
    #     img.append(soup.find('img', class_='wide-image')['src'])

        hemisphere_image_urls.append(d)
        browser.back()

    browser.quit()
    hemisphere_image_urls

    full_scrape['Mars Hemispheres'] = hemisphere_image_urls

    # print(full_scrape)
    return full_scrape

# if __name__ == '__main__':
#     print(scrape())