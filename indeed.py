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
    result =  requests.get("https://fr.indeed.com/jobs?q=stage+"+domaine+"&l="+location)
    src = result.content
    soup = BeautifulSoup (src.decode('utf-8', 'ignore'))
    titres = soup.findAll("h2",{"class":"title"})
    bodies = soup.findAll("div",{"class":"summary"})
    for i in range(len(titres)):
        try:
            titre = titres[i].text
            body = bodies[i].text
            lien = "https://fr.indeed.com" + titres[i].findAll("a")[0]['href']
            mycursor = db.cursor()
            sql = "INSERT INTO temp (site,titre,body,lien,domaine) VALUES (%s, %s, %s, %s, %s)"
            val = ("fr.indeed.com", titre, body, lien, domaine)
            mycursor.execute(sql, val)
            db.commit()
        except Exception as e:
            print(str(e))
    
    

