from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get("https://www.mvideo.ru/")

# button_popup = driver.find_element_by_class_name('main-container')
button_popup = driver.find_element_by_class_name('tooltipster-bottom')
button_popup.click()

# sales_button = driver.find_element_by_xpath('//a[@class=close)]')
# actions.move_to_element(sales_button).perform()

wait = WebDriverWait(driver, 5)

while True:
    try:
        close_button = wait.until(EC.presence_of_element_located(button_popup))
    except Exception:
        break
    else:
        button_popup.clik()

actions = ActionChains(driver)
goods = driver.find_element_by_xpath('//div[contains(h2, "Новинки")]')
actions.move_to_element(goods).perform()

wait = WebDriverWait(driver, 5)

while True:
    try:
        next_button = wait.until(EC.element_to_be_clickable(By.XPATH, '//div[contains(h2, "Новинки")]'))
    except Exception:
        break
    else:
        next_button.click()





