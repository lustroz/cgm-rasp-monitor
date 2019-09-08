import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import simplejson as json
import logging
import setting
import os

logger = logging.getLogger('cgm')

API_HOST = ''
headers = {'Authorization': 'Bearer '}

def req(path, query, method, data={}):
    config = setting.getCurrent()
    
    API_HOST = config['ns_addr']

    url = API_HOST + path

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        if method == 'GET':
            return session.get(url, headers=headers)
        else:
            return session.post(url, headers=headers, data=data)
    except:
        os.system('shutdown -r')

def getEntries(state, db):
    try:
        resp = req('/api/v1/entries.json', '', 'GET')
        if resp is None:
            return

        parsed = json.loads(resp.text)
        for entry in parsed:
            if entry['type'] == 'sgv':
                db.insertEntry('nightscout', entry['date'], entry['sgv'], entry['direction'])

        state.setState(state.DisplayValue)
    
    except Exception as e:
        logger.exception('request crashed. Error: %s', e)    

        if API_HOST == '':
            state.setState(state.InvalidParam)

    

    
    
