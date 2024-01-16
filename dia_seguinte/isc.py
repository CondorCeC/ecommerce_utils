import pandas as pd
def isc_sm():
    sm_path = "C:\\Users\\henni\\Downloads\\sm.xlsx"

    df_sm = pd.read_excel(sm_path)
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
    columns = [
        'ID', 'Rede - Loja', 'Nota da avaliação'
    ]

    df_sm = df_sm.dropna(subset=['Nota da avaliação'])
    df_sm['ID'] = range(800, 800 + len(df_sm))
    df_sm = df_sm[columns]
    df_sm.to_excel('dataset/ISC_sm.xlsx', index=False)


def isc_sap():
    #sap_path = "C:\\Users\\henni\\Downloads\\feedback.xlsx"
    sap_path = "dataset/pesquisa.xlsx"

    df_sap = pd.read_excel(sap_path)
    
    df_sap['loja_id'] = df_sap['loja_id'].replace({5: '5 - Wenceslau Braz',
                                        8: '8 - Paranaguá',
                                        11: '11 - São Braz',
                                        17: '17 - Ahú Gourmet',
                                        21: '21 - Nilo Peçanha',
                                        22: '22 - Champagnat',
                                        23: '23 - Araucária',
                                        27: '27 - Novo Mundo',
                                        29: '29 - Água Verde',
                                        28: '28 - Cristo Rei',
                                        31: '31 - Campo Largo',
                                        32: '32 - Ponta Grossa - Uvaranas',
                                        33: '33 - São José dos Pinhais',
                                        37: '37 - Cajuru',
                                        38: '38 - Colombo',
                                        43: '43 - Almirante Tamandaré',
                                        50: '50 - Santa Quitéria',
                                        91: '91 - Umbará'})
    columns = [
        'id', 'loja_id', 'rating', 'selected_options'
    ]

    df_sap = df_sap[columns]
    
    df_sap.to_excel('dataset/ISC_sap.xlsx', index=False)


def concat_isc():
    df_sap = pd.read_excel('dataset/ISC_sap.xlsx')
    df_sm = pd.read_excel('dataset/ISC_sm.xlsx')

    colunas_renomear = {
    
        'Nota da avaliação': 'rating',
        'ID': 'id',
        'Rede - Loja': 'loja_id'
    }

    # # # Renomeando as colunas
    df_sm.rename(columns=colunas_renomear, inplace=True)

    # # # Agora as colunas de df_sap e df_sm devem ser as mesmas, permitindo a concatenação
    df_combined = pd.concat([df_sm, df_sap], ignore_index=True)
    df_combined.to_excel('dataset/combined_ISC.xlsx', index=False)


