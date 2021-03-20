import pandas as pd 
import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import time

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.quote_db
collection = db.quote

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

url = 'http://quotes.toscrape.com/'
browser.visit(url)

#creating the html 
html = browser.html

# create the soup 
soup = BeautifulSoup(html, 'html.parser')

# creating a list of dictionaries 
quote_text = soup.find_all('div', class_='quote')
quote_list = []

i = 0
while i < len(quote_text):

    for info in range(len(quote_text)):
        # creating the dictionary
        quote_dictionary = {}
        
        #quote
        quote = quote_text[info]
        quote = quote.find('span', class_='text').text
        quote_dictionary['quote'] = quote
        
        #tags
        tags = quote_text[info]
        tags = tags.find('meta', class_='keywords')['content']
        quote_dictionary['tags'] = tags
    
        #author
        author = quote_text[info]
        
        link = author.a['href']
        author = author.find('small', class_='author').text
        quote_dictionary['author'] = author
    
        # tags in list form
        tag_list = tags.split(',')
        quote_dictionary['tag_list'] = tag_list
        
        # creating new url for about
        url=f"http://quotes.toscrape.com/{link}/"
        browser.visit(url)

        
        #html object
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        
        #author details
        birth_date = soup.find('span', class_='author-born-date').text
        location = soup.find('span', class_="author-born-location").text
        quote_dictionary['born'] = birth_date + ' ' + location
    
        description = soup.find('div', class_='author-description').text.replace('\n','')
        quote_dictionary['author_description'] = description
    
        quote_list.append(quote_dictionary)
    
        #click back
        browser.back()
 
    i = i + 1
    
    try:
        
        browser.links.find_by_partial_text('Next').click()
        html = browser.html
        soup = BeautifulSoup(html,'html.parser')
        quote_text = soup.find_all('div', class_='quote')
        time.sleep(.5)
        
    except:
        print("Scraping Complete")       

browser.quit()

collection.delete_many({})
collection.insert_many(quote_list)




