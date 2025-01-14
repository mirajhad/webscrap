from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

# Setup for Selenium WebDriver
website = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
path = 'C:/Users/miraj/OneDrive/Desktop/chromedriver-win64/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(website)

# List to store product data
product_data = []

# Find all divs with the class 'tUxRFH' (each div contains a product)
products = driver.find_elements(By.CLASS_NAME, 'tUxRFH')

# Loop through each product and extract relevant data
for product in products:
    try:
        # Extract product link
        product_link = product.find_element(By.TAG_NAME, 'a').get_attribute('href')

        # Extract product name (from alt text of the image)
        product_name = product.find_element(By.TAG_NAME, 'img').get_attribute('alt')

        # Extract image URL
        image_url = product.find_element(By.TAG_NAME, 'img').get_attribute('src')

        # Extract price (if available) - handle cases where it's not available
        price_element = product.find_elements(By.CLASS_NAME, 'Otbq5D')
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

# Convert the list of product data to a DataFrame
df = pd.DataFrame(product_data)

# Save the data to CSV file
df.to_excel('flipkart_laptops.xlsx', index=False, engine='openpyxl')

# Print the DataFrame to verify
print(df)

# Quit the WebDriver after scraping is complete
driver.quit()
