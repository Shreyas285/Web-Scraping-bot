import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os

# To get the DataFrame of top 25 Github Project Topics.
def get_webdata(url):
    #Making request to a github web page using url.
    #The serevr returns response object with webpage contents
    response = requests.get(url)
    page_contents = response.text
    #Parsing webpage contents into complex tree of Python objects.
    soup = BeautifulSoup(page_contents, 'html.parser')
    return soup  


def get_title():
    # To get title name of project topic.
    url = 'https://github.com/topics'
    soup = get_webdata(url)
    tit_sel = "f3 lh-condensed mb-0 mt-1 Link--primary"
    tit_tags = soup.find_all('p',{'class':tit_sel})
    title = []
    for tag in tit_tags:
        title.append(tag.text) 
    return title

def get_description():
    # To get description of project topic.
    url = 'https://github.com/topics'
    soup = get_webdata(url)
    des_sel = "f5 color-text-secondary mb-0 mt-1"
    des_tags = soup.find_all('p',{'class':des_sel})
    description = []
    for tag in des_tags:
        description.append(tag.text.strip()) 
    return description

def get_link():
    # To get link of the project topic.
    url = 'https://github.com/topics'
    soup = get_webdata(url)
    link_sel = "d-flex no-underline"
    link_tags = soup.find_all('a',{'class': link_sel})
    
    links = []
    base = 'https://github.com'
    for tag in link_tags:
        links.append(base + tag['href'] )
    return links

def create_topic_df(title,description,links):
    # To create the DataFrame of top 30 project topics.
    topic_dict = {'Title':title,'Description':description,'Link':links}
    df = pd.DataFrame(topic_dict)
    return df

def scrape_project_topics():
    # To get the DataFrame of top 30 Github Project Topics.
    url = 'https://github.com/topics'
    soup = get_webdata(url)
    # To get title name of project topic.
    title = get_title()
    # To get description of project topic.
    description = get_description()
    # To get url of project topic.
    links = get_link()
    # Calling function to create Dataframe.
    df = create_topic_df(title,description,links)
    return df


#Scrapig Github topics webpage for top 25 repositories
#To get the dictionary of the repository data.
def get_repo(url):
    # To get the dataframe of repositories in each top topics.
    soup = get_webdata(url)
    # To get list of repository tags
    repo_selector = 'f3 color-text-secondary text-normal lh-condensed'
    repo_tag = soup.find_all('h1',{"class":repo_selector})
    # To get list of rating tags.
    star_selector = 'social-count float-none'
    star_tag = soup.find_all('a',{'class':star_selector})
    #Creating dictionaty for appending variables.
    repo_dict = {'Username':[], 'Userurl':[], 'Reponame':[], 'Repourl':[], 'Ratings':[]}
    # Base url for the github repository
    base = 'https://github.com'
    # To populate dictionary with different repository variables.
    for i in range(len(repo_tag)):
        user_tag  = repo_tag[i]('a')
        user_name = user_tag[0].text.strip()
        user_url = base + user_tag[0]['href']
        repo_name = user_tag[1].text.strip()
        repo_url = base + user_tag[1]['href']
        rating   = str_to_float(star_tag[i].text.strip())
        repo_dict['Username'].append(user_name)
        repo_dict['Userurl'].append(user_url)
        repo_dict['Reponame'].append(repo_name)
        repo_dict['Repourl'].append(repo_url)
        repo_dict['Ratings'].append(rating)
    return create_repo_df(repo_dict)

# Convert ratings into integer.
def str_to_float(star):
    if star[-1] == 'k':
        return int(float(star[:-1])*1000)
    return int(star[:-1])

# Create a data frame out of dictionary
def create_repo_df(dictr):
    df = pd.DataFrame(dictr)
    return df

# To scrape repository data as DataframeS.
def load_topics(topic_url,path, Title):
    if os.path.exists(path):
        print('The file {} already exits. Skipping....'.format(path))
        return
    topic_df = get_repo(topic_url)
    topic_df.to_csv(path, index = None)
    print(Title,'is downloaded')
    
# Main function to scrape the data from Github Website.
def scrape_project_repo():
    print('Scraping top topics from Github')
    topics_df = scrape_project_topics()
    os.makedirs('Repository_data',exist_ok = True)
    for index, row in topics_df.iterrows():
        print("Scraping top repositories for {}".format(row['Title']))
        load_topics(row['Link'], '/resources/project/repo_data/' + row['Title'] + '.csv', row['Title'])  
        
        
 #END       
