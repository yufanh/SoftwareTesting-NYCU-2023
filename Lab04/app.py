from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver.chrome.service import Service as ChromiumService
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.edge.service import Service as EdgeService
# from webdriver_manager.microsoft import EdgeChromiumDriverManager


if __name__ == '__main__':
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options = options)
    # driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options = options)
    driver.get("https://www.nycu.edu.tw/")
    driver.maximize_window()
    news_click = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, r'新聞')))
    news_click.click()
    first_news = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//li[@class='su-post'][1]//a")))
    first_news.click()
    title = driver.find_element(By.XPATH, "//h1[@class='single-post-title entry-title']").text
    print(title)
    content = driver.find_element(By.XPATH, "//div[@class='entry-content clr']").text
    print(content)
    driver.switch_to.new_window('tab')
    driver.get("https://www.google.com")
    search = driver.find_element(By.NAME,'q')
    search.send_keys("311552017")
    search.send_keys(Keys.ENTER)
    search_title = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='MjjYud'][2]//h3")))
    print(search_title.text)
    driver.close()
