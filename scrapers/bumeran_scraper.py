import time
import random
import logging
import os
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BumeranScraper:
    def __init__(self):
        """Initialize Bumeran scraper"""
        self.base_url = "https://www.bumeran.com.ar"
        self.driver = None
        self.wait = None
        self._setup_driver()
        
    def _setup_driver(self):
        """Setup Chrome driver with options"""
        # Try using a remote Selenium server if provided
        selenium_url = os.getenv('SELENIUM_URL')
        if selenium_url:
            try:
                chrome_options = Options()
                chrome_options.add_argument('--disable-blink-features=AutomationControlled')
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                chrome_options.add_argument('--window-size=1920,1080')
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
                chrome_options.add_experimental_option('useAutomationExtension', False)
                self.driver = webdriver.Remote(command_executor=selenium_url, options=chrome_options)
                self.wait = WebDriverWait(self.driver, 20)
                logger.info(f"Connected to remote Selenium at {selenium_url}")
                return
            except Exception as e:
                logger.warning(f"Failed to connect to remote Selenium: {e}. Falling back to local Chrome.")

        try:
            chrome_options = Options()
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 20)  # Increased timeout
            logger.info("Chrome driver initialized successfully")
        except Exception as e:
            logger.error(f"Error setting up driver: {e}")
            raise
            
    def search_jobs(self, position, location="", max_jobs=50, email=None, password=None):
        """
        Search for jobs on Bumeran
        If email/password provided, logs in first to get better access to apply URLs
        """
        jobs = []
        if not self.driver:
            self._setup_driver()
        
        try:
            # Login if credentials provided
            if email and password:
                self._login(email, password)

            page = 1
            while len(jobs) < max_jobs:
                # Build search URL with pagination
                # NOTE: Bumeran doesn't support location in the URL slug
                position_slug = position.lower().replace(' ', '-')
                
                if page == 1:
                    search_url = f"{self.base_url}/empleos-busqueda-{position_slug}.html"
                else:
                    search_url = f"{self.base_url}/empleos-busqueda-{position_slug}-pagina-{page}.html"
                
                logger.info(f"Searching Bumeran page {page}: {search_url}")
                self.driver.get(search_url)
                
                # Scroll to trigger lazy loading
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                time.sleep(2)
                
                # Check for 404 or no results
                if "404" in self.driver.title or "no encontrada" in self.driver.page_source.lower():
                    logger.info("Reached end of results")
                    break

                # Extract jobs from current page
                page_jobs = self._extract_jobs_from_page()
                
                if not page_jobs:
                    logger.info("No more jobs found on this page")
                    break
                
                # Process each job to get apply URL if logged in
                for job in page_jobs:
                    if len(jobs) >= max_jobs:
                        break
                        
                    # If logged in, visit page to get real apply URL
                    if email and password:
                        real_apply_url = self._get_apply_url(job['URL'])
                        if real_apply_url:
                            job['Apply_URL'] = real_apply_url
                    
                    jobs.append(job)
                    logger.info(f"Added job: {job['Title']}")
                
                logger.info(f"Extracted {len(page_jobs)} jobs from page {page}. Total: {len(jobs)}")
                
                page += 1
                
        except Exception as e:
            logger.error(f"Error during search: {e}")
        finally:
            pass
            
        return jobs

    def _login(self, email, password):
        """Login to Bumeran"""
        try:
            logger.info("Attempting to login to Bumeran...")
            self.driver.get(f"{self.base_url}/login")
            time.sleep(5)
            
            # Email
            email_input = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
            email_input.clear()
            email_input.send_keys(email)
            
            # Password
            pass_input = self.driver.find_element(By.ID, "password")
            pass_input.clear()
            pass_input.send_keys(password)
            
            # Submit
            submit_btn = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_btn.click()
            
            # Wait for login to complete
            time.sleep(8)
            logger.info("Login submitted")
            
        except Exception as e:
            logger.error(f"Login failed: {e}")

    def _get_apply_url(self, job_url):
        """Visit job page and extract apply URL"""
        try:
            logger.info(f"Visiting job page: {job_url}")
            self.driver.get(job_url)
            time.sleep(3) # Wait for load
            
            try:
                # Look for "Postular" button/link
                apply_links = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='postula'], a[href*='apply']")
                for link in apply_links:
                    href = link.get_attribute('href')
                    if href and href != job_url and 'bumeran' not in href:
                        return href # External link
                
                # If no external link, return job_url (internal apply)
                return job_url
                
            except:
                return job_url
                
        except Exception as e:
            logger.error(f"Error getting apply URL: {e}")
            return job_url

    def _extract_jobs_from_page(self):
        """Extract all jobs from current page"""
        jobs = []
        
        try:
            # Wait for React to render completely (Bumeran uses React)
            logger.info("Waiting for React to render...")
            time.sleep(8)  # React needs ~8 seconds to fully render job cards
            
            # Try to find job cards
            job_cards = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/empleos/']")
            
            if not job_cards:
                logger.warning("No job cards found on page")
                return jobs
            
            logger.info(f"Found {len(job_cards)} potential job cards")

            # Filter and extract job data
            seen_urls = set()
            for card in job_cards:
                try:
                    job_data = self._extract_job_details(card)
                    if job_data and job_data['URL'] not in seen_urls:
                        jobs.append(job_data)
                        seen_urls.add(job_data['URL'])
                except Exception as e:
                    logger.debug(f"Error extracting job details: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error extracting jobs from page: {e}")
            
        return jobs
        
    def _extract_job_details(self, job_card):
        """Extract details from a single job card"""
        try:
            job_data = {}
            
            # URL
            url = job_card.get_attribute('href')
            if not url or '/empleos/' not in url:
                return None
            job_data['URL'] = url
            # Default to job URL for apply URL (will be updated if logged in)
            job_data['Apply_URL'] = url

            # Title - usually in h2
            try:
                title_elem = job_card.find_element(By.TAG_NAME, "h2")
                job_data['Title'] = title_elem.text.strip()
            except:
                # If no h2, skip this card
                return None

            # Initialize defaults
            job_data['Company'] = "Confidencial"
            job_data['Location'] = "Argentina"
            job_data['Date_Posted'] = "Reciente"
            job_data['Salary'] = "No especificado"
            job_data['Job_Type'] = "Full-time"
            job_data['Level'] = "No especificado"
            job_data['Description'] = job_data['Title'] # Placeholder

            # Extract other details from h3 tags
            try:
                h3s = job_card.find_elements(By.TAG_NAME, "h3")
                for h3 in h3s:
                    text = h3.text.strip()
                    if not text:
                        continue
                        
                    # Heuristics to identify fields
                    if any(x in text.lower() for x in ["publicado", "actualizado", "nuevo", "hoy", "ayer"]):
                        job_data['Date_Posted'] = text
                    elif any(x in text for x in ["Buenos Aires", "Capital Federal", "CABA", "Córdoba", "Santa Fe", "Mendoza", "Neuquén", "Rosario", "Tucumán"]):
                        job_data['Location'] = text
                    elif text in ["Presencial", "Híbrido", "Remoto"]:
                        job_data['Job_Type'] = text
                    elif len(text) < 50 and text != job_data['Title']: 
                        # Assume it's company if it's short and not one of the above
                        # Also check if it's a number (rating)
                        if not text.replace('.', '', 1).isdigit():
                            job_data['Company'] = text
            except:
                pass

            # Source
            job_data['Source'] = 'Bumeran'
            
            return job_data
                
        except Exception as e:
            return None
            
    def save_to_csv(self, jobs, filename=None):
        """Save jobs to CSV file"""
        try:
            if not jobs:
                logger.warning("No jobs to save")
                return None
                
            # Ensure results directory exists
            os.makedirs('results', exist_ok=True)
            
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"bumeran_jobs_{timestamp}.csv"
            
            filepath = os.path.join('results', filename)
            
            df = pd.DataFrame(jobs)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"Saved {len(jobs)} jobs to {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error saving to CSV: {e}")
            return None
            
    def close(self):
        """Close the browser"""
        try:
            if self.driver:
                self.driver.quit()
                logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")


if __name__ == "__main__":
    # Test the scraper
    scraper = BumeranScraper()
    try:
        jobs = scraper.search_jobs("Data Analyst", "Buenos Aires", max_jobs=20)
        if jobs:
            scraper.save_to_csv(jobs)
            print(f"Successfully extracted {len(jobs)} jobs")
        else:
            print("No jobs found")
    finally:
        scraper.close()
