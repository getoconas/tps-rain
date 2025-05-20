import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

# Metodo para obtener los enlaces que hace referencia a deportes en la pagina de infobae
def get_html_base(url):
  response = requests.get(url)

  if response.status_code == 200: # Verificar si la solicitud fue exitosa (200 OK)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer enlaces de la página
    # Encontrar todas las etiquetas <a> con la clase 'story-card-ctn' y asegurarse de que la clase sea exactamente 'story-card-ctn'
    array_links = [a for a in soup.find_all('a', class_='story-card-ctn') if a.get('class') == ['story-card-ctn']] 
    hrefs = []

    for i, news in enumerate(array_links[:30], start = 1):
      href = news.get('href') # href de la noticia
      hrefs.append(href)
    return hrefs
  else:
    print(f"*** Error al obtener la página: {response.status_code} ***")
    return None

# Obtener los href dentro de cada noticia 
def get_html_notice(url):
  response = requests.get(url)
  if response.status_code == 200: # Verificar si la solicitud fue exitosa (200 OK)
    soup = BeautifulSoup(response.content, 'html.parser') # Crear un objeto BeautifulSoup para analizar el contenido HTML
    urls = set() # Conjunto para almacenar URLs visitadas
    array_news = [
      a for a in soup.find_all('a', class_=('feed-list-card', 'most-read-card-ctn'))
      if a.get('class') == ['feed-list-card'] or a.get('class') == ['most-read-card-ctn']
    ]

    for i, news in enumerate(array_news, start = 1):
      href = news.get('href') # href de la noticia
      full_url = urljoin(base_url, href)
      urls.add(full_url)
    return urls
  else:
    print(f"*** Error al obtener la noticia: {response.status_code} ***")
    return None

# Metodo para realizar el crawling de las URLs
def crawl(url, max_depth):
  visited = set() # Conjunto para almacenar URLs visitadas
  queue = [(url, 0)] # Cola para almacenar URLs a visitar
  collected_urls = []

  while queue:
    current_url, current_depth = queue.pop(0)
    if current_depth > max_depth:
      continue
    if current_url in visited:
      continue

    print(f"Crawling {current_url} at depth {current_depth}")
    visited.add(current_url)
    urls = get_html_notice(current_url)
    for url in urls:
      # Agregar URLs de profundidad 3 sin visitarlas
      if current_depth == 2:
        collected_urls.append((url, current_depth + 1))
      elif current_depth + 1 <= max_depth and url not in visited:
        queue.append((url, current_depth + 1))  
  
  return collected_urls

# Metodo para guardar las URLs recolectadas en un archivo Excel
def save_to_excel(data, filename):
  df = pd.DataFrame(data, columns=['URL', 'Depth'])
  df.to_excel(filename, index=False)

# Iniciar el crawling desde la URL inicial con una profundidad máxima de 2
base_url = "https://www.infobae.com"
start_url = "https://www.infobae.com/deportes"
max_depth = 2
href_base = get_html_base(start_url)

# Recorrer los enlaces obtenidos de la pagina principal
for href in href_base:
  full_url = urljoin(base_url, href)
  print('************ Link Noticia Principal: ' + full_url + ' ************')
  collected_urls = crawl(full_url, max_depth)

# Guardar las URLs recolectadas en un archivo Excel
filename = "collected_urls.xlsx"
save_to_excel(collected_urls, filename)

print("*** URLs recolectadas guardadas en el archivo collected_urls.xlsx***")
print("*** Fin del programa ***") # Mensaje de finalización del programa
