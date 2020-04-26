import sys
import json
import time
import random
import platform
import pyperclip
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from src import misc

class Browser:
    def __init__(self):
        self.driver = None
        
    def handleFirefoxCapabilities(self, strategy, proxy):
        capabilities = webdriver.DesiredCapabilities.FIREFOX
        capabilities["pageLoadStrategy"] = strategy
        if proxy is not None:
            capabilities['proxy'] = {
                "proxyType": "MANUAL",
                "httpProxy": proxy,
                "ftpProxy": proxy,
                "sslProxy": proxy
            }
        return capabilities

    def startFirefoxBrowser(self, strategy, headless, proxy = None):
        try:
            opt = webdriver.FirefoxOptions()
            opt.headless = headless
            firefox_capabilities = self.handleFirefoxCapabilities(strategy, proxy)
            if platform.architecture()[0] == '32bit':
                bin_path = './geckodriver-linux32'
            else:
                bin_path = './geckodriver-linux64'
            self.driver = webdriver.Firefox(executable_path=bin_path, capabilities=firefox_capabilities, firefox_options=opt)
        except Exception as e:
            print(e, end='')
            misc.ePrint('failed to launch Firefox Browser')
            sys.exit(1)
            
    def closeBrowser(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(e, end='')
            pass
        
    def navigate(self, url, proxy = None):
        try:
            self.driver.get(url)
        except Exception as e:
            print(e, end='')
            misc.ePrint('failed to navigate to \'' + url + '\'')
            return False
        else:
            return True
            
    def getCurrentUrl(self):
        return self.driver.current_url

    def waitElement(self, element, timeout):
        wait = WebDriverWait(self.driver, timeout)
        try:
            element = wait.until(element)
        except Exception as e:
            print(e, end='')
            misc.ePrint('timeout exception')
            return None
        else:
            return element
        
    def executeScript(self, element, timeout):
        element = self.waitElement(element, timeout)
        self.driver.execute_script("arguments[0].click();", element)
