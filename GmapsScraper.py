from selenium import webdriver
from bs4 import BeautifulSoup
import time
import io
import pandas as pd


#add your chrome driver path here
browser = webdriver.Chrome("Your chrome driver path")

#add your google map link whose data you want to scrape
browser.get('https://www.google.com/maps/place/abc')
actions = ActionChains(browser)

browser.maximize_window()
time.sleep(3)
content = browser.find_element_by_class_name('scrollable-show').click()
htmlstring = browser.page_source
afterstring=""
for i in range(12):
    afterstring = htmlstring
    actions.send_keys(Keys.PAGE_DOWN).perform()
    htmlstring = browser.page_source
    if (i>12):
        print ("ended scraping crack test one")
        actions.send_keys(Keys.PAGE_DOWN).perform()
        htmlstring = browser.page_source
        if (i>12):
           print ("--Scrapping End--")
           break
    time.sleep(3)
    

textdoc = io.open("data.txt", "a+", encoding="utf-8")
soup = BeautifulSoup(htmlstring,"html.parser")
mydivs = soup.findAll("div", {"class": "section-review-content"})
counter = 0
Reviwer_data ={'Reviewer Name':[],'Reviewer Rating':[],'Reviewer Profile URL':[],'Review':[],'Time':[]}
for a in mydivs:
    textdoc.write(str("\nReviewer name: "+a.find("div", class_="section-review-title").text)+" \n||Reviewerer Profile URL:"+ str(a.find("a").get('href')))
    textdoc.write(" \n||Review:" + a.find("span", class_="section-review-text").text+" \n||Time: " + a.find("span", class_="section-review-publish-date").text)
    textdoc.write("\n")
    textdoc.write(str(a.find("span", class_="section-review-stars")))
    textdoc.write("=========================================\n")
    Reviwer_data['Reviewer Name'].append(a.find("div", class_="section-review-title").text)
    Reviwer_data['Reviewer Rating'].append(str(a.find("span", class_="section-review-stars")))
    Reviwer_data['Reviewer Profile URL'].append(str(a.find("a").get('href')))
    Reviwer_data['Review'].append(a.find("span", class_="section-review-text").text)
    Reviwer_data['Time'].append(a.find("span", class_="section-review-publish-date").text)
    counter = counter + 1
print("Total reviews scraped:"+str(counter))
textdoc.close()
pd.DataFrame(Reviwer_data).to_csv('data.csv',index=0)

