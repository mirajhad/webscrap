from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Setup for Selenium WebDriver
website = 'https://www.flipkart.com/search?q=mobiles'
path = 'C:/Users/miraj/OneDrive/apps/chromedriver-win64/chromedriver.exe'
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
            price_element = product.find_elements(By.CLASS_NAME, 'Nx9bqj _4b5DiR')  # Update class name for price
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

# Function to check if the page is blank (i.e., no products)
def is_page_blank():
    try:
        # If no products are found on the page, return True (blank page)
        products = driver.find_elements(By.CLASS_NAME, 'tUxRFH')
        return len(products) == 0
    except Exception as e:
        print(f"Error checking if page is blank: {e}")
        return False

# Loop to scrape all pages until the last page
current_page = 1
retries = 0  # Counter for retries on blank pages
while True:
    print(f"Scraping page {current_page}...")

    # Check if the page is blank and retry up to 3 times
    while is_page_blank() and retries < 3:
        print(f"Page is blank. Retrying... ({retries + 1}/3)")
        retries += 1
        driver.refresh()  # Reload the page
        time.sleep(3)  # Wait for the page to reload

    # If the page is still blank after 3 retries, exit the loop
    if is_page_blank():
        print(f"Page is still blank after {retries} retries. Exiting...")
        break

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
    retries = 0  # Reset retries after a successful page load

# Convert the list of product data to a DataFrame
df = pd.DataFrame(product_data)

# Save the data to Excel file
df.to_excel('flipkart_laptops.xlsx', index=False, engine='openpyxl')

# Print the DataFrame to verify
print(df)

# Quit the WebDriver after scraping is complete
driver.quit()
