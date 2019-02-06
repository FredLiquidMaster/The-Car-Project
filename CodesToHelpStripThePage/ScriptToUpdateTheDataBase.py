import requests,os,pprint,re,shelve
from bs4 import BeautifulSoup as bs
print('1')

Working_Directory = "C:\\Users\\baggyy\\Documents\\programes\\Car_data_project\\scraper\\data_dict_WD\\"

url = "http://www.kijiji.ca/b-autos-camions/grand-montreal/c174l80002"
makes_ctn_list = str(bs(requests.get(url).content,"html.parser").find_all("ul",{"data-menuid":"carmake_s"})).split("</li>")
print('2')
makes_list = []
for things in makes_ctn_list:
    makes_list.append(things[things.find("     "):things.find("</a>")].strip(" ").lower())
makes_list = makes_list[:-3]
print(makes_list)

print('3')
# upload de la list dans la variable
adid_list = []

# upload de la liste dans la variable
# import data_dict
# data_dict = data_dict.data_dict
data_dict = {}

def url_maker(car_make):
    base_url = "http://www.kijiji.ca/b-autos-camions/grand-montreal/"
    end_url = "/c174l80002a54?ad=offering"
    return base_url+car_make+end_url

def url_maker_v2(car_make,model,page):
    base_url = "http://www.kijiji.ca/b-autos-camions/grand-montreal/"
    end_url = "/c174l80002a54a1000054?ad=offering"
    if page == 0:
        return base_url+car_make+"-"+model+end_url
    return base_url+car_make+"-"+model+"/page-"+str(page+1)+end_url

print('4')
for i in range(len(makes_list[1:2])):# loop des makes -> [1:]
    make = makes_list[i].strip(" ").strip("'").replace(" ","+")
    url = url_maker(make)
    g_data = str(bs(requests.get(url).content,"html.parser").find_all("ul",{"data-menuid":"carmodel_s"})).split("data-id")
#    model_dict = {}
# loop des models -> return url
    for model_ctn in g_data[1:6]: # -> [1:]
        model = model_ctn[2:model_ctn.find("href")-2].strip(" ")
        nb_de_page = int(model_ctn[model_ctn.find(")</li>")-6:model_ctn.find(")</li>")].strip(" ").strip("(").replace("xa",""))//20+1
        url_list = []
        for page in range(nb_de_page):
            url = url_maker_v2(make,model,page)
# lancement du sraper pour url 
            print("get<"+make+" "+model+"> page("+str(page)+")")
            g_data = bs(requests.get(url).content,"html.parser").find_all("div",{"class": "clearfix"})

            for item in g_data[1:]:
                info_dict = {}
                info = item.find_all("div")
# stripage des infos
        #find the ad id
                adid_ctn = str(info[1])
                adid_index = adid_ctn.find("data-adid=")
                adid = adid_ctn[adid_index+11:adid_index+21]
        # see if the ad already in list
                state = ""
                if adid in adid_list:
                    state = "old"
                else:
                    state = "new"
                    adid_list.append(adid)

        #find the price
                price_ctn = str(info[3].find_all("div",{"class":"price"}))
                price_index = price_ctn.find(",")
                price_strip = price_ctn[price_index-15:price_index+2].strip(" ").split("\\xa0")
                price = ("").join(price_strip)

        #find the km
                km_ctn = str(info[-1])
                km_index = km_ctn.find("km")
                km = km_ctn[km_index-10:km_index].strip(" ")

        #find year
                year_ctn = str(info[3].find_all("a",{"class":"title enable-search-navigation-flag "}))
                year_regex = re.compile(r"\d{4}")
                year_result_list = year_regex.findall(year_ctn[year_ctn.find(">")+3:-5].strip(" "))
                year = ""
                for result in year_result_list:
                    if 1900 < int(result) < 2020:
                        year = result

        #find quand
                quand_ctn = str(info[3].find_all("div",{"class":"location"}))
                quand_index1 = quand_ctn.find("posted")
                quand_index2 = quand_ctn.find("</span>")
                quand = quand_ctn[quand_index1+8:quand_index2]

        #find location
                location_index2 = quand_ctn.find("<span")
                location_index1 = quand_ctn.find("location")
                location = quand_ctn[location_index1+13:location_index2].strip(" ")

# save the info in data_dict
                if state == "new":
                    info_dict.setdefault("adid",adid)
                    info_dict.setdefault("make",make)
                    info_dict.setdefault("model",model)
                    info_dict.setdefault("price",price)
                    info_dict.setdefault("km",km)
                    info_dict.setdefault("year",year)
                    info_dict.setdefault("quand",quand)
                    info_dict.setdefault("location",location)
                    info_dict.setdefault("state",state)
                    data_dict.setdefault(adid,info_dict)

#save la new adid_list


#save data_dict.py
print(data_dict)
print("data_dict <save done>")

print("updater_data_dict <end>")



