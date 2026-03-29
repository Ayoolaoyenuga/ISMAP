import requests
import json
import time

time.sleep(2)
BASE='http://127.0.0.1:5000'
print('Signup ->', end=' ')
r = requests.post(BASE+'/api/register', json={'username':'pytestuser','email':'pytestuser@example.com','password':'pass1234'})
print(r.status_code, r.text)
print('Login ->', end=' ')
r = requests.post(BASE+'/api/login', json={'email':'pytestuser@example.com','password':'pass1234'})
print(r.status_code, r.text)
if r.status_code==200:
    token = r.json().get('token')
    headers={'Authorization':f'Bearer {token}'}
    print('Register domain ->', end=' ')
    r2 = requests.post(BASE+'/api/register/example.com', headers=headers, json={'interval':6})
    print(r2.status_code, r2.text)
    print('Register domain again ->', end=' ')
    r3 = requests.post(BASE+'/api/register/example.com', headers=headers, json={'interval':6})
    print(r3.status_code, r3.text)
else:
    print('Login failed; skipping domain tests')
