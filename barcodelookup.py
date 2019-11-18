import requests 

productid = "044000032029"

lookupurl = 'https://api.upcdatabase.org/product/'+ productid +'?apikey=4C581A903B39142996356BF57FE06171'

resp = requests.get(lookupurl)

print(resp.json())