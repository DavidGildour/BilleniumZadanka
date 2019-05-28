import requests

from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

with webdriver.Firefox() as driver:
    driver.get('https://camera.deckchair.com/st-regis-le-morne-mauritius')
    assert 'Global HD Live Webcams' in driver.title

    elem = driver.find_element_by_class_name('action-button')
    url = elem.get_attribute('href')

with open('test.jpg', 'wb') as f:
    r = requests.get(url)
    f.write(r.content)

print("Image saved to file.")