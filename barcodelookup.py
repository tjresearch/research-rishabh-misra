import requests 
import sys


# productid = sys.argv[1]   => This was my original approach, but I changed it 

def lookup(productid):
    lookupurl = 'https://api.upcdatabase.org/product/'+ productid +'?apikey=4C581A903B39142996356BF57FE06171'

    resp = requests.get(lookupurl)

    if(resp.json()['success']):
        return resp.json()['title']  # Will return the title of the item it finds
    
    return None