import requests
import simplejson as json
import database

API_HOST = 'http://ns.dolucy.com:9237'
headers = {'Authorization': 'Bearer '}

def req(path, query, method, data={}):
    url = API_HOST + path
    print('HTTP Method: %s' % method)
    print('Request URL: %s' % url)
    print('Headers: %s' % headers)
    print('QueryString: %s' % query)

    if method == 'GET':
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, headers=headers, data=data)

def getEntries():
    resp = req('/api/v1/entries.json', '', 'GET')
    parsed = json.loads(resp.text)
    #print(json.dumps(parsed, indent=4, sort_keys=True))
    for entry in parsed:
        database.insertEntry('nightscout', entry['date'], entry['sgv'], entry['direction'])
    
