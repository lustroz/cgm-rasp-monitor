import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import simplejson as json
import logging
import setting
import re

logger = logging.getLogger('cgm')

API_HOST = 'https://shareous1.dexcom.com'
headers = { 'User-Agent': 'Dexcom Share/3.0.2.11 CFNetwork/711.2.23 Darwin/14.0.0', 
            'Content-Type': 'application/json', 
            'Accept': 'application/json' }

direction = {
    0: 'None',
    1: 'DoubleUp',
    2: 'SingleUp',
    3: 'FortyFiveUp',
    4: 'Flat',
    5: 'FortyFiveDown',
    6: 'SingleDown',
    7: 'DoubleDown'
}

def convertEntry(entry):
    regex = re.compile('\((.*)\)')
    match = regex.search(entry['WT'])    
    date = match.group(1)

    dirStr = direction.get(entry['Trend'])
    if dirStr == None:
        dirStr = 'None'

    return {
        'date': date,
        'sgv': entry['Value'],
        'direction': dirStr
    }

def req(path, query, method, data={}):
    url = API_HOST + path
    if len(query) > 0:
        url += '?' + query

    # logger.info(url)

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    if method == 'GET':
        return session.get(url, headers=headers)
    else:
        return session.post(url, headers=headers, data=data)

def getEntries(state, db):
    config = setting.getCurrent()
    try:
        param = {
            'applicationId': 'd89443d2-327c-4a6f-89e5-496bbb0317db',
            'accountName': config['ds_user'],
            'password': config['ds_pass']   
        }

        resp = req('/ShareWebServices/Services/General/LoginPublisherAccountByName', '', 'POST', json.dumps(param))
        if resp is None:
            return
        # logger.info(resp.text)

        query = 'sessionID={0}&minutes=1440&maxCount=1'.format(resp.text[1:-1])

        resp = req('/ShareWebServices/Services/Publisher/ReadPublisherLatestGlucoseValues', query, 'POST')
        if resp is None:
            return
        # logger.info(resp.text)
        parsed = json.loads(resp.text)
        for e in parsed:
            entry = convertEntry(e)
            db.insertEntry('dexcomshare', entry['date'], entry['sgv'], entry['direction'])  

        state.setState(state.DisplayValue)              
    
    except Exception as e:
        logger.exception('request crashed. Error: %s', e)    

        if config['ds_user'] == '' or config['ds_pass'] == '':
            state.setState(state.InvalidParam)
       

    

    
    
