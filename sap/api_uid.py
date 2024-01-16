import requests
import json


base_url = "https://api.c9t6aobb6f-condorsup1-p1-public.model-t.cc.commerce.ondemand.com"

endpoint_token = "/authorizationserver/oauth/token"
headers_token = {
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=58979B1E78CD226AFBAD5885C3074401.api-795bb9f7cc-nz9ln; ROUTE=.api-795bb9f7cc-nz9ln'
}
params_token = {
    'client_id': 'api-order',
    'client_secret': 'order@123',
    'grant_type': 'client_credentials',
    'scope': 'basic'
}
response_token = requests.post(base_url + endpoint_token, headers=headers_token, params=params_token)
token_data = response_token.json()

if 'access_token' in token_data:
    access_token = token_data['access_token']

    
    uid = "024030029"
    endpoint_orders_by_user = f"/occ/v2/condor/users/{uid}/orders"
    params_orders_by_user = {
        'currentPage': '0',
        'fields': 'DEFAULT',
        'pageSize': '20'
    }


    headers = {
        'accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
        'Cookie': 'ROUTE=.api-795bb9f7cc-nz9ln'
    }

    response = requests.get(base_url + endpoint_orders_by_user, headers=headers, params=params_orders_by_user)

    if response.status_code == 200:
        orders_data = response.json()
        print(json.dumps(orders_data, indent=4))
    else:
        print("Erro ao obter os pedidos do cliente.")
        print(response.text)
else:
    print("Erro ao obter o token de acesso.")
    print(token_data)