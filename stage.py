import MySQLdb
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="khalil",         # your username
                     passwd="123456",  # your password
                     db="stage",
                     charset='utf8')        # name of the data base

domaines = [
        'agriculture','ecologie','sciences veterinaires','architecture','artisanat','arts plastiques','audiovisuel','infographie','histoire des arts','assurances','bourse','immobilier','commerce international','e-commerce','management','marketing','communication','journalisme','mediation culturelle','publicite','droit','science politique','science economique','administration','audit','comptabilite','ressources humaines','hotellerie','tourisme','developpement','intelligence artificielle','reseaux','sante','nutrition','genie civil','electronique','biologie','logistique'
]

location = 'france'

for domaine in domaines:
    result =  requests.get("https://www.stage.fr/jobs/?q="+domaine+"&l="+location+"&p=3")
    src = result.content

    soup = BeautifulSoup (src.decode('utf-8', 'ignore'))
    articles = soup.findAll("article")

    for article in articles:
        try:
            titre = article.findAll("a",{"class":"link"})[0].text
            body = article.findAll("div",{"class":"listing-item__desc hidden-sm hidden-xs"})[0].text
            lien = article.findAll("a",{"class":"link"})[0]['href']


            mycursor = db.cursor()
            sql = "INSERT INTO temp (site,titre,body,lien,domaine) VALUES (%s, %s, %s, %s, %s)"
            val = ("www.stage.fr", titre, body, lien, domaine)
            mycursor.execute(sql, val)
            db.commit()
        except Exception as e:
            print(str(e))

        



"""
driver = webdriver.Firefox()

chromeDriver= "/home/krypton/Downloads/chromedriver_linux64"

search = soup.find("div", {"id": "s0-26_2-9-0-1[1]-0-0-xCarousel-x-carousel-items"}).find("ul").findAll("li")
for elt in search:
    print(elt.find("img")['data-src'])
"""

"""
headers = {
    'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36',
}

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/local/bin/chromedriver',chrome_options=chrome_options)

driver.get('https://www.stage.fr/jobs/?q=developpement&l=France')
"""

