import json
import requests
from bs4 import BeautifulSoup

def getCountry(ipAddress):
    response = requests.get("http://freegeoip.net/json/"+ipAddress)
    resJ = json.loads(response.text)
    cll=[]
    cll.append(resJ.get("country_code"))
    cll.append(resJ.get("latitude"))
    cll.append(resJ.get("longitude"))
    return cll

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

print(IPs)
print(len(IPs))


leng= len(IPs)-1

for data in IPs:
    if leng >= 0:
        print("country code :"+ getCountry(IPs[leng])[0])
        print("latitude :"+ str(getCountry(IPs[leng])[1]))
        print("longitude :"+ str(getCountry(IPs[leng])[2]))

    leng -=1
