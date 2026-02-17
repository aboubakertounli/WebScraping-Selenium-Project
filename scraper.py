import os
import csv
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver(headless=True):
    """
    Initializes and returns a Chrome WebDriver instance.
    
    Args:
        headless (bool): Whether to run the browser in headless mode.
    
    Returns:
        webdriver.Chrome: The configured Chrome driver.
    """
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    # Adding a user-agent to avoid being blocked
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    chrome_options.binary_location = "/usr/bin/chromium-browser"
    # In the sandbox, Chromium and its driver are pre-installed
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def download_image(url, folder, filename):
    """
    Downloads an image from a URL and saves it to a local folder.
    
    Args:
        url (str): The URL of the image.
        folder (str): The local directory to save the image.
        filename (str): The name of the file to save.
    """
    if not url:
        return None
    
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            # Clean filename to remove invalid characters
            clean_filename = "".join([c for c in filename if c.isalnum() or c in (
                ' ', '.', '_')]).rstrip()
            filepath = os.path.join(folder, f"{clean_filename}.jpg")
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            return f"{clean_filename}.jpg"
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
    return None

def get_products(driver, keyword, pages=2):
    """
    Scrapes product data from Amazon for a given keyword across multiple pages.    
    Args:
        driver (webdriver.Chrome): The active WebDriver instance.
        keyword (str): The search keyword.
        pages (int): Number of pages to scrape.
        
    Returns:
        list: A list of dictionaries containing product information.
    """
    products = []
    base_url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
    
    for page in range(1, pages + 1):
        url = f"{base_url}&page={page}"
        print(f"Scraping page {page}: {url}")
        driver.get(url)
        
        # Explicit wait for product results to load
        try:
            wait = WebDriverWait(driver, 15)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-result-item')))
        except TimeoutException:
            print(f"Timeout waiting for page {page} to load.")
            continue
            
        # Find all product containers
        items = driver.find_elements(
            By.CSS_SELECTOR, 'div.s-result-item[data-component-type="s-search-result"]')
        
        for item in items:
            try:
                # Extract Title
                try:
                    # Broad selector for any heading in the result item
                    title_element = item.find_element(By.TAG_NAME, 'h2')
                    title = title_element.text.strip()
                except NoSuchElementException:
                    title = "N/A"
                
                # Extract Price
                try:
                    price_whole = item.find_element(
                        By.CSS_SELECTOR, 'span.a-price-whole').text
                    price_fraction = item.find_element(
                        By.CSS_SELECTOR, 'span.a-price-fraction').text
                    price = f"${price_whole}.{price_fraction}"
                except NoSuchElementException:
                    price = "N/A"
                
                # Extract Rating
                try:
                    rating_element = item.find_element(
                        By.CSS_SELECTOR, 'span.a-icon-alt')
                    rating = rating_element.get_attribute('innerHTML').split(' ')[0]
                except NoSuchElementException:
                    rating = "N/A"
                
                # Extract Image URL
                try:
                    image_element = item.find_element(
                        By.CSS_SELECTOR, 'img.s-image')
                    image_url = image_element.get_attribute('src')
                except NoSuchElementException:
                    image_url = None
                
                # Download image and get local filename
                image_filename = "N/A"
                if image_url:
                    # Use a shortened version of the title for the filename
                    safe_title = title[:30] if title != "N/A" else "product"
                    image_filename = download_image(
                        image_url, "images", f"{safe_title}_{len(products)}")
                
                products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "image_filename": image_filename
                })
                
            except Exception as e:
                print(f"Error extracting item: {e}")
                continue
                
    return products

def save_to_csv(products, filename="products.csv"):
    """
    Saves the list of products to a CSV file.
    
    Args:
        products (list): List of product dictionaries.
        filename (str): Name of the CSV file.
    """
    if not products:
        print("No products to save.")
        return
        
    keys = products[0].keys()
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(products)
        print(f"Successfully saved {len(products)} products to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    # Dynamic keyword input
    keyword = input("Enter the product you want to search for: ") or "laptop"
    
    # Create images directory if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")
        
    print(f"Starting scraper for: {keyword}")
    
    driver = None
    try:
        # Initialize driver (Headless mode enabled by default for server environment)
        driver = setup_driver(headless=True)
        
        # Scrape products from the first 2 pages
        product_list = get_products(driver, keyword, pages=2)
        
        # Save data to CSV
        save_to_csv(product_list, filename="/home/ubuntu/selenium_scraper/products.csv")
        
    except Exception as e:
        print(f"An error occurred during execution: {e}")
    finally:
        if driver:
            driver.quit()
            print("Browser closed.")

if __name__ == "__main__":
    main()
