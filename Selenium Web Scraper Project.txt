# Selenium Web Scraper Project

This project is a professional Python-based web scraper designed to extract product data from e-commerce websites (specifically Amazon) using **Selenium**. It is built for academic evaluation, demonstrating best practices in web automation, data extraction, and error handling.

## 🎯 Project Objectives
- **Automated Browsing**: Uses Selenium to navigate through search results.
- **Dynamic Content Handling**: Manages JavaScript-rendered content that static scrapers like BeautifulSoup cannot handle.
- **Data Extraction**: Collects product titles, prices, ratings, and image URLs.
- **Media Management**: Automatically downloads product images into a local directory.
- **Structured Output**: Saves all scraped data into a clean `products.csv` file.

## ⚙️ Technical Features
- **Python & Selenium**: Core technologies for automation.
- **Chrome/Chromium WebDriver**: Managed via `webdriver-manager` for seamless setup.
- **Explicit Waits**: Uses `WebDriverWait` and `expected_conditions` instead of inefficient `time.sleep`.
- **Headless Mode**: Optional headless execution for server-side or background processing.
- **Graceful Error Handling**: Robustly handles missing data (prices, ratings) and network timeouts.

## 🧠 Why Selenium vs. BeautifulSoup?
In modern web development, many websites use frameworks like React, Vue, or Angular to render content dynamically using JavaScript. 
- **BeautifulSoup** only parses the initial HTML source code returned by the server. If the data is loaded via JavaScript after the page opens, BeautifulSoup will see an empty or incomplete page.
- **Selenium** controls a real web browser. It executes JavaScript, waits for elements to render, and interacts with the page exactly like a human user. This makes it essential for scraping modern, interactive websites.

## 📂 Project Structure
- `scraper.py`: The main Python script containing all scraping logic.
- `requirements.txt`: List of necessary Python libraries.
- `products.csv`: The output data file (generated after running).
- `images/`: Directory containing downloaded product images (generated after running).

## 🚀 Instructions to Run

### 1. Prerequisites
Ensure you have Python 3.x installed. You will also need Chrome or Chromium browser.

### 2. Install Dependencies
Run the following command to install required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Scraper
Execute the script using Python:
```bash
python scraper.py
```
The script will prompt you for a **search keyword** (e.g., "laptop" or "iphone"). It will then scrape the first 2 pages of results, download images, and save the data to `products.csv`.

## 🛠️ Code Structure
The script is organized into modular functions for clarity and reusability:
- `setup_driver()`: Configures and initializes the Chrome WebDriver.
- `get_products()`: Handles navigation and data extraction logic.
- `download_image()`: Manages image retrieval and local storage.
- `save_to_csv()`: Formats and exports data to CSV.

---
*Developed for Academic Evaluation - 2026*
