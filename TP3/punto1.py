import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def get_html_base(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        array_links = [a for a in soup.find_all('a', class_='story-card-ctn') if a.get('class') == ['story-card-ctn']]
        hrefs = [a.get('href') for a in array_links[:30]]
        return hrefs
    except requests.RequestException as e:
        print(f"*** Error al obtener la página base: {e} ***")
        return []

def get_referenced_news(url, base_url):
    """Obtiene enlaces a otras noticias desde una noticia"""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        referenced_urls = []
        array_news = soup.find_all('a', href=True)

        for news in array_news:
            href = news.get('href')
            if href and ('/deportes/' in href or '/sports/' in href):  # filtrar enlaces a otras noticias de deportes
                full_url = urljoin(base_url, href)
                referenced_urls.append(full_url)
        return referenced_urls
    except requests.RequestException as e:
        print(f"*** Error al obtener referencias desde la noticia: {e} ***")
        return []

def build_graph(news_urls, base_url):
    graph = nx.DiGraph()  # grafo dirigido

    for source_url in news_urls:
        print(f"Procesando noticia: {source_url}")
        referenced = get_referenced_news(source_url, base_url)
        for target_url in referenced:
            if target_url in news_urls:  # solo consideramos enlaces entre las 30 noticias principales
                if graph.has_edge(source_url, target_url):
                    graph[source_url][target_url]['weight'] += 1
                else:
                    graph.add_edge(source_url, target_url, weight=1)
    return graph

def save_graph(graph, filename="TP3/grafo_noticias.graphml"):
    nx.write_graphml(graph, filename)
    print(f"*** Grafo exportado a {filename} ***")

def draw_graph(graph):
    plt.figure(figsize=(15, 12))
    pos = nx.spring_layout(graph, k=0.3, iterations=50)  # distribución del grafo
    edge_weights = nx.get_edge_attributes(graph, 'weight')

    # Dibujar nodos y bordes
    nx.draw_networkx_nodes(graph, pos, node_size=300, node_color='skyblue', alpha=0.8)
    nx.draw_networkx_edges(graph, pos, width=[edge_weights[e] for e in graph.edges()], alpha=0.5, arrows=True)
    nx.draw_networkx_labels(graph, pos, font_size=8)

    # Dibujar pesos (opcional)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_weights, font_size=7)

    plt.title("Grafo de Referencias entre Noticias Deportivas", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("TP3/grafo_noticias.png", dpi=300)
    plt.show()
    
# MAIN
base_url = "https://www.infobae.com"
start_url = "https://www.infobae.com/deportes"

# Paso 1: obtener las 30 noticias
href_base = get_html_base(start_url)
news_urls = [urljoin(base_url, href) for href in href_base if href]

# Paso 2: construir el grafo de referencias entre noticias
grafo = build_graph(news_urls, base_url)

# Paso 3: exportar a archivo
save_graph(grafo)

# Llamar a la función luego de construir el grafo
draw_graph(grafo)

print("*** Fin del programa ***")
