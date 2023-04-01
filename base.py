from functions import Constructor
from bs4 import BeautifulSoup

def scrap():
    url_base = "https://www.my.example.com" # No debe terminar en /
    url = "https://www.my.example.com/index.php/store"
    tables_name = 'Domain,Product,Price'

    domain = Constructor.ext_domain(url_base)
    outfile = Constructor.outfile(domain, tables_name)

    # Imprimimos los valores del atributo href de cada elemento encontrado
    lista_links = []
    for link in Constructor.ext_urls(url):
        var_scrap_links = link["href"].replace('#', '')
        if 'language' not in var_scrap_links and '/store/' in var_scrap_links:
            if 'http' not in var_scrap_links and ':\\' not in var_scrap_links:
                lista_links.append(url_base+var_scrap_links)
            elif domain in var_scrap_links:
                lista_links.append(var_scrap_links)

    # URL de la página a extraer datos
    urls = list(set(lista_links)) # Eliminar duplicados

    for url in urls:
        # Realizar la solicitud HTTP GET a la página web
        #response = requests.get(url)
        response = Constructor.get_requests_with_tor(url)
        
        # Parsear el contenido HTML utilizando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar los elementos HTML que contienen los nombres y precios de los productos
        product_name = soup.find_all('div', class_='top-area')
        product_price = soup.find_all('div', class_='price')
        
        # Iterar sobre los elementos encontrados e imprimir los nombres y precios de los productos
        for nprofuct, pproduct in zip(product_name, product_price):         
            try:
                name_sucio = nprofuct.find('h4').text
                name = name_sucio.replace('  ', '').replace('\n', '').replace(',', '.')
                
                #print(url)
                price_sucio = pproduct.find('span').text
                price = price_sucio.replace(',', '.')

                print(f"{name}: {price}")
                outfile.write(f"{domain},{name},{price}\n")
            except Exception as e:
                if str(e) == "'NoneType' object has no attribute 'text'":
                        try:
                            price_sucio = pproduct.text
                            price = price_sucio.replace('  ', '').replace('\n', '').replace(',', '.')

                            print(f"{name}: {price}")
                            outfile.write(f"{domain},{name},{price}\n")
                        except Exception as a:
                            print(f"ERROR - {url} - {e}")
                            outfile.write('ERROR,ERROR,ERROR')
                else:
                    print(f"ERROR - {url} - {e}")
                    outfile.write('ERROR,ERROR,ERROR')
    outfile.close()