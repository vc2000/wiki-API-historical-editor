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


#API wiki - edit history
r=requests.get("https://en.wikipedia.org/w/index.php?title=Application_programming_interface&action=history")
soup=BeautifulSoup(r.text,"lxml")
history=soup.find("ul",{"id":"pagehistory"})
data = history.find_all("li")

lis=[]
for items in data:

    try:
        #IP - mw-userlink mw-anonuserlink
        #username - mw-userlink
        lis.append(items.find("a",{"class","mw-userlink mw-anonuserlink"}).text)
    except:
        print("")
print("IPAddress is :" +lis[0])


print("country code :"+ getCountry(lis[0])[0])
print("latitude :"+ str(getCountry(lis[0])[1]))
print("longitude :"+ str(getCountry(lis[0])[2]))
