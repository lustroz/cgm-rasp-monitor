import requests
import simplejson as json
import logging

logger = logging.getLogger('cgm')

API_HOST = 'http://ns.dolucy.com:9237'
headers = {'Authorization': 'Bearer '}

def req(path, query, method, data={}):
    url = API_HOST + path
    # print('HTTP Method: %s' % method)
    # print('Request URL: %s' % url)
    # print('Headers: %s' % headers)
    # print('QueryString: %s' % query)

    if method == 'GET':
        return requests.get(url, headers=headers)
    else:
        return requests.post(url, headers=headers, data=data)

def getEntries(db):
    resp = req('/api/v1/entries.json', '', 'GET')
    parsed = json.loads(resp.text)
    # logger.info(json.dumps(parsed, indent=4, sort_keys=True))
    for entry in parsed:
        if entry['type'] == 'sgv':
            db.insertEntry('nightscout', entry['date'], entry['sgv'], entry['direction'])
    
