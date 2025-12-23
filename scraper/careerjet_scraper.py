import requests
from bs4 import BeautifulSoup
from utils.formatter import JobFormatter
import urllib.parse

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from utils.formatter import JobFormatter

class CareerjetScraper:
    def __init__(self):
        self.driver = None

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape(self, designation, location, experience):
        print(f"Scraping Careerjet for {designation} in {location}...")
        jobs = []
        try:
            self.setup_driver()
            # URL: https://www.careerjet.co.in/search/jobs?s={}&l={}
            url = f"https://www.careerjet.co.in/search/jobs?s={designation}&l={location}"
            print(f"DEBUG: Careerjet URL: {url}")
            
            self.driver.get(url)
            time.sleep(5) # Wait for Cloudflare/JS
            
            # Check title
            print(f"DEBUG: Page Title: {self.driver.title}")
            
            # Selector: article.job or div.job
            job_cards = self.driver.find_elements(By.CLASS_NAME, "job")
            print(f"DEBUG: Found {len(job_cards)} job cards on Careerjet")
            
            count = 0
            for card in job_cards:
                if count >= 5: break
                try:
                    # Extraction using selenium
                    try:
                        title = card.find_element(By.TAG_NAME, "h2").text
                        link_elem = card.find_element(By.TAG_NAME, "h2").find_element(By.TAG_NAME, "a")
                        link = link_elem.get_attribute("href")
                    except:
                        title = "Unknown"
                        link = url
                    
                    try:
                        company = card.find_element(By.CLASS_NAME, "company").text
                    except:
                        company = "Confidential"
                        
                    try:
                        loc = card.find_element(By.CLASS_NAME, "location").text
                    except:
                        loc = location
                        
                    try:
                        desc = card.text
                        salary = "Not Disclosed"
                        # Salary check
                        # (Simulated logic or try finding specific class if exists)
                    except:
                        pass
                    
                    job = {
                        "Job Title": title,
                        "Company Name": company,
                        "Location": loc,
                        "Experience Required": str(experience) + " Years",
                        "Salary Details": "Not Disclosed",
                        "Job Portal Name": "Careerjet",
                        "Job URL": link
                    }
                    jobs.append(JobFormatter.normalize_job(job))
                    count += 1
                except Exception as e:
                    continue

        except Exception as e:
            print(f"Error scraping Careerjet: {e}")
        finally:
            if self.driver:
                self.driver.quit()
        
        return jobs
