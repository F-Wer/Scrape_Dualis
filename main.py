import codecs
import os
import smtplib
import ssl
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from selenium import webdriver
from PIL import Image
from secret import *


class scrape_Grades():
    def Scrape(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--window-size=1920,4000')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.binary_location = r'C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe'
        driver_path: str = r'D:\Python\webdriver\chromedriver.exe'
        driver = webdriver.Chrome(options=options, executable_path=driver_path)
        driver.execute_cdp_cmd("Network.setExtraHTTPHeaders", {"headers": {"User-Agent": "browserClientA"}})
        print('Open Chrome')
        driver.get("https://dualis.dhbw.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=EXTERNALPAGES&ARGUMENTS=-N000000000000001,-N000324,-Awelcome")
        driver.find_element_by_xpath('//*[@id="field_user"]').send_keys(username)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="field_pass"]').send_keys(password)
        driver.find_element_by_xpath('//*[@id="logIn_btn"]').click()
        print('Logged in')
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="link000310"]/a').click()
        time.sleep(2)
        Noten = driver.find_element_by_xpath('//*[@id="contentSpacer_IE"]/div').text
        element = driver.find_element_by_tag_name('body')
        element_png = element.screenshot_as_png
        driver.close()
        with open("D:/Noten.png", "wb") as file:
            file.write(element_png)
            file.close()
        with codecs.open('D:/Noten.txt', 'w') as f:
            f.write(Noten)
            f.close()
            os.system('D:/Noten.txt')

    def Send_Mail(self):
        img_data = open("D:/Noten.png", 'rb').read()
        port = 465  # For SSL
        # Create a secure SSL context
        context = ssl.create_default_context()


        # reading the file in binary mode. Because it is saved as a UTF-8 file and there is a error, if you try to convert it to ASCII
        r = open('D:/Noten.txt', "r")
        msg = MIMEMultipart()
        msg.attach(MIMEText(r.read()))
        msg['Subject'] = 'Dualis'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        image = MIMEImage(img_data, name=os.path.basename('Noten.png'))
        msg.attach(image)
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, passwort_g)
            print("Login for E-Mail")
            server.sendmail(sender_email, receiver_email, msg.as_string())
            print("Email send")

o = scrape_Grades()
o.Scrape()
o.Send_Mail()