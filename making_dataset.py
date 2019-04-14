# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 04:39:57 2019

@author: Manish
"""

import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

def push_data(s,tag):
"""
    this function take input as the link of the first poem with the tag of poem
    and retrives the poem,poem name,poet name from the next 50 pages.
"""
    current_url =s
    for i in range(50):
        try:
            uclient = urlopen(current_url)
            page_html = uclient.read()
            uclient.close()
            
            #making soup of the page and storing it
            page_soup= soup(page_html,"html.parser")
            
            #finding the url for the next poem and storing it for next loop 
            next_url_container=page_soup.findAll("a",{"id":"next_link_video"})
            next_url =next_url_container[0]
            next_url = "https://www.poemhunter.com"+next_url.get("href")
            
            #finding poem on the page and title on the page and stroring them in container for retrieval
            poem_container = page_soup.findAll("div",{"class":"KonaBody"})
            title_container =page_soup.findAll("h2",{"class":"title w-660 black"})
            poem=poem_container[0]
            title= title_container[0]          
            poem=poem.p.get_text(strip=True ,separator='|').replace(',','|')

            #retrieving poet name from title
            l=title.text.split('-')
            title=l[0]
            poet=l[-1].split(' ')
            poet =poet[-1]+" "+poet[-2]
            category=tag
            
            #writing the content in file in csv format
            f.write(title.replace(",","|") + "," +poem+"," + poet + "," + category+'\n')
            current_url = next_url
        except:
            pass

if __name__=="__main__":
    file_name="poems.csv"
    f=open(file_name,'w')
    headers ="poem_name, poem_content ,poet_name ,category\n"
    f.write(headers)
    #passing link of the poem hunter site for scraping the content
    push_data("https://www.poemhunter.com/poems/lonely/page-1/31929/","lonely")
    push_data("https://www.poemhunter.com/poems/lonely/page-2/12830184/","lonely")
    push_data("https://www.poemhunter.com/poems/beauty/page-1/33137/","beauty")
    push_data("https://www.poemhunter.com/poems/beauty/page-2/35264/","beauty")
    push_data("https://www.poemhunter.com/poems/nature/page-1/150514/","nature")
    push_data("https://www.poemhunter.com/poems/nature/page-2/3119285/","nature")
    push_data("https://www.poemhunter.com/poems/believe/page-1/32293/","believe")
    push_data("https://www.poemhunter.com/poems/believe/page-2/19658/","believe")
    f.close()