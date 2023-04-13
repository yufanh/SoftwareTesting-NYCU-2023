from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException
import time

if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options = options)
    # driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    driver.maximize_window()
    driver.get('https://docs.python.org/3/tutorial/index.html')
    wait = WebDriverWait(driver, 10)
    select = Select(wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]//*[@id="language_select"]'))))
    select.select_by_value("zh-tw")

    while True:
        try:
            select.first_selected_option
        except StaleElementReferenceException:
            break

    myTitle = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]//h1')))
    cont = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]//p')))
    print(myTitle.text)
    print(cont.text)

    wait.until(EC.presence_of_element_located((By.XPATH,'/html/body/div[2]/ul/li[11]/div/form/input[1]'))).send_keys("class" + Keys.RETURN)
    myText = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results"]/ul/li[1]/a')))
    print(myText.text)
    myText = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results"]/ul/li[2]/a')))
    print(myText.text)
    myText = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results"]/ul/li[3]/a')))
    print(myText.text)
    myText = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results"]/ul/li[4]/a')))
    print(myText.text)
    myText = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-results"]/ul/li[5]/a')))
    print(myText.text)
    driver.close()
