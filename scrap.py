from selenium import webdriver

website = 'https://www.flipkart.com/'
path='C:/Users/miraj/OneDrive/Desktop/chromedriver-win64/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get(website)

#driver.quit()