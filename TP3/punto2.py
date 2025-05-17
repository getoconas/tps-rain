import requests # requests es una biblioteca para realizar solicitudes HTTP
from bs4 import BeautifulSoup # BeautifulSoup es una biblioteca para analizar documentos HTML y XML
import nltk

# Descargar datos necesarios para NLTK
nltk.download('punkt')
nltk.download('stopwords')

# URL de la sección de economía de Infobae
url = 'https://www.infobae.com/economia/'

# Realizar la solicitud HTTP a la página web
response = requests.get(url)
print(response)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
  soup = BeautifulSoup(response.content, 'html.parser') # Crear un objeto BeautifulSoup para analizar el contenido HTML
  #print(soup)

  # Encontrar las noticias
  arrayNews = soup.find_all('a', class_='story-card-ctn') # Encontrar todas las etiquetas <a> con la clase 'story-card-ctn'
  print(arrayNews)
  
  textos = []

  print("------------------------")
  for i, news in enumerate(arrayNews[:10], start = 1):
    print(f"Noticia {i}:")
    print(news)
    # URL de la noticia
    news_href = news.get('href')
    print('Href:', news_href)
    
