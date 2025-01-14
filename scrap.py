from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Setup for Selenium WebDriver
website = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
path = 'C:/Users/miraj/OneDrive/Desktop/chromedriver-win64/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(website)

# List to store product data
product_data = []

# Get total number of pages dynamically
def get_total_pages():
    try:
        pagination = driver.find_element(By.XPATH, '//nav[contains(@class,"WSL9JP")]')
        page_links = pagination.find_elements(By.TAG_NAME, 'a')

        # Extract the last page number
        last_page = int(page_links[-2].text)
        return last_page
    except Exception as e:
        print(f"Error fetching total pages: {e}")
        return 1  # Assume 1 page if we fail to detect total pages

# Function to scrape data from the current page
def scrape_page_data():
    products = driver.find_elements(By.CLASS_NAME, 'tUxRFH')

    for product in products:
        try:
            # Extract product link
            product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Extract product name (from alt text of the image)
            product_name = product.find_element(By.TAG_NAME, 'img').get_attribute('alt')

            # Extract image URL
            image_url = product.find_element(By.TAG_NAME, 'img').get_attribute('src')

            # Extract price (if available) - handle cases where it's not available
            price_element = product.find_elements(By.CLASS_NAME, '_30jeq3')  # Update class name for price
            price = price_element[0].text.strip() if price_element else 'Not Available'

            # Store the data as a dictionary
            product_data.append({
                'link': product_link,
                'name': product_name,
                'url': image_url,
                'price': price
            })

        except Exception as e:
            print(f"Error extracting data for a product: {e}")
            continue

# Loop to scrape all pages until the last page
current_page = 1
while True:
    print(f"Scraping page {current_page}...")

    # Scrape data for the current page
    scrape_page_data()

    # Try to get the total number of pages
    last_page = get_total_pages()

    if current_page >= last_page:
        print("Reached last page.")
        break  # Stop if the current page is the last page

    # Modify the URL to go to the next page and reload the page
    next_page_url = f'{website}&page={current_page + 1}'  # Modify URL to point to the next page
    driver.get(next_page_url)

    # Wait for the next page to load
    time.sleep(3)

    # Increment the current page
    current_page += 1

# Convert the list of product data to a DataFrame
df = pd.DataFrame(product_data)

# Save the data to Excel file
df.to_excel('flipkart_laptops.xlsx', index=False, engine='openpyxl')

# Print the DataFrame to verify
print(df)

# Quit the WebDriver after scraping is complete
driver.quit()
