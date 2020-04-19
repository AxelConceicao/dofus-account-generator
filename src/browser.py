import json
import time
import string
import random
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select

def random_alphaNumeric_string(lettersCount, digitsCount):
    sampleStr = ''.join((random.choice(string.ascii_letters) for i in range(lettersCount)))
    sampleStr += ''.join((random.choice(string.digits) for i in range(digitsCount)))
    sampleList = list(sampleStr)
    random.shuffle(sampleList)
    finalString = ''.join(sampleList)
    return finalString

class Browser:
    driverTempmail = None
    driverDofus = None
        
    def runDofusLocaly(self, url = 'https://www.dofus.com/fr/mmorpg/jouer'):
        self.driverDofus = webdriver.Firefox()
        self.driverDofus.get(url)
        
    def runDofus(self, proxy = None):
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True
        firefox_capabilities["pageLoadStrategy"] = "none" 
        if proxy is not None:
            firefox_capabilities['proxy'] = {
                "proxyType": "MANUAL",
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy
            }
        url = 'https://www.dofus.com/fr/mmorpg/jouer'
        self.driverDofus = webdriver.Firefox(capabilities=firefox_capabilities)
        try:
            self.driverDofus.get(url)
            self.driverDofus.implicitly_wait(15) # seconds
            self.driverDofus.find_element_by_id('ak_field_4')
        except:
            print('Unable to load www.dofus.com')
            self.driverDofus.quit()
            return False
        return True
        
    def submitForm(self, mail):
        login = 'mc' + random_alphaNumeric_string(6, 3) + 'l'
        password = 'mc' + random_alphaNumeric_string(6, 3) + 'p'
        self.driverDofus.find_element_by_id('userlogin').send_keys(login)
        self.driverDofus.find_element_by_id('user_password').send_keys(password)
        self.driverDofus.find_element_by_id('user_password_confirm').send_keys(password)
        self.driverDofus.find_element_by_id('user_mail').send_keys(mail)
        Select(self.driverDofus.find_element_by_id('ak_field_1')).select_by_value(str(random.randint(1, 31)))
        Select(self.driverDofus.find_element_by_id('ak_field_2')).select_by_value(str(random.randint(1, 12)))
        Select(self.driverDofus.find_element_by_id('ak_field_3')).select_by_value(str(random.randint(1970, 2000)))
        self.driverDofus.find_element_by_id('ak_field_4').click()
        try:
            WebDriverWait(self.driverDofus, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "ak-title")))
        except:
            print('Registration failed')
            self.driverDofus.quit()
            return None
        creds = login + ':' + password
        print('Account created: ' + creds)
        with open('accounts.txt', 'a') as file:
            file.write(creds)
        return creds
    
    def setPseudo(self, url):
        nickname = 'mc' + random_alphaNumeric_string(6, 3) + 'n'
        self.driverDofus.get(url)
        self.driverDofus.implicitly_wait(5) # seconds
        self.driverDofus.get('https://www.dofus.com/fr/')
        WebDriverWait(self.driverDofus, 5).until(EC.presence_of_element_located((By.XPATH, '//a[@class="login ak-modal-trigger"]')))
        self.driverDofus.find_element_by_xpath('//a[@class="login ak-modal-trigger"]').click()
        self.driverDofus.find_element_by_id('usernickname').send_keys(nickname)
        self.driverDofus.find_element_by_xpath('//a[@class="btn btn-primary ak-btn-big"]').click()
        print('Pseudo set: ' + nickname)

    def runTempmail(self):
        url = 'https://temp-mail.org/fr'
        # url = 'file:///home/takoo/ongoing/dofus/account_creator/ex.html'
        self.driverTempmail = webdriver.Firefox()
        self.driverTempmail.get(url)
    
    def getConfirmationMail(self):
        xpath_mail = '//ul/li[3]/div[2]/span/a'
        WebDriverWait(self.driverTempmail, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_mail)))
        self.driverTempmail.find_element_by_xpath(xpath_mail).click()
        xpath_btn = '//tbody/tr/td/table/tbody/tr/td/a'
        WebDriverWait(self.driverTempmail, 10).until(EC.element_to_be_clickable((By.XPATH, xpath_btn)))
        url = self.driverTempmail.find_element_by_xpath(xpath_btn).get_attribute('href')
        print('Confirmation url: ' + url)
        return url
    
    def getMailAdress(self):
        if self.driverTempmail is None : self.runTempmail()
        if self.waitElement('click-to-copy', 10) is False : return None
        self.driverTempmail.find_element_by_xpath("//button[@id='click-to-copy']").click()
        mail = pyperclip.paste()
        print('Mail: ' + mail)
        return mail

    def waitElement(self, element, timeout):
        try:
            WebDriverWait(self.driverTempmail, timeout).until(
                EC.element_to_be_clickable((By.ID, "click-to-copy"))
            )
        except:
            print('TimeoutException, unable to find element: ' + element)
            return False
        return True
        
    def __init__(self):
        super().__init__()
