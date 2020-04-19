import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from src import misc, browser

class Dofus(browser.Browser):
    def __init__(self):
        super().__init__()
        
    def start(self, proxy):
        self.startFirefoxBrowser('none', False, proxy)
        if not self.navigate('https://www.dofus.com/fr/mmorpg/jouer', proxy):
            return None
        else:
            time.sleep(3)
            return 'OK'
        
    def register(self, mail):
        login = 'mc' + misc.random_alphaNumeric_string(6, 3) + 'l'
        password = 'mc' + misc.random_alphaNumeric_string(6, 3) + 'p'
        
        if self.waitElement(EC.element_to_be_clickable((By.ID, "ak_field_4")), 15) is None:
            misc.ePrint('cannot find registration form')
            return None
        
        self.waitElement(EC.visibility_of_element_located((By.ID, "userlogin")), 1).send_keys(login)
        self.waitElement(EC.visibility_of_element_located((By.ID, "user_password")), 1).send_keys(password)
        self.waitElement(EC.visibility_of_element_located((By.ID, "user_password_confirm")), 1).send_keys(password)
        self.waitElement(EC.visibility_of_element_located((By.ID, "user_mail")), 1).send_keys(mail)
        Select(self.waitElement(EC.visibility_of_element_located((By.ID, "ak_field_1")), 1)).select_by_value(str(random.randint(1, 31)))
        Select(self.waitElement(EC.visibility_of_element_located((By.ID, "ak_field_2")), 1)).select_by_value(str(random.randint(1, 12)))
        Select(self.waitElement(EC.visibility_of_element_located((By.ID, "ak_field_3")), 1)).select_by_value(str(random.randint(1970, 2000)))
        self.waitElement(EC.element_to_be_clickable((By.ID, "ak_field_4")), 1).click()
        
        if self.waitElement(EC.visibility_of_element_located((By.CLASS_NAME, "ak-title")), 120):
            creds = login + ':' + password
            print('Account created: ' + creds)
            return creds
        else:
            misc.ePrint('registration failed')
            return None
        
    def chooseNickname(self, url):
        nickname = 'mc' + misc.random_alphaNumeric_string(6, 3) + 'n'
        
        self.navigate(url)
        if self.waitElement(EC.element_to_be_clickable((By.XPATH, '//div[@class="ak-game-download"]/a')), 10):
            print('Email confirmed')
        else:
            misc.ePrint('invalid confirmation email')
            return None
        if not self.navigate('https://www.dofus.com/fr/'):
            return None
        time.sleep(3)
        # self.executeScript(EC.element_to_be_clickable((By.XPATH, '//a[@class="ak-close"]')), 10) # close cookies
        self.executeScript(EC.element_to_be_clickable((By.XPATH, '//a[@class="login ak-modal-trigger"]')), 10) # open nickname ui
        time.sleep(1)
        self.waitElement(EC.visibility_of_element_located((By.ID, 'usernickname')), 10).send_keys(nickname) # write nickname
        time.sleep(1)
        self.waitElement(EC.element_to_be_clickable((By.XPATH, '//input[@class="btn btn-primary ak-btn-big"]')), 10).click() # click confirm btn
        time.sleep(1)

        print('Nickname set: ' + nickname)
        return nickname