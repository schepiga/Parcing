import ast
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from pymongo import MongoClient

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get("https://www.mvideo.ru/?cityId=CityCZ_975")

wait = WebDriverWait(driver, 10)
button_popup = driver.find_element_by_class_name('span[@data-close="true"]')
while True:
    try:
        close_button = wait.until(EC.presence_of_element_located(button_popup))
    except Exception as e:
        print(e)
    else:
        button_popup.clik()

actions = ActionChains(driver)
goods = driver.find_element_by_xpath('//div[contains(h2, "Новинки")]')
actions.move_to_element(goods).perform()

while True:
    try:
        next_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(h2, "Новинки")]/../..//a[contains(@class, "next-btn")]')
        )
        )
    except Exception as e:
        break
    else:
        next_button.click()

new_goods = driver.find_element_by_xpath(
    'div[contains(h2, "Новинки")]/../..//a[contains(@class, "fl-product-tile-picture")]')

client = MongoClient('localhost', 27017)
new_goods_db = client['mvideo15082021']

for itm in new_goods:
    name = itm.get_attribete('data-product-info')
    goods_list = ast.literal_eval(name)
    new_goods_db.goods.inset_one(goods_list)
