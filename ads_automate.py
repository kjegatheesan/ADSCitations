import os
import re
import sys
import time

import pyperclip
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Set location of Chromedriver
# The Service class manage the start and stop of drivers + specifies the location of the drivers
s = Service("/usr/local/bin/chromedriver")

# Set some selenium chrome options
chromeOptions = Options()
# To keep the browser open even after the process has ended. Waits for the quit function to close the window.
chromeOptions.add_experimental_option("detach", True)
# To have the browser window open 
chromeOptions.headless = False 
driver = webdriver.Chrome(service=s, options=chromeOptions)

class ADSCitations:
    def __init__(self, ads_query, bib_file):
        self.ads_query = ads_query 
        self.bib_file = bib_file 

    def ads_automate(self):
        driver.get("https://ui.adsabs.harvard.edu/")
        driver.implicitly_wait(5)

        # Locate the search bar object using Inspect and retrieve the Xpath
        # Use find_element() with Xpath 
        search_bar = driver.find_element(By.XPATH, '//*[@id="query-search-input"]')
        search_bar.send_keys(self.ads_query)
        # Locate and click on the search button
        driver.find_element(By.XPATH, '//*[@id="landing-page-layout"]/section/div/div[1]/div/div[1]/div[3]/div/form/div/div/span/button').click()
        
        # Needs some time to load and locate the object - without this, it searches for the object before it exists and finds nothing
        time.sleep(3)

        # Display the paper title and author list  

        n_results = int(driver.find_element(By.XPATH, '//*[@id="search-bar-row"]/div/div[2]/div/span[2]').text)

        print("Your search returned {} results.".format(n_results))
    
        if n_results>1:

            if n_results>10:
                print("Displaying the first 10 results. If unsuccessful, please refine search query.")

                for i in range(1,11):
                    print(str(i) + " " + driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div/div[2]/ul/li[{i}]/div/div[2]/div/a/h3').text)
                    print(driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div/div[2]/ul/li[{i}]/div/div[3]/div/ul[1]').text)

            else:
                 for i in range(1,n_results+1):
                    print(str(i) + " " + driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div/div[2]/ul/li[{i}]/div/div[2]/div/a/h3').text)
                    print(driver.find_element(By.XPATH, f'//*[@id="main-content"]/div[1]/div/div/div[2]/ul/li[{i}]/div/div[3]/div/ul[1]').text)

                
            user_answer = input("Your choice: ")

            if user_answer==0: sys.exit(0)

            # Locate the search result link corresponding to the user_answer and click on it
            title_xpath = f'//*[@id="main-content"]/div[1]/div/div/div[2]/ul/li[{user_answer}]/div/div[2]/div/a/h3'
            title = driver.find_element(By.XPATH, title_xpath).text
            driver.find_element(By.XPATH, title_xpath).click()

        elif n_results==0:
            driver.close() 
            sys.exit(0)       

        else:
            title_xpath = '//*[@id="main-content"]/div[1]/div/div/div[2]/ul/li/div/div[2]/div/a/h3'
            title = driver.find_element(By.XPATH, title_xpath).text
            print(title)
            print(driver.find_element(By.XPATH, '//*[@id="main-content"]/div[1]/div/div/div[2]/ul/li/div/div[3]/div/ul[1]').text)
            driver.find_element(By.XPATH, title_xpath).click()

        time.sleep(1)

        # Locate the author and year of publication
        author = driver.find_element(By.XPATH, '//*[@id="authors-and-aff"]/ul/li[1]/a').text
        author_cite = author.split(",")[0].lower()
        year = driver.find_element(By.XPATH, '//*[@id="current-subview"]/div[1]/article/dl/dd[2]').text
        if year.isdigit(): 
            year_cite = year
        else:
            year_cite = year.split(" ")[1]

        article_cite = f"{author_cite}{year_cite}"

        # Locate the "Export Citation" link and click on it 
        driver.find_element(By.XPATH, '//*[@id="left-column"]/div/nav/a[9]/div').click()
        time.sleep(1)


        # Locate the "Copy to clipboard" link and click on it 
        driver.find_element(By.XPATH, '//*[@id="current-subview"]/div[8]/div/div/div/div[2]/div/div[1]/div/button[2]').click()

        driver.close()

        # Paste the text copied to the clipboard onto a .bib file
        # ... but store it in a variable first to manipulate it 
        bibtex = pyperclip.paste()
        pattern = r'\{([^}]*)\}'
        lst = re.findall(pattern, bibtex)
        str_to_rep = lst[0].split(",")[0]
        bibtex_write =  bibtex.replace(str_to_rep, article_cite)

        if not os.path.exists(self.bib_file):
            with open(self.bib_file, "w") as p:
                p.write(bibtex_write)
                p.close()

        else:
            with open(self.bib_file, "r") as f:
                if title in f.read():
                    print("Citation already added.")
                    f.close()
                else:    
                    with open(self.bib_file, "a") as  p:
                        p.write(bibtex_write)        
                        p.close()




        

