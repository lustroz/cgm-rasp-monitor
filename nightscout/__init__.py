import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
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

    try:
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        if method == 'GET':
            return session.get(url, headers=headers)
        else:
            return session.post(url, headers=headers, data=data)
    
    except Exception as e:
        logger.exception('request crashed. Error: %s', e)

def getEntries(state, db):
    resp = req('/api/v1/entries.json', '', 'GET')
    if resp is None:
        return

    parsed = json.loads(resp.text)
    # logger.info(json.dumps(parsed, indent=4, sort_keys=True))
    for entry in parsed:
        if entry['type'] == 'sgv':
            db.insertEntry('nightscout', entry['date'], entry['sgv'], entry['direction'])
    
