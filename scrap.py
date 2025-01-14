from selenium import webdriver
from selenium.webdriver.common.by import By

website = 'https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
path='C:/Users/miraj/OneDrive/Desktop/chromedriver-win64/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(website)

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

        # Find the price (if available) - adjust according to the actual structure of the page
        price = product.find_element(By.CLASS_NAME, 'Otbq5D').text.strip() if product.find_elements(By.CLASS_NAME,
                                                                                                    'Otbq5D') else 'Not Available'

        # Print or store the extracted data
        print(f"Product Name: {product_name}")
        print(f"Product Link: {product_link}")
        print(f"Image URL: {image_url}")
        print(f"Price: {price}")
        print('-' * 40)

    except Exception as e:
        print(f"Error extracting data for a product: {e}")

#driver.quit()