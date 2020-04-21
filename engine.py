import sys
from src import proxy, dofus, tempmail, misc

class Engine:
    def __init__(self):
        self.tempmail = tempmail.Tempmail()
        self.dofus = dofus.Dofus()
        
    def saveAccount(self, account):
        misc.sPrint('account \'' + account + '\' created')
        with open('accounts.txt', 'a') as file:
            file.write(account + '\n')
    
    def createAccount(self, proxy = None):
        if self.dofus.start(proxy) is None : return None
        email = self.tempmail.getEmailAdress()
        if email is None : return None
        account = self.dofus.register(email)
        if account is None : return None
        url = self.tempmail.getConfirmationEmail()
        if url is None : return None
        if self.dofus.chooseNickname(url) is None : return None
        return account

    def generator(self):
        success = 0
        self.tempmail.start()
        while True:
            account = self.createAccount()
            if account is None : break        
            self.dofus.closeBrowser()
            if account is not None:
                self.saveAccount(account)
                success += 1
                if success == 4 : break
                self.tempmail.deleteEmail()
        self.tempmail.closeBrowser()
        
    def generatorLocalProxy(self, filename):
        self.tempmail.start()
        for myProxy in proxy.getLocalProxy(filename):
            print('Trying with ' + myProxy)
            account = self.createAccount(myProxy)
            self.dofus.closeBrowser()
            while account is not None:
                self.saveAccount(account)
                self.tempmail.deleteEmail()
                print('Keep trying with ' + myProxy)
                account = None
                account = self.createAccount(myProxy)
                self.dofus.closeBrowser()
        self.tempmail.closeBrowser()

    def generatorOnlineProxy(self):
        self.tempmail.start()
        while True:
            myProxy = None
            while myProxy is None:
                myProxy = proxy.getOnlineProxy()
            print('Trying with ' + myProxy)
            account = self.createAccount(myProxy)
            self.dofus.closeBrowser()
            while account is not None:
                self.saveAccount(account)
                self.tempmail.deleteEmail()
                print('Keep trying with ' + myProxy)
                account = None
                account = self.createAccount(myProxy)
                self.dofus.closeBrowser()
        self.tempmail.closeBrowser()

if __name__ == "__main__":
    for i, v in enumerate(sys.argv):
        if ('--local-proxy' == v or '-l' == v) and len(sys.argv) > i + 1:
            if misc.isFileExist(sys.argv[i + 1]):
                Engine().generatorLocalProxy(sys.argv[2])
                exit(0)
        if '--online-proxy' == v or '-o' == v:
            Engine().generatorOnlineProxy()
            exit(0)
    Engine().generator()
    exit(0)