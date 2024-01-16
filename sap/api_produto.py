import requests
import xmltodict
import json

def produto(ean):
    url = f"https://api.c9t6aobb6f-condorsup1-p1-public.model-t.cc.commerce.ondemand.com/occ/v2/condor/products/{ean}"
    #url = "https://api.c9t6aobb6f-condorsup1-p1-public.model-t.cc.commerce.ondemand.com/occ/v2/condor/products/7908163647519"
    headers = {'accept': 'application/xml'}

    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        dict_data = xmltodict.parse(response.content)

        json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)

        with open("json/data.json", "w", encoding="utf-8") as json_file:
            json_file.write(json_data)

        print("Dados salvos em data.json")
    else:
        print(f"Erro na requisição: {response.status_code}")
        print("Resposta da API:", response.text) 

def estoque():
    url = "https://api.c9t6aobb6f-condorsup1-p1-public.model-t.cc.commerce.ondemand.com/occ/v2/condor/products/7891515534110/stock/21"
    headers = {'accept': 'application/xml'}

    response = requests.get(url, headers=headers)


    if response.status_code == 200:

        dict_data = xmltodict.parse(response.content)


        json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)

        with open("json/estoque.json", "w", encoding="utf-8") as json_file:
            json_file.write(json_data)

        print("Dados salvos em estoque.json")
    else:
        print(f"Erro na requisição: {response.status_code}")   


produto(7894904727193)