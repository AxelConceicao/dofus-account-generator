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
            # else:
            #     break
        self.tempmail.closeBrowser()
        
    def generatorProxylist(self, filename):
        self.tempmail.start()
        for myProxy in proxy.getLocalProxy(filename):
            print('Trying with ' + myProxy)
            if myProxy is not None:
                account = self.createAccount(myProxy)
                self.dofus.closeBrowser()
                if account is not None:
                    self.saveAccount(account)
                    self.tempmail.deleteEmail()
                    print('Keep trying with ' + myProxy)
                    self.runWithProxy(myProxy)
        self.tempmail.closeBrowser()

if __name__ == "__main__":
    if '--proxy' in sys.argv and len(sys.argv) >= 3:
        Engine().generatorProxylist(sys.argv[2])
    else:
        Engine().generator()
    exit(0)