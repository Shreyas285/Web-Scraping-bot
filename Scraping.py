import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os

# To get the DataFrame of top 30 Github Project Topics.
def scrape_project_topics():
    
    # Get the tittle of the topic
    def get_title(tags):
        title = []
        for tag in tags:
            title.append(tag.text) 
        return title 
    # Get the description of the topic
    def get_desc(tags):
        description = []
        for tag in tags:
            description.append(tag.text.strip()) 
        return description
    # Get the URl of the topic
    def get_link(tags):
        links = []
        base = 'https://github.com'
        for tag in tags:
            links.append(base + tag['href'] )
        return links
    # To create the DataFrame of top 30 project topics.
    def create_df(title,description,links):
        topic_dict = {'Title':title,'Description':description,'Link':links}
        df = pd.DataFrame(topic_dict)
        return df
    
    # Url for the github repository
    url = 'https://github.com/topics'
    
    # To parse a website int unicode characters using BeautifulSoup.
    response = requests.get(url)
    page_contents = response.text
    soup = BeautifulSoup(page_contents, 'html.parser')
    
    # To get title name.
    tit_sel = "f3 lh-condensed mb-0 mt-1 Link--primary"
    tit_tags = soup.find_all('p',{'class':tit_sel})
    title = get_title(tit_tags)
    
    # To get description.
    des_sel = "f5 color-text-secondary mb-0 mt-1"
    des_tags = soup.find_all('p',{'class':des_sel})
    description = get_desc(des_tags)
    
    # To get topic url.
    link_sel = "d-flex no-underline"
    link_tags = soup.find_all('a',{'class': link_sel})
    links = get_link(link_tags)
    
    # Creating data fram using dictionary.
    df = create_df(title,description,links)
    return df   
