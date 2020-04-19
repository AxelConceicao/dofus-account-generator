import sys
import requests
from src import proxy, browser

class Engine:
    browser = None
    file = ''
    nb = 0

    def __init__(self, file = 'accounts.txt', nb = 1):
        self.file = file
        self.nb = nb
        self.browser = browser.Browser()

    def run(self):
        self.browser.runTempmail()
        while self.nb != 0:
            self.browser.runDofus(None)
            creds = self.browser.submitForm(self.browser.getMailAdress())
            if creds is not None:
                url = self.browser.getConfirmationMail()
                self.browser.setPseudo(url)
                self.nb = self.nb - 1
        return
        self.browser.runTempmail()
        while self.nb != 0:
            myProxy = proxy.getOnlineProxy()
            if myProxy and self.browser.runDofus(myProxy):
                creds = self.browser.submitForm(self.browser.getMailAdress())
                if creds is not None:
                    url = self.browser.getConfirmationMail()
                    self.browser.setPseudo(url)
                    self.nb = self.nb - 1

if __name__ == "__main__":
    filename = None
    nb = None
    # if (len(sys.argv) != 3):
    #     print('python3 engine.py [file] [nb]')
    #     exit(1)
    # filename = sys.argv[1]
    # nb = sys.argv[2]
    Engine().run()
    # with open(filename, 'a') as w:
    exit(0)