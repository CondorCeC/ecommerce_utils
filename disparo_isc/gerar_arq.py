import locale
from datetime import datetime
import pandas as pd
import os

# Função para converter a string de data para o formato desejado
def convert_date(date_str):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    date_str = date_str.replace('BRT', '').strip()
    date_str = ' '.join(date_str.split())
    dt = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y')
    return dt

# Leitura do arquivo CSV
df_csv = pd.read_csv("C:\\Users\\henni\\Downloads\\list.csv", delimiter=";")
temp_excel_path = "C:\\Users\\henni\\Downloads\\TempPasta1.xlsx"
df_csv.to_excel(temp_excel_path, index=False)

# Leitura do arquivo Excel temporário
df_excel = pd.read_excel(temp_excel_path)

# Conversão da coluna 'Data' para o formato de data
df_excel['Data'] = df_excel['Data'].apply(convert_date)
df_excel['Data'] = pd.to_datetime(df_excel['Data'])

# Processamento adicional dos dados
df_excel['Loja Selecionada Id'] = df_excel['Loja Selecionada'].apply(lambda x: x.split(' ')[0] + '-00')
df_excel['Pedido Completo'] = df_excel.apply(lambda row: row['Loja Selecionada Id'] + str(row['Nº do pedido.']), axis=1)
df_final = df_excel[['Loja Selecionada Id', 'E-mail', 'Pedido Completo', 'Data']]

# Renomeando as colunas
df_final.rename(columns={
    'Loja Selecionada Id': 'nome',
    'E-mail': 'Email',
    'Pedido Completo': 'pedido',
    'Data': 'data'
}, inplace=True)

# Salvando o arquivo final
final_excel_path = "C:\\Users\\henni\\Área de Trabalho\\pesquisa_envio\\disparo.xlsx"
df_final.to_excel(final_excel_path, index=False)

# Removendo o arquivo temporário
os.remove(temp_excel_path)
