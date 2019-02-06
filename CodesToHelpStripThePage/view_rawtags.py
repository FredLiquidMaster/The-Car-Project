import requests
from bs4 import BeautifulSoup as bs

url = "http://www.kijiji.ca/b-autos-camions/grand-montreal/c174l80002"
r = requests.get(url)
soup = bs(r.content,"html.parser")
g_data = soup.find_all("div",{"class": "clearfix"})

conteur =0
for item in g_data[1:2]:
    info = item.find_all("div")
#find the ad id
    adid_ctn = str(info[1])
    print("-------------------------------------------------------------------ad id ------------>")
    print(adid_ctn)
#find the price
    price_ctn = str(info[3].find_all("div",{"class":"price"}))
    print("-------------------------------------------------------------------price ------------>")
    print(price_ctn)
#find the km
    km_ctn = str(info[-1])
    print("-------------------------------------------------------------------km --------------->")
    print(km_ctn)
#find model
    model_ctn = str(info[3].find_all("a",{"class":"title enable-search-navigation-flag "}))
    print("-------------------------------------------------------------------model ------------>")
    print(model_ctn)
#find quand et ou
    quand_ctn = str(info[3].find_all("div",{"class":"location"}))
    print("-------------------------------------------------------------------quand et ou ------>")
    print(quand_ctn)
#conteur plus noyeance
    conteur = conteur+1
    print(str(conteur)+"""
      =========================================================================================
      =========================================================================================""")
    