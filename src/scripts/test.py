from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


driver = webdriver.Chrome()
driver.get("https://meet.google.com/wph-fjdb-npn")
#assert "Python" in driver.title
time.sleep(10)
elem = driver.find_element(By.CLASS_NAME, "qdOxv-fmcmS-wGMbrd")
elem.clear()
elem.send_keys("ROBOT")
elem.send_keys(Keys.RETURN)
#assert "No results found." not in driver.page_source
time.sleep(60)
driver.close()