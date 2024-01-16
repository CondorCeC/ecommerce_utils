import requests
from datetime import datetime
import json
import pandas as pd
def Collect():
    url = 'https://pesquisa.cndr.me/api/feedback/'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        mes_atual = datetime.now().month
        mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
        filtered_data = [item for item in data if datetime.strptime(item['data_pedido'], '%Y-%m-%d').month in [mes_atual, mes_anterior]]
        #filtered_data = [item for item in data if datetime.strptime(item['data_pedido'], '%Y-%m-%d').month == 12]
        with open('json/pesquisa.json', 'w', encoding='utf-8') as json_file:
            json.dump(filtered_data, json_file, ensure_ascii=False, indent=4)
        df = pd.read_json('json/pesquisa.json')
        df.to_excel('dataset/pesquisa.xlsx')
    else:
        print("Erro ao fazer a requisição")   

Collect()