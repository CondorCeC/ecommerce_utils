import requests
import json

base_url = "https://api.c9t6aobb6f-condorsup1-p1-public.model-t.cc.commerce.ondemand.com"


endpoint_token = "/authorizationserver/oauth/token"
endpoint_order = "/occ/v2/condor/orders/"

headers = {
    'Content-Type': 'application/json',
    'Cookie': 'JSESSIONID=58979B1E78CD226AFBAD5885C3074401.api-795bb9f7cc-nz9ln; ROUTE=.api-795bb9f7cc-nz9ln'
}

params_token = {
    'client_id': 'api-order',
    'client_secret': 'order@123',
    'grant_type': 'client_credentials',
    'scope': 'basic'
}


response_token = requests.post(base_url + endpoint_token, headers=headers, params=params_token)
print(response_token.status_code)
print(response_token.text)

token_data = response_token.json()

if 'access_token' in token_data:
    access_token = token_data['access_token']
    
    headers['Authorization'] = f'Bearer {access_token}'
    
    order_code = '00911262'
    
    response_order = requests.get(base_url + endpoint_order + f"{order_code}?fields=DEFAULT", headers=headers)
    
    if response_order.status_code == 200:
        order_data = response_order.json()
        with open('resposta.json', 'w') as f:
            json.dump(order_data, f, indent=4)
        print("Order details saved to resposta.json")
    else:
        print("Error fetching order details.")
        print(response_order.text)
else:
    print("Token not found in the response.")
    print(token_data)