
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re

#KOD ZA MAIN STRANICU(prva strana)
from requests.exceptions import MissingSchema

URL_MAIN = "https://www.kupujemprodajem.com/search.php?action=list&data%5Bpage%5D=1&data%5Bprev_keywords%5D=thinkpad&data%5Border%5D=relevance&submit%5Bsearch%5D=Tra%C5%BEi&dummy=name&data%5Bkeywords%5D=thinkpad&data%5Bprice_from%5D=6000&data%5Bprice_to%5D=18000&data%5Bcurrency%5D=rsd"
URL = ""
page_main = requests.get(URL_MAIN)
soup_main = BeautifulSoup(page_main.content, 'html.parser')

linkovi = []

#racunanje broja stranica
brStranica = soup_main.find_all("a", title=re.compile("Strana.*"))
print(brStranica[len(brStranica) - 2].text)

nizOglasa = soup_main.find_all(id=re.compile("adDescription.*"))
for oglas in nizOglasa:
    linkovi.extend(oglas.find("a", class_="adName"))
#TODO: dodati i filter za X220 i X200, takodje probati i pretragu samog oglasa i trazenje kljuca na samoj stranici oglasa
for link in linkovi:
    x = re.search("^.*X201.*$", link.text.strip())
    if x:
        print(link.text)
        print("https://www.kupujemprodajem.com" + link.parent["href"])

linkovi = []
#pretraga ostalih stranica
URL = "https://www.kupujemprodajem.com/search.php?action=list&data%5Baction%5D=list&data%5Bsubmit%5D%5Bsearch%5D=Tra%C5%BEi&data%5Bdummy%5D=name&data%5Bpage%5D=2&data%5Bprev_keywords%5D=thinkpad&data%5Border%5D=relevance&data%5Bkeywords%5D=thinkpad&data%5Bprice_from%5D=6000&data%5Bprice_to%5D=18000&data%5Bcurrency%5D=rsd&data%5Blist_type%5D=search"
for i in range(2, int(brStranica[len(brStranica) - 2].text) + 1):
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        nizOglasa = soup.find_all(id=re.compile("adDescription.*"))
        for oglas in nizOglasa:
            linkovi.extend(oglas.find("a", class_="adName"))
        # TODO: dodati i filter za X220 i X200, takodje probati i pretragu samog oglasa i trazenje kljuca na samoj stranici oglasa
        for link in linkovi:
            x = re.search("^.*X201.*$", link.text.strip())
            if x:
                print(link.text)
                print("https://www.kupujemprodajem.com" + link.parent["href"])
        linkovi = []
        URL = "https://www.kupujemprodajem.com/search.php?action=list&data%5Baction%5D=list&data%5Bsubmit%5D%5Bsearch%5D=Tra%C5%BEi&data%5Bdummy%5D=name&data%5Bpage%5D=" + str(i) + "&data%5Bprev_keywords%5D=thinkpad&data%5Border%5D=relevance&data%5Bkeywords%5D=thinkpad&data%5Bprice_from%5D=6000&data%5Bprice_to%5D=18000&data%5Bcurrency%5D=rsd&data%5Blist_type%5D=search"

    except MissingSchema:
        print("poslednja stranica")
        break
