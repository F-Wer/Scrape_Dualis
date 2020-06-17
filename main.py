import codecs
import os
import shutil
import smtplib
import ssl
import time
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium import webdriver
from secret import *
'''
There has to be a file called secret.py with following arg:
passwort_g='' 
receiver_email=''
sender_email = ""
username=''
password=''
'''
from email import encoders
#Scraping the current grades for the DHBW Ravensburg

class scrape_Grades():
    def Scrape(self):
        #Open chrome with a few options so that it's harder for sites to detect a bot
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        driver = webdriver.Chrome(options=options, executable_path=r'D:\Python\webdriver\chromedriver.exe')
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
        print('Close Chrome')
        #Saving the scraped grades as a picture and as plain text
        with open("D:/Noten.png", "wb") as file:
            file.write(element_png)
            file.close()
        with codecs.open('D:/Noten.txt', 'w') as f:
            f.write(Noten)
            f.close()
        print('Files saved')

    def Send_Mail(self):
        #Copy the current script; I have to save the file as a txt file bc. some email providers don't like executables
        shutil.copy(__file__, 'D:/main.txt')
        port = 465  # For SSL
        # Create a secure SSL context
        context = ssl.create_default_context()
        # reading the file in binary mode. Because it is saved as a UTF-8 file and there is a error, if you try to convert it to ASCII
        print('Creating E-Mail')
        r = open('D:/Noten.txt', "r") #Send the grades as plain text in the email body
        msg = MIMEMultipart()
        msg.attach(MIMEText(r.read()))
        r.close()
        msg['Subject'] = 'Dualis'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        file = ('D:/main.txt', 'D:/Noten.txt', 'D:/Noten.png')
        for files in file: #Attaching the grades as plain text file and picture and the current script
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(files, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(files))
            msg.attach(part)
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(sender_email, passwort_g)
            print("Login for E-Mail")
            server.sendmail(sender_email, receiver_email, msg.as_bytes())
            print("Email send")

if __name__ == "__main__":
    o = scrape_Grades()
    o.Scrape()
    o.Send_Mail()
