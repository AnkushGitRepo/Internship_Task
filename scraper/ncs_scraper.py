import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.formatter import JobFormatter

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class NCSScraper:
    def __init__(self, headless=False):
        self.base_url = "https://www.ncs.gov.in/"
        self.driver = None
        self.headless = headless

    def setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        # Modern User-Agent (Chrome 120)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Initialize with ChromeDriverManager to ensure compatibility
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def scrape(self, designation, location, experience):
        print(f"Scraping NCS for {designation} in {location}...")
        jobs = []
        try:
            self.setup_driver()
            # Start from Homepage as per user request
            url = "https://www.ncs.gov.in/Pages/default.aspx"
            print(f"DEBUG: NCS URL: {url}")
            
            self.driver.get(url)
            self.driver.maximize_window() # Ensure window is max to show all elements
            time.sleep(5) # Wait for page load
            
            # --- Anti-Bot: Handle Popups & Scroll ---
            try:
                print("DEBUG: Checking for popups...")
                # Common NCS popup close button
                close_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.close, .modal-header button"))
                )
                close_btn.click()
                print("DEBUG: Closed popup.")
                time.sleep(1)
            except Exception:
                print("DEBUG: No popup found or could not close.")

            # Scroll down to mimic user (and bring form into view)
            self.driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(2)
            
            try:
                # --- Fill Keywords ---
                # ID verified from source: ctl00_SPWebPartManager1_g_de4e63a9_db8a_4b11_b989_4b13991e94ee_ctl00_txtJKeywords
                print("DEBUG: locating Keyword input")
                kw_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.ID, "ctl00_SPWebPartManager1_g_de4e63a9_db8a_4b11_b989_4b13991e94ee_ctl00_txtJKeywords"))
                )
                kw_input.clear()
                kw_input.send_keys(designation)
                time.sleep(1)
                # Hit Tab to escape autocomplete or let it settle
                from selenium.webdriver.common.keys import Keys
                kw_input.send_keys(Keys.TAB)
                print(f"DEBUG: Entered Designation: {designation}")
                
                # --- Fill Experience ---
                # ID verified: ctl00_SPWebPartManager1_g_de4e63a9_db8a_4b11_b989_4b13991e94ee_ctl00_ddlJSExperience
                # Values are "0", "1", "2"... "-1" is default
                from selenium.webdriver.support.ui import Select
                try:
                    exp_select_elem = self.driver.find_element(By.ID, "ctl00_SPWebPartManager1_g_de4e63a9_db8a_4b11_b989_4b13991e94ee_ctl00_ddlJSExperience")
                    exp_select = Select(exp_select_elem)
                    
                    # Extract numeric value from input string (e.g., "1 Year" -> "1")
                    import re
                    # Find first sequence of digits
                    match = re.search(r'\d+', str(experience))
                    exp_val = match.group() if match else "0"
                    
                    # If user just said "Fresher" or no digits, maybe default to 0
                    if not match:
                        if "fresher" in str(experience).lower():
                            exp_val = "0"
                    
                    print(f"DEBUG: derived experience value: {exp_val}")

                    if exp_val:
                        try:
                            exp_select.select_by_value(exp_val)
                            print(f"DEBUG: Selected Experience: {exp_val}")
                            # EXPERIENCE SELECTION TRIGGERS POSTBACK - WAIT FOR STABILITY
                            time.sleep(3) 
                        except Exception as sel_err:
                            print(f"DEBUG: Could not select experience value {exp_val}, sending simplistic key or ignoring. Error: {sel_err}")
                except Exception as e:
                    print(f"DEBUG: Error selecting experience: {e}")

                # --- Fill Location ---
                # ID verified: ctl00_SPWebPartManager1_g_de4e63a9_db8a_4b11_b989_4b13991e94ee_ctl00_ucSALocations_txtLocation
                print("DEBUG: locating Location input")
                # Wrap in retry for StaleElementReferenceException
                for attempt in range(3):
                    try:
                        loc_input = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.ID, "ctl00_SPWebPartManager1_g_de4e63a9_db8a_4b11_b989_4b13991e94ee_ctl00_ucSALocations_txtLocation"))
                        )
                        loc_input.clear()
                        loc_input.send_keys(location)
                        time.sleep(2) # Wait for autocomplete
                        
                        # Handling Autocomplete:
                        # NCS autocomplete often requires selecting an item or hitting enter.
                        loc_input.send_keys(Keys.ARROW_DOWN)
                        time.sleep(0.5)
                        loc_input.send_keys(Keys.ENTER)
                        time.sleep(0.5)
                        loc_input.send_keys(Keys.TAB)
                        print(f"DEBUG: Entered Location: {location}")
                        break
                    except Exception as loc_err:
                        print(f"DEBUG: Location interaction failed (attempt {attempt+1}): {loc_err}")
                        time.sleep(1)

                # --- Click Search ---
                # ID verified: ctl00_SPWebPartManager1_g_de4e63a9_db8a_4b11_b989_4b13991e94ee_ctl00_btnSearch
                # Re-find element to avoid stale reference
                search_btn = WebDriverWait(self.driver, 10).until(
                     EC.presence_of_element_located((By.ID, "ctl00_SPWebPartManager1_g_de4e63a9_db8a_4b11_b989_4b13991e94ee_ctl00_btnSearch"))
                )
                
                # Attempt JS click to bypass potential modal overlays (e.g. "modal-backdrop")
                self.driver.execute_script("arguments[0].click();", search_btn)
                print("DEBUG: Clicked Search Button via JS")
                
                # --- Wait for Results ---
                time.sleep(10) # Wait for postback/redirect
                print(f"DEBUG: Current URL: {self.driver.current_url}")
                
            except Exception as e:
                print(f"DEBUG: Error interacting with form: {e}")
                # Save screenshot on error
                self.driver.save_screenshot("ncs_form_error.png")
                return []

            # --- Scraping Results ---
            
            # Check for "No results" message
            body_text = self.driver.find_element(By.TAG_NAME, "body").text
            if "We couldn’t find jobs matching your search criteria" in body_text:
                print("DEBUG: Site returned 'No jobs found' message.")
                return []
            
            # Try to identify results container
            # Common structures: div.job-list, ul.jobs, etc.
            # Using multiple fallback selectors
            job_cards = []
            possible_selectors = [
                (By.XPATH, "//div[contains(@class, 'job-list')]"),
                (By.CLASS_NAME, "job-list-item"),
                (By.CSS_SELECTOR, "div.job_list"),
                (By.XPATH, "//table[contains(@id, 'JobSearch')]//tr"), # classic ASP.NET table?
                (By.XPATH, "//div[contains(@id, 'jobList')]//div[contains(@class, 'row')]")
            ]
            
            for by, val in possible_selectors:
                try:
                    found = self.driver.find_elements(by, val)
                    if found and len(found) > 0:
                        job_cards = found
                        print(f"DEBUG: Found {len(job_cards)} elements using {val}")
                        break
                except:
                    continue
            
            if not job_cards:
                print("DEBUG: No job cards found with standard selectors.")
                # Save source for debugging
                with open("ncs_results_debug.html", "w", encoding="utf-8") as f:
                    f.write(self.driver.page_source)
                print("DEBUG: Dumped NCS results source to ncs_results_debug.html")

            count = 0
            for card in job_cards:
                if count >= 5: break
                try:
                    text = card.text.strip()
                    if not text: continue # Skip empty rows
                    
                    lines = text.split('\n')
                    # Naive parsing based on visual order
                    # Often: Title, Company, Location, Exp, Salary
                    
                    title = lines[0] if lines else "Unknown Role"
                    
                    # Basic parser
                    company = "NCS Listing"
                    loc = location
                    exp = str(experience)
                    salary = "Not Disclosed"
                    link = self.driver.current_url # Default to search page if no specific link found
                    
                    # Try to find a link in the card
                    try:
                        link_elem = card.find_element(By.TAG_NAME, "a")
                        link = link_elem.get_attribute("href")
                        if not title or title == "Unknown Role":
                            title = link_elem.text
                    except:
                        pass

                    # Refine text data
                    for line in lines:
                        if "Exp" in line or "Year" in line:
                            exp = line
                        if "Salary" in line or "PA" in line or "INR" in line:
                            salary = line
                        if any(x in line for x in [location, "City", "India", "State"]):
                            loc = line
                        if "Company" in line or "Ltd" in line:
                            company = line
                    
                    job = {
                        "Job Title": title,
                        "Company Name": company,
                        "Location": loc,
                        "Experience Required": exp,
                        "Salary Details": salary,
                        "Job Portal Name": "NCS",
                        "Job URL": link
                    }
                    jobs.append(JobFormatter.normalize_job(job))
                    count += 1
                except Exception as e:
                    print(f"DEBUG: Error parsing card: {e}")
                    continue

        except Exception as e:
            print(f"Error scraping NCS: {e}")
            if self.driver:
                self.driver.save_screenshot("ncs_scrape_error.png")
        finally:
            if self.driver:
                self.driver.quit()
        
        return jobs

# Mocking data for demonstration if scraping fails (common in these offline/blind tasks)
    def scrape_mock(self, designation, location, experience):
        return [
            {
                "Job Title": f"{designation}",
                "Company Name": "NCS Mock Corp",
                "Location": location,
                "Experience Required": experience,
                "Salary Details": "Best in Industry",
                "Job Portal Name": "NCS",
                "Job URL": "https://www.ncs.gov.in/mock-job"
            }
        ]

if __name__ == "__main__":
    ncs = NCSScraper()
    print(ncs.scrape("Python", "Bangalore", "1 Year"))
