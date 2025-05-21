import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Método para obtener los enlaces que hacen referencia a deportes en la página de infobae
def get_html_base(url):
    response = requests.get(url)

    if response.status_code == 200: # Verificar si la solicitud fue exitosa (200 OK)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extraer enlaces de la página
        array_links = [a for a in soup.find_all('a', class_='story-card-ctn') if a.get('class') == ['story-card-ctn']] 
        hrefs = []

        for i, news in enumerate(array_links[:50], start=1):
            href = news.get('href') # href de la noticia
            hrefs.append(href)
        return hrefs
    else:
        print(f"*** Error al obtener la página: {response.status_code} ***")
        return None

# Obtener los href dentro de cada noticia 
def get_html_notice(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        urls = set()
        array_news = [
            a for a in soup.find_all('a', class_=('feed-list-card', 'most-read-card-ctn'))
            if a.get('class') == ['feed-list-card'] or a.get('class') == ['most-read-card-ctn']
        ]

        for news in array_news:
            href = news.get('href')
            if href and ('/deportes/' in href):
                full_url = urljoin(base_url, href)
                urls.add(full_url)
        return urls
    else:
        print(f"*** Error al obtener la noticia: {response.status_code} ***")
        return None

# Método para obtener noticias referenciadas (para el grafo)
def get_referenced_news(url, base_url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        referenced = set()
        
        # Buscar enlaces a otras noticias deportivas
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if href and ('/deportes/' in href or '/sports/' in href):
                full_url = urljoin(base_url, href)
                referenced.add(full_url)
        return referenced
    else:
        print(f"Error al obtener noticia {url}: {response.status_code}")
        return set()

# Método para realizar el crawling de las URLs
def crawl(url, max_depth):
    visited = set()
    queue = [(url, 0)]
    collected_urls = []

    while queue:
        current_url, current_depth = queue.pop(0)
        if current_depth > max_depth:
            continue
        if current_url in visited:
            continue

        print(f"Crawling {current_url} at depth {current_depth}")
        visited.add(current_url)
        collected_urls.append((current_url, current_depth))

        urls = get_html_notice(current_url)
        if urls:
            for url in urls:
                if url not in visited:
                    queue.append((url, current_depth + 1))

    return collected_urls

# Método para guardar las URLs recolectadas en un archivo Excel
def save_to_excel(data, filename):
    df = pd.DataFrame(data, columns=['URL', 'Depth'])
    df.to_excel(filename, index=False)

# Funciones para el grafo
def build_graph(news_urls_with_depth, base_url):
    graph = nx.DiGraph()
    url_to_depth = {url: depth for url, depth in news_urls_with_depth}  # Extrae URL y depth

    for source_url, source_depth in news_urls_with_depth:  # Itera sobre tuplas
        print(f"Procesando noticia: {source_url}")
        referenced = get_referenced_news(source_url, base_url)
        for target_url in referenced:
            if target_url in url_to_depth:  # Verifica si la URL referenciada está en el grafo
                weight = source_depth  # Usa depth como peso (o define otra lógica)
                if graph.has_edge(source_url, target_url):
                    graph[source_url][target_url]['weight'] += weight
                else:
                    graph.add_edge(source_url, target_url, weight=weight)
    return graph

def save_graph(graph, filename="grafo_noticias.graphml"):
    nx.write_graphml(graph, filename)
    print(f"*** Grafo exportado a {filename} ***")


def extract_title_from_url(url):
    """Extrae el título de la noticia desde la URL y lo limita a 10 palabras"""
    # Ejemplo de URL: https://www.infobae.com/deportes/2025/05/20/river-plate-se-enfrentara-a-platense-por-un-lugar-en-las-semifinales/
    parts = url.split('/')
    if len(parts) >= 6:  # Asegurarse que la URL tiene el formato esperado
        title_part = parts[-2] if parts[-1] == '' else parts[-1]  # Manejar URLs que terminen en /
        title_words = title_part.split('-')[:10]  # Tomar las primeras 10 palabras
        shortened_title = ' '.join(title_words) + ('-..' if len(title_part.split('-')) > 10 else '')
        return shortened_title
    return url  # Si no se puede extraer el título, devolver la URL completa

def draw_graph(graph):
    plt.figure(figsize=(15, 12))
    pos = nx.spring_layout(graph, k=0.3, iterations=50)
    edge_weights = nx.get_edge_attributes(graph, 'weight')
    
    # Crear etiquetas con títulos cortos
    labels = {node: extract_title_from_url(node) for node in graph.nodes()}
    
    # Dibujar nodos y bordes
    nx.draw_networkx_nodes(graph, pos, node_size=300, node_color='magenta', alpha=0.8)
    nx.draw_networkx_edges(graph, pos, width=[edge_weights[e] for e in graph.edges()], alpha=0.5, arrows=True)
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=8)  # Usar las etiquetas personalizadas

    # Dibujar pesos (opcional)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_weights, font_size=7)

    plt.title("Grafo de Referencias entre Noticias Deportivas", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("grafo_noticias.png", dpi=300)
    plt.show()

# Configuración principal
base_url = "https://www.infobae.com"
start_url = "https://www.infobae.com/deportes"
max_depth = 2

# Paso 1: Obtener noticias principales
print("Obteniendo noticias principales...")
href_base = get_html_base(start_url)
news_urls = [urljoin(base_url, href) for href in href_base[:30] if href]  # Limitar a 30 noticias para el grafo

# Paso 2: Crawling para recolectar URLs
print("\nRealizando crawling...")
collected_urls_total_set = set()
collected_urls_total = []

for href in href_base[:30]:  # Usar las mismas 30 noticias para consistencia
    full_url = urljoin(base_url, href)
    if full_url not in collected_urls_total_set:
        collected_urls_total.append((full_url, 0))
        collected_urls_total_set.add(full_url)

    print(f"\n************ Link Noticia Principal: {full_url} ************")
    collected_urls = crawl(full_url, max_depth)
    for url, depth in collected_urls:
        if url not in collected_urls_total_set:
            collected_urls_total.append((url, depth))
            collected_urls_total_set.add(url)

# Guardar las URLs recolectadas en Excel
print("\nGuardando URLs recolectadas...")
save_to_excel(collected_urls_total, "collected_urls.xlsx")

# Paso 3: Construir y visualizar el grafo
print("\nConstruyendo grafo de referencias...")

print(f"Total de URLs para el grafo: {len(collected_urls_total)}")
#urls_para_grafo = [url for url, depth in collected_urls_total] 
grafo = build_graph(collected_urls_total, base_url)
save_graph(grafo)
draw_graph(grafo)

print("\n*** Proceso completado exitosamente ***")