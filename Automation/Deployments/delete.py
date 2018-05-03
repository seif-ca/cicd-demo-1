import requests
import json

DB_USER = 'pete@tamisin.com'
DB_PASS = 'ApacheSpark1$'
SHARDNAME = 'tamisin-sandbox'

LOGIN_ENDPOINT = 'https://%s.cloud.databricks.com/j_security_check' % SHARDNAME
CSRF_ENDPOINT = 'https://%s.cloud.databricks.com/config' % SHARDNAME

USERS_LIST_ENDPOINT = 'https://%s.cloud.databricks.com/accounts' % SHARDNAME

### 1. 'Login' to Databricks using/start a session
session = requests.Session()
login_result = session.post(LOGIN_ENDPOINT, data={'j_username':DB_USER,'j_password':DB_PASS})

### 2. Grab CRSF token required for future requests & update the headers for future requests as part of this session
csrf_token = session.get(CSRF_ENDPOINT).json()['csrfToken']
session.headers.update({'X-CSRF-Token':csrf_token})

list_users_result = session.get(USERS_LIST_ENDPOINT, auth=(DB_USER,DB_PASS))


userjson = list_users_result.text
users = json.loads(userjson)
for user in users:
    uid = user.get('id','')
    username = user.get('username','')
    if 'peter' in username:
        print("deleting user:" + username + ":" + str(uid))
        #del_users_result = session.delete(USERS_LIST_ENDPOINT + '/' + str(uid), auth=(DB_USER,DB_PASS))

        print('deleting user path: /Users/' + username)
        values = {'path': '/Users/' + username, 'recursive': 'true'}
        print(values)
        resp = requests.post('https://' + SHARDNAME + '.cloud.databricks.com/api/2.0/workspace/delete',
                             data=values, auth=(DB_USER, DB_PASS))
        print(resp.text)