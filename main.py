import codecs
import time

import selenium
from selenium import webdriver
import json
options = webdriver.ChromeOptions()
#options.add_argument('--headless')
options.add_argument('--window-size=1920,4000')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'
driver_path: str = r'D:\Programs\BrowserDriver\chromedriver.exe'
driver = webdriver.Chrome(options=options, executable_path=driver_path)
driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
driver.get("https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=EXTERNALPAGES&ARGUMENTS=-N000000000000001,-N000324,-Awelcome")
driver.find_element_by_xpath('//*[@id="field_user"]').send_keys(USERNAME)
time.sleep(5)
driver.find_element_by_xpath('//*[@id="field_pass"]').send_keys(PASSWORD)
driver.find_element_by_xpath('//*[@id="logIn_btn"]').click()
time.sleep(5)
driver.find_element_by_xpath('//*[@id="link000310"]/a').click()
time.sleep(5)
Noten = driver.find_element_by_xpath('//*[@id="contentSpacer_IE"]/div').text
element = driver.find_element_by_tag_name('body')
element_png = element.screenshot_as_png
driver.close()
with open("D:/Noten.png", "wb") as file:
    file.write(element_png)
    file.close()
with codecs.open('D:/Noten.txt', 'w', 'utf-8-sig') as f:
    # Uhrzeit und Liste in Txt speichern
    f.write(Noten)
    f.close()
