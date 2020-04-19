import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from src import browser, misc

class Tempmail(browser.Browser):
    def __init__(self):
        super().__init__()
        
    def start(self):
        self.startFirefoxBrowser('normal', False)
        self.navigate('https://temp-mail.org/fr')
        
    def getEmailAdress(self):
        self.waitElement(EC.element_to_be_clickable((By.ID, "click-to-copy")), 10).click()
        mail = pyperclip.paste()
        print('Email address: ' + mail)
        return mail
    
    def getConfirmationEmail(self):
        self.waitElement(EC.element_to_be_clickable((By.XPATH, '//ul/li[3]/div[2]/span/a')), 30).click()
        print('Confirmation email received')
        url = self.waitElement(EC.element_to_be_clickable((By.XPATH, '//tbody/tr/td/table/tbody/tr/td/a')), 15).get_attribute('href')
        print('Confirmation url: ' + url)
        return url
    
    def deleteEmail(self):
        self.waitElement(EC.element_to_be_clickable((By.ID, "click-to-delete")), 10).click()