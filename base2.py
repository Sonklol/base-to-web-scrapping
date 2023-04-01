from functions import Constructor
from bs4 import BeautifulSoup

def scrap():
    url_base = "https://www.example.es"
    url = "https://www.example.es/"
    tables_name = 'Domain,Product,Price,Price_Comments'

    domain = Constructor.ext_domain(url_base)
    outfile = Constructor.outfile(domain, tables_name)

    # Imprimimos los valores del atributo href de cada elemento encontrado
    lista_links = []
    for link in Constructor.ext_urls(url):
        var_scrap_links = link["href"]
        if '34941620100' not in var_scrap_links:
            if 'http' not in var_scrap_links and ':\\' not in var_scrap_links:
                lista_links.append(url_base+var_scrap_links)
            elif domain in var_scrap_links:
                lista_links.append(var_scrap_links)

    # URL de la página a extraer datos
    urls = list(set(lista_links)) # Eliminar duplicados

    for url in urls:
        # Realizar la solicitud HTTP GET a la página web
        response = Constructor.get_requests_with_tor(url)

        # Parsear el contenido HTML utilizando BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Encontrar los elementos HTML que contienen los nombres y precios de los productos
        product_name = soup.find_all('div', class_='product')
        product_price = soup.find_all('b', class_='show')
        
        # Iterar sobre los elementos encontrados e imprimir los nombres y precios de los productos
        for nprofuct, pproduct in zip(product_name, product_price):     
            try:
                name_sucio = nprofuct.find('b', dt='name').text
                name = name_sucio.replace('  ', '').replace('\n', '').replace(',', '.')
                #print(pproduct)
                price_sucio = pproduct.find('span').text
                price = price_sucio.replace('  ', '').replace('\n', '').replace(',', '.')

                price_comments_sucio = pproduct.find('span', class_="comments").text
                price_comments = price_comments_sucio.replace('  ', '').replace('\n', '').replace(',', '.')

                if price_comments not in price:
                    print(f"{name}: {price} {price_comments}")
                    outfile.write(f"{domain},{name},{price},{price_comments}\n")
                else:
                    print(f"{name}: {price}")
                    outfile.write(f"{domain},{name},{price}\n")
            except:
                pass
                #print(f"ERROR - {url} - {e}")
                #outfile.write('ERROR,ERROR,ERROR')
    outfile.close()