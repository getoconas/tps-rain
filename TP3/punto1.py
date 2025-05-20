import requests
from bs4 import BeautifulSoup

# Metodo para obtener los enlaces que hace referencia a deportes en la pagina de infobae
def get_html_base(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.text, 'html.parser')

  # Extraer enlaces de la página
  array_links = [a for a in soup.find_all('a', class_='story-card-ctn') if a.get('class') == ['story-card-ctn']] # Encontrar todas las etiquetas <a> con la clase 'story-card-ctn' y asegurarse de que la clase sea exactamente 'story-card-ctn'
  hrefs = []

  for i, news in enumerate(array_links[:30], start = 1):
    href = news.get('href') # href de la noticia
    hrefs.append(href)
  return hrefs

def crawl(url, depth):
  if depth == 0:
    return
  try:
    print("Desarrollo del crawling...")
  except Exception as e:
    print(f"Error al procesar {url}: {e}")

# Iniciar el crawling desde la URL inicial con una profundidad máxima de 2
start_url = "https://www.infobae.com/deportes"
max_depth = 2
href_base = get_html_base(start_url)

for href in href_base:
  print(start_url + href)
  # Aquí se puede llamar a la función crawl para cada URL base
  # crawl(url, max_depth)

