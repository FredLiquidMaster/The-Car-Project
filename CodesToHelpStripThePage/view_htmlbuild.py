import requests
from bs4 import BeautifulSoup as bs

url = "http://www.kijiji.ca/b-autos-camions/grand-montreal/c174l80002"
r = requests.get(url)

soup = bs(r.content,"html.parser")

g_data = soup.find_all("div",{"class": "clearfix"})

conteur =0
for item in g_data[1:2]:
    info = item.find_all("div")
    conteur2 = 0
    for things in info:
        print(things)
        conteur2 = conteur2 +1
        print(str(conteur2)+"-----------------------------------------------")

    conteur = conteur+1
    print(str(conteur)+"=========================================================================================")
    