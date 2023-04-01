from datetime import datetime
import requests
import socks
import socket
from bs4 import BeautifulSoup
import tldextract
import os

class Constructor:
    # Fecha y Hora actual
    def hora_fecha():
        now = datetime.now()
        fecha_hora = now.strftime('%H-%M-%d-%m-%Y')
        
        return fecha_hora

    # Extraer el nombre de dominio
    def ext_domain(url_base):
        extracted = tldextract.extract(url_base)
        domain = extracted.domain

        return domain
    def ext_urls(url):
        # Hacemos la solicitud HTTP a la página
        #response = requests.get(url)
        response = Constructor.get_requests_with_tor(url)

        # Analizamos el contenido HTML de la respuesta utilizando BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Buscamos todos los elementos <a> que contienen un atributo href
        links = soup.find_all("a", href=True)

        return links

    def outfile(domain, tables_name):
        # Crear carpeta
        try:
            os.makedirs('exports')
        except FileExistsError:
            pass

        # Crear archivo
        outfile = open(f'exports\{domain}-{Constructor.hora_fecha()}.txt', "w", encoding='utf-8')
        outfile.write(tables_name+'\n')
       
        return outfile

    # Configuración de SOCKS proxy con TOR
    def get_requests_with_tor(url):
        ports_list = [9150, 9050]
        response = None

        for ports in ports_list:
            socks.set_default_proxy(socks.SOCKS5, "localhost", ports)
            socket.socket = socks.socksocket
            try:
                response = requests.get(url)
                break
            except requests.exceptions.RequestException:
                pass
            
        # Comprobar si la solicitud fue exitosa
        if response is None or response.status_code != 200:
            print('WARNING - RECUERDA QUE HAY QUE ABRIR TOR Y CONECTARSE PARA QUE PUEDA FUNCIONAR.')
            print("ERROR - Error al hacer la solicitud HTTP GET a la página web.")

        return response