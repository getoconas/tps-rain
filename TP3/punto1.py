import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from unidecode import unidecode # convertir caracteres Unicode a ASCII
import matplotlib.pyplot as plt 
import pandas as pd
import networkx as nx

# Metodo para obtener los enlaces que hace referencia a deportes en la pagina de infobae
def get_html_base(url):
  response = requests.get(url)

  if response.status_code == 200: # Verificar si la solicitud fue exitosa (200 OK)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extraer enlaces de la página
    # Encontrar todas las etiquetas <a> con la clase 'story-card-ctn' y asegurarse de que la clase sea exactamente 'story-card-ctn'
    array_links = [a for a in soup.find_all('a', class_='story-card-ctn') if a.get('class') == ['story-card-ctn']] 
    hrefs = []

    for i, news in enumerate(array_links[:60], start = 1):
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
      if href and ('/deportes/' in href):  # filtrar enlaces a otras noticias de deportes
        full_url = urljoin(base_url, href)
        urls.add(full_url)
    return urls
  else:
    print(f"*** Error al obtener la noticia: {response.status_code} ***")
    return None
  
def get_title(url):
  response = requests.get(url)
  if response.status_code == 200: # Verificar si la solicitud fue exitosa (200 OK)
    #print('200 OK')
    soup = BeautifulSoup(response.content, 'html.parser') # Crear un objeto BeautifulSoup para analizar el contenido HTML
    title_element = soup.find('h1').text.strip() # Obtener el título de la noticia
    #title = unidecode(title_element).lower()
    return title_element
  else:
    print(f"*** Error al obtener el título: {response.status_code} ***")
    return None

# Metodo para realizar el crawling de las URLs
def crawl(url, max_depth):
  visited = set()  # Conjunto para almacenar URLs visitadas
  queue = [(url, 0)]  # Cola para almacenar URLs a visitar
  collected_urls = []

  while queue:
    current_url, current_depth = queue.pop(0)
    if current_depth > max_depth:
      continue
    if current_url in visited:
      continue

    print(f"Crawling {current_url} at depth {current_depth}")
    visited.add(current_url)

    # Guardar el enlace actual y su profundidad
    title = get_title(current_url)
    collected_urls.append((current_url, current_depth, title))

    # Obtener nuevos enlaces internos
    urls = get_html_notice(current_url)
    for url in urls:
      if url not in visited:
        queue.append((url, current_depth + 1))

  return collected_urls

def build_graph(collected_urls):
  G = nx.DiGraph()
  url_set = set(url for url, _, _ in collected_urls)
  for source_url, _, source_title in collected_urls:
    G.add_node(source_url, title=source_title)  # Agregar nodo con título
    referenced = get_html_notice(source_url)
    if referenced:
      for target_url in referenced:
        if target_url in url_set:
          if G.has_edge(source_url, target_url):
            G[source_url][target_url]['weight'] += 1
          else:
            G.add_edge(source_url, target_url, weight=1)
  return G

def save_graph(graph, filename="grafo_noticias.graphml"):
  nx.write_graphml(graph, filename)

# Metodo para guardar las URLs recolectadas en un archivo Excel

def save_to_excel(data, filename):
  df = pd.DataFrame(data, columns=['URL', 'Depth', 'title'])
  df.to_excel(filename, index=False)

def draw_and_save_graph(graph, filename="grafo_noticias.png"):
    plt.figure(figsize=(30, 30))
    pos = nx.spring_layout(graph, k=0.20, iterations=20)

    # Etiquetas de nodos: usa el atributo 'title'
    labels = {
        node: (graph.nodes[node]['title'][:25] + '...') 
        if len(graph.nodes[node]['title']) > 25 
        else graph.nodes[node]['title']
        for node in graph.nodes
    }

    # Filtrar aristas con peso <= 2
    edges_to_draw = [
        (u, v) for u, v, d in graph.edges(data=True) if d['weight'] <= 2
    ]
    edge_weights = {
        (u, v): d['weight'] for u, v, d in graph.edges(data=True) if d['weight'] <= 2
    }

    # Dibujar solo los nodos y las aristas filtradas
    nx.draw_networkx_nodes(graph, pos, node_size=100)
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8)
    nx.draw_networkx_edges(graph, pos, edgelist=edges_to_draw, edge_color='gray', alpha=0.7)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_weights, font_color='red', font_size=7)

    plt.savefig(filename, format="png", dpi=350)
    plt.close()

# Iniciar el crawling desde la URL inicial con una profundidad máxima de 2
base_url = "https://www.infobae.com"
start_url = "https://www.infobae.com/deportes"
max_depth = 2
href_base = get_html_base(start_url)
collected_urls_total = []
# Recorrer los enlaces obtenidos de la pagina principal
for href in href_base:
  full_url = urljoin(base_url, href)
  print('Noticia Principal: ' + full_url)
  collected_urls = crawl(full_url, max_depth)
  collected_urls_total.extend(collected_urls)

graph = build_graph(collected_urls_total)
save_graph(graph)
print("*** Grafo exportado como grafo_noticias.graphml ***")

draw_and_save_graph(graph)
print("*** Imagen del grafo guardada como grafo_noticias.png ***")

# Guardar las URLs recolectadas en un archivo Excel
filename = "collected_urls.xlsx"
save_to_excel(collected_urls_total, filename)

#print("*** URLs recolectadas guardadas en el archivo collected_urls.xlsx***")
print("*** Fin del programa ***") # Mensaje de finalización del programa
