import json
import pandas
import requests
from bs4 import BeautifulSoup
# get key from config
import config

def getCLL(ipAddress):
    response = requests.get("http://freegeoip.net/json/"+ipAddress)
    resJ = json.loads(response.text)
    cll=[]
    cll.append(resJ.get("country_code"))
    cll.append(resJ.get("latitude"))
    cll.append(resJ.get("longitude"))

    return cll

def getTimezone(lat,lon):
    venus = config.config['apikey']
    response = requests.get("https://maps.googleapis.com/maps/api/timezone/json?location="+str(lat)+","+str(lon)+"&timestamp=1331161200&key="+venus)
    resJ = json.loads(response.text)
    return resJ.get("timeZoneName")

IPs = []

count = 20161116094830
while(len(IPs) < 300):
    try:
        if count == 0:
            url = "https://en.wikipedia.org/w/index.php?title=Application_programming_interface&action=history"
        else:

            url = "https://en.wikipedia.org/w/index.php?title=Application_programming_interface&dir=prev&offset={}&action=history".format(count)
            count +=1
        r=requests.get(url)
        #soup=BeautifulSoup(r.content,"html.parser")
        soup=BeautifulSoup(r.text,"lxml")
        history=soup.find("ul",{"id":"pagehistory"})
        data = history.find_all("li")

        for items in data:

            try:
                #IP - mw-userlink mw-anonuserlink
                #username - mw-userlink
                IPs.append(items.find("a",{"class","mw-userlink mw-anonuserlink"}).text)
            except:
                print("")

    except:
        break

#print(IPs)
#print(len(IPs))

big_lis=[]
leng= len(IPs)-1
for data in IPs:
    d={}
    if leng >= 0:
        d["IP Address"] = IPs[leng]
        d["country code"]= getCLL(IPs[leng])[0]
        d["latitude"]= getCLL(IPs[leng])[1]
        d["longitude"]= getCLL(IPs[leng])[2]
        d["timeZoneName"] = getTimezone((getCLL(IPs[leng])[1]),(getCLL(IPs[leng])[2]))
    big_lis.append(d)
    leng -=1

df=pandas.DataFrame(big_lis)
df.to_csv("api.csv")
