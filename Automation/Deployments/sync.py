import json
import httplib2
import requests

h = httplib2.Http(".cache")

h.add_credentials('pete@tamisin.com', 'Ranma120866!') # Basic authentication

resp, content = h.request("https://tamisin-sandbox.cloud.databricks.com/api/2.0/workspace/list?path=/DEVELOP/Spark-ILT/Python", "GET")
dresp = json.loads(content.decode())

objects = dresp['objects']
for o in objects:
    if (o['object_type']) == 'NOTEBOOK':
        print('Beginning file download of' + o['path'])

        url = 'https://tamisin-sandbox.cloud.databricks.com/api/2.0/workspace/export?path=/DEVELOP&format=DBC&direct_download=true'
r = requests.get(url)

with open('/Users/scott/Downloads/cat3.jpg', 'wb') as f:
    f.write(r.content)

# Retrieve HTTP meta-data
print(r.status_code)
print(r.headers['content-type'])
print(r.encoding)
