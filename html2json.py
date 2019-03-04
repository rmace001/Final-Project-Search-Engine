import string
import operator
import json
import certifi
import urllib3
import requests





http = urllib3.PoolManager( cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

url = 'https://www.ucr.edu/'
uniqueID = '1'
finalDate = '3-4-19'
htmlContent = http.request('GET', url)
#htmlContent = requests.get(url)
ContentUrl = json.dumps({
        'url' : str(url),
        'uid' : str(uniqueID),
        'page_content' : str(htmlContent.data),
        'date' : str(finalDate)
        })
print(ContentUrl)
