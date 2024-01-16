from django.shortcuts import render, redirect
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pandas as pd
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR')
from PIL import Image, ImageDraw, ImageFont
import os

def home(request):
    return render(request, 'disparo_isc/index.html')

def envio_pesquisa(request):
    if request.method == 'GET':
        return render(request, 'disparo_isc/envio_pesquisa.html')
    if request.method == 'POST':
        
        file = request.FILES['file']
        df = pd.read_excel(file)

        print(df)
        smtp_server = 'smtp.condor.com.br'
        smtp_port = 587
        smtp_username = 'sac.cec'
        smtp_password = 'PXGf@3PU'

        datas_pedido = df['data'].tolist()
        emails = df['Email']  
        nomes = df['nome'] 
        pedidos = df['pedido'] 
        pedidos = df['pedido'].astype(str).str.rstrip('.0').tolist()
        data_pedido = df['data']
        CAMINHO_HTML = 'base_templates/global/arte1.html'


        with open(CAMINHO_HTML, 'r') as arquivo:
            texto_arquivo = arquivo.read()

        for email, nome, pedido, data in zip(emails, nomes, pedidos, data_pedido):
            if isinstance(data, str):
                data = datetime.strptime(data, '%d/%m/%Y')
            formatted_data = data.strftime('%Y-%m-%d')
            remetente = 'Condor em Casa <sac.cec>'
            destinatario = email


            #texto_email = texto_arquivo.replace('{pedido}', str(pedido))
            texto_email = (texto_arquivo.replace('{pedido}', str(pedido))
                           .replace('{data_pedido}', str(formatted_data)))

            
            mime_multipart = MIMEMultipart()
            mime_multipart['from'] = remetente
            mime_multipart['to'] = destinatario
            mime_multipart['subject'] = 'Pesquisa Satisfação Condor em Casa'

            corpo_email = MIMEText(texto_email, 'html', 'utf-8')
            mime_multipart.attach(corpo_email)

            # Envia o e-mail
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                
                server.ehlo()
                server.login(smtp_username, smtp_password)
                server.send_message(mime_multipart)
                print(f'E-mail enviado para {email} com sucesso!')

        return render(request, 'disparo_isc/envio_pesquisa.html')