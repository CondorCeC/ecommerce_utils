import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR')
from datetime import datetime
import os

sm_path = "C:\\Users\\henni\\Downloads\\sm.xlsx"

def sm():
    df_sm = pd.read_excel(sm_path)
    df_sm = df_sm.drop(df_sm[df_sm['Status do pedido'] == 'CAN'].index)
    colunas_sm = [
        'Código do pedido',    
        'Valor do pedido', 
        'Status do pedido',    
        'Tipo de entrega', 
        'Data do pedido',  
        'Data da entrega', 
        'Plataforma', 
        'Rede - Loja'
    ]
    df_sm['Rede - Loja'] = df_sm['Rede - Loja'].replace({'Condor- Loja Super Condor Wenceslau Braz': '5 - Wenceslau Braz',
                                            'Condor- Loja Super Condor Paranaguá-Centro': '8 - Paranaguá',
                                            'Condor- Loja Hiper Condor São Braz': '11 - São Braz',
                                            'Condor- Loja Super Condor Ahú': '17 - Ahú Gourmet',
                                            'Condor- Loja Hiper Condor Nilo Peçanha': '21 - Nilo Peçanha',
                                            'Condor- Loja Champagnat': '22 - Champagnat',
                                            'Condor- Loja Hiper Condor Araucária BR': '23 - Araucária',
                                            'Condor- Loja Hiper Condor Novo Mundo': '27 - Novo Mundo',
                                            'Condor- Loja Hiper Condor Água Verde': '29 - Água Verde',
                                            'Condor- Super Condor Campo Largo-Centro': '31 - Campo Largo',
                                            'Condor- Loja Hiper Condor Uvaranas': '32 - Ponta Grossa - Uvaranas',
                                            'Condor- Loja Hiper Condor São José dos Pinhais-Rua Joinville': '33 - São José dos Pinhais',
                                            'Condor- Loja Super Condor Cajuru': '37 - Cajuru',
                                            'Condor- Loja Hiper Condor Colombo': '38 - Colombo',
                                            'Condor- Super Condor Almirante Tamandaré ': '43 - Almirante Tamandaré',
                                            'Condor- Loja Super Condor Santa Quitéria': '50 - Santa Quitéria',
                                            'Condor- Super Condor Umbará': '91 - Umbará'})
    df_sm = df_sm[colunas_sm]
    df_sm[['Data da entrega', 'Horário Entrega']] = df_sm['Data da entrega'].str.split('T', expand=True)
    df_sm[['Data do pedido', 'Horário Entrega']] = df_sm['Data do pedido'].str.split('T', expand=True)
    df_sm.drop('Horário Entrega', axis=1, inplace=True)

    df_sm.to_excel('dataset/sm.xlsx', index=False)

def sap():
    sap_path = "C:\\Users\\henni\\Downloads\\list.csv"
    def convert_date(date_str):
        locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        date_str = date_str.replace('BRT', '').strip()
        date_str = ' '.join(date_str.split()) 
        dt = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y')
        return dt.strftime('%Y-%m-%d')
    df_sap = pd.read_csv(sap_path, delimiter=";")
    df_sap = df_sap.drop(df_sap[df_sap['Status do pedido'] == 'Cancelado'].index)
    df_sap['Loja Selecionada'] = df_sap['Loja Selecionada'].replace({'8 - Paranaguá - Centro': '8 - Paranaguá',
                                                                     '17 - Gourmet Ahu': '17 - Ahú Gourmet',})
    temp_excel_path = "C:\\Users\\henni\\Downloads\\TempPasta1.xlsx"
    df_sap.to_excel(temp_excel_path, index=False)
    df_excel = pd.read_excel(temp_excel_path)
    df_excel['Data de Entrega / Retirada'] = df_excel['Data de Entrega / Retirada'].apply(convert_date)
    df_excel['Data'] = df_excel['Data'].apply(convert_date)
    df_excel['Loja Selecionada Id'] = df_excel['Loja Selecionada'].apply(lambda x: x.split(' ')[0] + '-00')
    df_excel['Código do pedido'] = df_excel.apply(lambda row: row['Loja Selecionada Id'] + str(row['Nº do pedido.']), axis=1)
    df_excel['Modo de entrega'] = df_excel['Modo de entrega'].replace({'Retirada[pickup]': 'RETIRADA',
                                        'Entrega no endereço[standard-gross]': 'ENTREGA',
    })
    df_excel['Plataforma'] = 'SAP'
    colunas_sap = [
        'Código do pedido',    
        'Preço total.1', 
        'Status do pedido',    
        'Modo de entrega', 
        'Data',  
        'Data de Entrega / Retirada',  
        'Plataforma',
        'Loja Selecionada'
    ]
    df_excel = df_excel[colunas_sap]
    df_excel.to_excel('dataset/sap.xlsx', index=False)
    os.remove(temp_excel_path)


def concat_relat():
    df_sap = pd.read_excel('dataset/sap.xlsx')
    df_sm = pd.read_excel('dataset/sm.xlsx')
    colunas_renomear = {
        'Preço total.1': 'Valor do pedido', 
        #'Preço total': 'Valor do pedido', 
        'Modo de entrega': 'Tipo de entrega',
        'Data': 'Data do pedido',  
        'Data de Entrega / Retirada': 'Data da entrega',  
        'Loja Selecionada': 'Rede - Loja'
    }

    # Renomeando as colunas
    df_sap.rename(columns=colunas_renomear, inplace=True)

    # Agora as colunas de df_sap e df_sm devem ser as mesmas, permitindo a concatenação
    df_combined = pd.concat([df_sm, df_sap], ignore_index=True)
    df_combined.to_excel('dataset/combined_data.xlsx', index=False)

sap()
sm()
concat_relat()