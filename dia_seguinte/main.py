import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime, timedelta
import ast
from collections import Counter
from pesquisa import Collect
from isc import isc_sap, isc_sm, concat_isc
from relatorio import sm, sap, concat_relat

# Carregar o arquivo Excel
Collect()
print('Requisição ISC Feita!')
isc_sap()
print('ISC SAP Finalizado!')
isc_sm()
print('ISC SiteMercado Finalizado!')
concat_isc()
print('Concatenando ISC!')
sm()
print('Gerando Faturamento SiteMercado!')
sap()
print('Gerando Faturamento Sap!')
concat_relat()
print('Concatenando Relatórios!')
print('Gerando Imagens!')

#Carrega os arquivos
file_path = "dataset/combined_data.xlsx"
rating_path = "dataset/combined_ISC.xlsx"
rating_path2 = "dataset/ISC_sap.xlsx"
df = pd.read_excel(file_path)
df_r = pd.read_excel(rating_path)
df_r2 = pd.read_excel(rating_path2)
df_r = df_r.drop_duplicates(subset='id')

#Padronizar o nome das lojas

df_r['loja_id'] = df_r['loja_id'].replace({5: '5 - Wenceslau Braz',
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

def calcular_rating_por_loja_mes(df):#, mes, ano):
    return df.groupby(['loja_id'])['rating'].mean().round(1)

def calcular_selecoes_por_loja_e_tipo(df):
    selecoes_por_loja = {}
  
    opcoes_a_ignorar = [
        'Agilidade da Entrega', 'Agilidade da Retirada',
        'Disponibilidade de Produtos', 'Facilidade de Compra no site',
        'Qualidade da Separação', 'Superou as Expectativas', 
        
    ]

    categorias_tipo = {
        "Agilidade da Entrega": "Logística",
        "Agilidade da Retirada": "Logística",
        "Disponibilidade de Produtos": "Sistema",
        "Facilidade de Compra no site": "Sistema",
        "Qualidade da Separação": "Operação",
        "Superou as Expectativas": "Operação",
        "Atendimento na Loja": "Operação",
        "Escolha da Carne": "Operação",
        "Escolha das Frutas": "Operação",
        "Formas de Pagamento": "Sistema",
        "Mais opções de produtos no site": "Sistema",
        "Não substituíram produtos": "Operação",
        "Substituíram produtos sem minha autorização": "Operação",
        "Serviço de Entrega": "Logística",
        "Temperatura dos Produtos": "Operação",
        "Validade dos Produtos": "Operação",
        "Atendimento do Entregador": "Logística",
        "Entrega Fora do Horário": "Logística",
        "Não recebi todos os produtos do meu pedido": "Operação",
        "Separação Ruim dos Produtos": "Operação",
        "Escolha do hortifruti": "Operação",
        "Escolha da carne": "Operação",
        "Mais formas de pagamento": "Sistema",
        "Dificuldade de compra no site": "Sistema",
        "Dificuldade na retirada": "Operação",
        'Atendimento na Loja': "Operação",
    }

    def string_to_list(string):
        if isinstance(string, list):
            return string
        elif string is None or string == 'nan':
            return []
        items = string.replace("'", "").strip('[]').split(',')
        return [item.strip() for item in items if item]

    df['selected_options'] = df['selected_options'].astype(str).apply(string_to_list)

    for loja in df['loja_id'].unique():
        df_loja = df[df['loja_id'] == loja]
        todas_selecoes = []
        contagem_por_tipo = Counter()
        for selecoes in df_loja['selected_options']:
            selecoes_filtradas = [opcao for opcao in selecoes if opcao not in opcoes_a_ignorar]
            todas_selecoes.extend(selecoes_filtradas)
            for selecao in selecoes_filtradas:
                tipo = categorias_tipo.get(selecao, "Outro")
                contagem_por_tipo[tipo] += 1
        selecoes_contadas = Counter(todas_selecoes)
        selecoes_por_loja[loja] = {
            'categorias': dict(selecoes_contadas),
            'tipos': dict(contagem_por_tipo)
        }
    
    return selecoes_por_loja

def calcular_faturamento_por_loja_e_plataforma(df, data, nome_loja, plataforma):
    df_filtrado = df[(df['Data da entrega'] == data) & (df['Rede - Loja'] == nome_loja) & (df['Plataforma'] == plataforma)]
    faturamento = df_filtrado['Valor do pedido'].sum()
    return faturamento


def resumo_total_pedidos_por_loja(data):

    df_filtrado = df[df['Data da entrega'] == data]

    pedidos_por_tipo = df_filtrado.groupby(['Plataforma', 'Rede - Loja', 'Tipo de entrega']).size().reset_index(name='Quantidade')

    total_pedidos_por_loja = df_filtrado.groupby(['Plataforma', 'Rede - Loja']).size().reset_index(name='Total Pedidos')

    resumo = pd.merge(pedidos_por_tipo, total_pedidos_por_loja, on=['Plataforma', 'Rede - Loja'])

    return resumo

todas_lojas = ['5 - Wenceslau Braz', '8 - Paranaguá',
 '11 - São Braz', '17 - Ahú Gourmet', '21 - Nilo Peçanha', 
 '22 - Champagnat', '23 - Araucária', '27 - Novo Mundo', 
  '29 - Água Verde', '31 - Campo Largo', '32 - Ponta Grossa - Uvaranas', 
  '33 - São José dos Pinhais', '37 - Cajuru', '38 - Colombo', 
  '43 - Almirante Tamandaré', '50 - Santa Quitéria', '91 - Umbará']

for loja in todas_lojas:
    data_hoje = datetime.now().date()
    data_amanha = data_hoje + timedelta(days=1)

    data_hoje_str = data_hoje.strftime('%Y-%m-%d')
    data_amanha_str = data_amanha.strftime('%Y-%m-%d')
    data_hoje_img = data_hoje.strftime("%d/%m/%Y")
    data_amanha_img = data_amanha.strftime("%d/%m/%Y")
    faturamento_loja_dia_sap = calcular_faturamento_por_loja_e_plataforma(df, data_hoje_str, loja, 'SAP')
    faturamento_loja_seguinte_sap = calcular_faturamento_por_loja_e_plataforma(df, data_amanha_str, loja, 'SAP')
    faturamento_loja_dia_sitemercado = calcular_faturamento_por_loja_e_plataforma(df, data_hoje_str, loja, 'SiteMercado')
    faturamento_loja_seguinte_sitemercado = calcular_faturamento_por_loja_e_plataforma(df, data_amanha_str, loja, 'SiteMercado')
    resumo_pedidos_dia_seguinte = resumo_total_pedidos_por_loja(data_amanha_str)
    resumo_pedidos_dia = resumo_total_pedidos_por_loja(data_hoje_str)
    rating_loja = calcular_rating_por_loja_mes(df_r).get(loja, "N/A")
    selecoes_loja = calcular_selecoes_por_loja_e_tipo(df_r2).get(loja, {})
    
    categorias_info = ''
    categorias_ordenadas = sorted(selecoes_loja.get('categorias', {}).items(), key=lambda x: x[1], reverse=True)

    for cat, contagem in categorias_ordenadas:
        categorias_info += f"{cat}: {contagem}\n"

    tipos_info = ''
    tipos_ordenados = sorted(selecoes_loja.get('tipos', {}).items(), key=lambda x: x[1], reverse=True)

    total_tipos = sum(val for _, val in tipos_ordenados)

    # Definindo a largura fixa para cada campo
    largura_tipo = 10
    largura_quantidade = 6
    largura_percentual = 6

    for tipo, contagem in tipos_ordenados:
        percentual = (contagem / total_tipos) * 100 if total_tipos > 0 else 0
        # Formatação de números com zero à esquerda
        tipos_info += f"{tipo:<{largura_tipo}} {contagem:02d}   {int(percentual)}%\n"

    tipos_info += f"{'Total':<{largura_tipo}} {total_tipos:02d}    100%"
 
    resumo_loja_dia_seguinte = resumo_pedidos_dia_seguinte[resumo_pedidos_dia_seguinte['Rede - Loja'] == loja]
    resumo_loja_dia = resumo_pedidos_dia[resumo_pedidos_dia['Rede - Loja'] == loja]

    entrega_sap = entrega_sitemercado = retirada_sap = retirada_sitemercado = 0
    entrega_sap1 = entrega_sitemercado1 = retirada_sap1 = retirada_sitemercado1 = 0
    font_size = 14
    font_loja = 14
    font_size2 = 17
    font_size3 = 24
    
    font = ImageFont.truetype('arial.ttf', size=font_size)
    font2 = ImageFont.truetype('impact.ttf', size=font_size2)
    font3 = ImageFont.truetype('impact.ttf', size=font_size3)
    font4 = ImageFont.truetype('impact.ttf', size=font_loja)
    
    for _, row in resumo_loja_dia_seguinte.iterrows():
        if row['Plataforma'] == 'SAP' and row['Tipo de entrega'] == 'ENTREGA':
            entrega_sap += row['Quantidade']
        elif row['Plataforma'] == 'SAP' and row['Tipo de entrega'] == 'RETIRADA':
            retirada_sap += row['Quantidade']
        elif row['Plataforma'] == 'SiteMercado' and row['Tipo de entrega'] == 'ENTREGA':
            entrega_sitemercado += row['Quantidade']
        elif row['Plataforma'] == 'SiteMercado' and row['Tipo de entrega'] == 'RETIRADA':
            retirada_sitemercado += row['Quantidade']
    
    total_pedidos = entrega_sap + entrega_sitemercado + retirada_sap + retirada_sitemercado
    total_sap = entrega_sap + retirada_sap
    total_sm = entrega_sitemercado + retirada_sitemercado

    for _, row in resumo_loja_dia.iterrows():
        if row['Plataforma'] == 'SAP' and row['Tipo de entrega'] == 'ENTREGA':
            entrega_sap1 += row['Quantidade']
        elif row['Plataforma'] == 'SAP' and row['Tipo de entrega'] == 'RETIRADA':
            retirada_sap1 += row['Quantidade']
        elif row['Plataforma'] == 'SiteMercado' and row['Tipo de entrega'] == 'ENTREGA':
            entrega_sitemercado1 += row['Quantidade']
        elif row['Plataforma'] == 'SiteMercado' and row['Tipo de entrega'] == 'RETIRADA':
            retirada_sitemercado1 += row['Quantidade']
    total_pedidos_dia = entrega_sap1 + entrega_sitemercado1 + retirada_sap1 + retirada_sitemercado1
    total_sap1 = entrega_sap1 + retirada_sap1
    total_sm1 = entrega_sitemercado1 + retirada_sitemercado1
    data_dia = datetime.now()              
    img = Image.new('RGB', (550, 640), color=(5, 79, 119))
    draw = ImageDraw.Draw(img)
    texto_loja = f'{loja}\n\n\n'
    sap = 'SAP'
    sap1 = 'SAP'
    site_mercado = 'SiteMercado'
    site_mercado1 = 'SiteMercado'
    texto_corpo = f'''

        Faturamento: R${faturamento_loja_dia_sap:.0f} 
        Pedidos: {total_sap1}

        Faturamento: R${faturamento_loja_dia_sitemercado:.0f}
        Pedidos: {total_sm1}
 

    '''
    texto_corpo1 = f'''

    
        Faturamento: R${faturamento_loja_seguinte_sap:.0f} 
        Pedidos: {total_sap}
 
        Faturamento: R${faturamento_loja_seguinte_sitemercado:.0f}
        Pedidos: {total_sm}
 
    '''
  
  
    texto_datahoje = f'{data_hoje_img}'
    texto_dataamanha = f'{data_amanha_img}'
    texto_ISC = f'ISC {rating_loja}'
    linha_separadora = "-" * 72
    feedback = f'''{categorias_info}
    
    '''


    texto_corpo2 = f"{tipos_info}"
  
  
    text_feedback = ' Feedback negativo dos clientes:'
    
    linhas = tipos_info.split('\n')
    x, y = 350, 295
    largura_tipo = 10  # Ajuste conforme necessário
    largura_quantidade = 11  # Ajuste conforme necessário para quantidade
    largura_percentual = 6
    draw.text((10, 20), texto_loja, font=font2, fill=(255, 255, 255))
    draw.text((30, 55), texto_corpo, font=font, fill=(255, 255, 255))
    draw.text((260, 35), texto_corpo1, font=font, fill=(255, 255, 255))
    draw.text((20, 45), texto_datahoje, font=font2, fill=(255, 255, 255))
    draw.text((280, 45), texto_dataamanha, font=font2, fill=(255, 255, 255))
    draw.text((20, 220), texto_ISC, font=font3, fill=(255, 255, 255))
    draw.text((20, 190), linha_separadora, font=font3, fill=(255, 255, 255))
    draw.text((40, 70), sap, font=font4, fill=(255, 255, 255))
    draw.text((40, 120), site_mercado, font=font4, fill=(255, 255, 255))
    draw.text((280, 70), sap1, font=font4, fill=(255, 255, 255))
    draw.text((280, 120), site_mercado1, font=font4, fill=(255, 255, 255))
    draw.text((20, 325), feedback, font=font, fill=(255, 255, 255))
 
    for linha in linhas:
        partes = linha.split()  # Divide a linha em partes

        if len(partes) == 3:
            tipo, quantidade, percentual = partes

           
            if tipo == "Sistema":
                tipo = tipo.ljust(16)  
            elif tipo == "Logística":
                tipo = tipo.ljust(16) 
            elif tipo == "Operação":
                tipo = tipo.ljust(13)  
            elif tipo == "Total":
                tipo = tipo.ljust(24)

            quantidade_ajustada = quantidade.ljust(largura_quantidade)
            percentual_ajustado = percentual.ljust(largura_percentual)

            linha_ajustada = f"{tipo}{quantidade_ajustada}{percentual_ajustado}"

            draw.text((x, y), linha_ajustada, font=font4, fill=(255, 255, 255))
            y += 20
    draw.text((20, 285), text_feedback, font=font4, fill=(255, 255, 255))
    #Logística = Image.open('media/Condoremcasa-removebg-preview.png')
    Logística = Image.open('media/logo_nova.png')

    Logística = Logística.resize((120, 120))
    img.paste(Logística, (420, 510), Logística)
                
    img.save(os.path.join(f'imagens/{loja}.png'))

print('Finalizado!')