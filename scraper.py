from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_hospitals():
    print("Scraping hospital data...")
    url = "https://sirs.kemkes.go.id/fo/home/dashboard_rs?id=0"

    # Initialize Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no GUI)
    driver = webdriver.Chrome(service=Service("path/to/chromedriver"), options=options)

    try:
        # Load the page
        driver.get(url)
        time.sleep(5)  # Allow time for JavaScript to load

        # Extract table data using BeautifulSoup
        soup = BeautifulSoup(driver.page_source, "html.parser")
        rows = soup.find_all("tr")[1:]  # Skip the header row
        hospitals = []

        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:  # Ensure the row has enough columns
                continue
            hospital_data = {
                "name": cols[1].text.strip(),
                "province": cols[2].text.strip(),
                "city": cols[3].text.strip(),
                "type": cols[4].text.strip(),
                "status": cols[5].text.strip()
            }
            hospitals.append(hospital_data)

        return hospitals

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        driver.quit()

def save_to_csv(data, filename="hospitals.csv"):
    if not data:
        print("No data to save.")
        return
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    hospitals = scrape_hospitals()
    if hospitals:
        save_to_csv(hospitals)
    else:
        print("No data scraped. Please check the website or your connection.")
