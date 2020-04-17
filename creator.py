import sys
import time
from lxml import html
import requests

class Ressource:
    id = None
    name = None
    img = None
    def __init__(self, id, name, img):
        self.id = id
        self.name = name
        self.img = img

    def write(self, file):
        file.writerow([str(self.id), self.name])

    def saveImg(self):
        img_data = requests.get(self.img).content
        with open("img/" + str(self.id) + '.png', 'wb') as handler:
            handler.write(img_data)

    def dump(self):
        print(str(self.id) + ':' + self.name)

class Scraper:
    start = None
    file = None

    def __init__(self, file, start = 1):
        self.file = file
        self.start = start
        self.scrap()

if __name__ == "__main__":
    filename = 'accounts.txt'
    start = None
    if (len(sys.argv) > 1):
        start = int(sys.argv[1])
    data = []
    with open('items.csv', 'r') as csvfile:
        r = csv.reader(csvfile, encoding='utf-8')
        for row in r:
            data.append(row)
    with open('items.csv', 'w') as csvfile:
        w = csv.writer(csvfile, delimiter=',')
        for row in data:
            w.writerow(row)
        Scraper(w, start)
    exit(0)