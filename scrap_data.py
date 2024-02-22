# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 21:31:13 2024

@author: User
"""
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
import pandas as pd
from pymongo import MongoClient
import logging
import os 
from webdriver_manager.chrome import ChromeDriverManager
from fastapi import FastAPI

import uvicorn
app = FastAPI()

DBURL ="mongodb://localhost:27017/"
client = MongoClient(DBURL)
db = client.facebook_scraping
log_path=os.getcwd().replace("\\","/")
logging.basicConfig(filename=log_path+'scraping.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)    
optionsoptions = Options()
optionsoptions.add_argument('--no-sandbox')
optionsoptions.add_argument('--disable-dev-shm-usage')
optionsoptions.headless = True
optionsoptions.add_argument('--headless')
prefs = {"profile.managed_default_content_settings.images":2,
         "profile.default_content_setting_values.notifications":2,
         "profile.managed_default_content_settings.stylesheets":2,
         "profile.managed_default_content_settings.cookies":2,
         "profile.managed_default_content_settings.javascript":1,
         "profile.managed_default_content_settings.plugins":1,
         "profile.managed_default_content_settings.popups":2,
         "profile.managed_default_content_settings.geolocation":2,
         "profile.managed_default_content_settings.media_stream":2,
}
optionsoptions.add_experimental_option("prefs",prefs)

@app.get("/scrape/{page_name}")
async def scrap_page(page_name):
    try:
        
        driver = webdriver.Chrome(options=optionsoptions,executable_path = "./chromedriver.exe")       
        driver.get("https://www.facebook.com/"+str(page_name))
        driver.maximize_window()
        time.sleep(3)
        try:
            close=driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[1]/div/div[2]/div/div/div/div[1]/div/i")
            close.click()
        except:
            pass
        try:
            for _ in range(3):
                driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
                time.sleep(2)
        except:
            pass
            
        
        posts=[]
        photos=[]
        info=[]
        
        try:
            info1=driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div/div[3]")
            info.append(info1.text)
        except:
            pass
        try:
            info2=driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[1]/div[2]/div/div[1]/div/div/div/div/div[2]/div[1]/div/div/span")
            info.append(info2.text)
        except:
            pass
        try:
            info3=driver.find_element_by_tag_name("ul")
            info.append(info3.text)
        except:
            pass
        
        try:
            postss=driver.find_elements_by_xpath("//div[@class='x1iorvi4 x1pi30zi x1l90r2v x1swvt13']")
            for post in postss:
                posts.append(post.text)
        except:
            pass
        try:
            photoss=driver.find_elements_by_xpath("//img[@class='x1ey2m1c xds687c x5yr21d x10l6tqk x17qophe x13vifvy xh8yej3 xl1xv1r']")
            for post in photoss:
                photos.append(str(post.get_attribute("src")))
        except:
            pass
        info='/n'.join(str(v) for v in info)
        photos='*****'.join(str(v) for v in photos)
        posts='/n'.join(str(v) for v in posts)
        
        di = {"page_info" : [info],"posts":[posts],"photos":[photos]}
        dataee=pd.DataFrame(di)
        record=dataee.to_dict('records')
        db.data.insert_many(record)
        return {"page_info" : info,"posts":posts,"photos":photos}
    except Exception as e:
        logger.error(e)
        return {"info" :"somthing went wrong"}

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)