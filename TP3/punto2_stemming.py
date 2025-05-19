import re # trabajar con expresiones regulares
import requests # realizar solicitudes HTTP
from bs4 import BeautifulSoup # analizar documentos HTML y XML
from unidecode import unidecode # convertir caracteres Unicode a ASCII
from collections import Counter # Counter sirve para contar elementos hashables
import matplotlib.pyplot as plt # para crear gráficos

import nltk
from nltk.tokenize import word_tokenize # word_tokenize para tokenizar texto
from nltk.corpus import stopwords # stopwords para filtrar palabras vacías

# Descargar datos necesarios para NLTK
nltk.download('punkt')
nltk.download('stopwords')

# URL de la sección de economía de Infobae
url = 'https://www.infobae.com/economia/'

# Función para obtener los detalles de la noticia que se manda por la URL
def get_details_news(url):
  response = requests.get(url) # Realizar la solicitud HTTP a la página web
  if response.status_code == 200: # Verificar si la solicitud fue exitosa (200 OK)
    soup = BeautifulSoup(response.content, 'html.parser') # Crear un objeto BeautifulSoup para analizar el contenido HTML

    # Titulo de la noticia
    title_element_news = soup.find('h1', class_='display-block article-headline text_align_left').text.strip() 
    title_news = unidecode(title_element_news).lower() if title_element_news else "*** No se encontro titulo de la noticia ***" 
    
    # Resumen de la noticia
    summary_element_news = soup.find('h2', class_='article-subheadline text_align_left').text.strip()
    summary_news = unidecode(summary_element_news).lower() if summary_element_news else "*** No se encontro resumen de la noticia ***"

    # Contenido de la noticia
    content_element_news = soup.find('div', class_='body-article')
    if content_element_news:
      content = content_element_news.find_all(['p', 'h2'])
      content_news = [unidecode(c.get_text(separator=" ", strip=True)).lower() for c in content]

    # Imagenes dentro de la noticia
    images_news = []
    if content_element_news:
      images_element_news = content_element_news.find_all('img')
      for img in images_element_news:
        img_url = img.get('src')
        if img_url:
          images_news.append(img_url)
    
    # Eliminar signos de puntuacion del titulo, resumen y contenido
    title_news = re.sub(r'[^\w\s]', '', title_news)
    summary_news = re.sub(r'[^\w\s]', '', summary_news)
    content_news = [re.sub(r'[^\w\s]', '', c) for c in content_news]
    content_total_news = ""
    for i in range(len(content_news)):
      content_total_news += content_news[i] + " "
    
    return {
      'title': title_news,
      'summary': summary_news,
      'content': content_total_news,
      'images': images_news
    }
  else:
    print(f"*** Error al obtener la noticia: {response.status_code} ***")
    return None 

# Programa Principal
# Realizar la solicitud HTTP a la página web
response = requests.get(url)

if response.status_code == 200: # Verificar si la solicitud fue exitosa (200 OK)
  soup = BeautifulSoup(response.content, 'html.parser') # Crear un objeto BeautifulSoup para analizar el contenido HTML
  arrayNews = soup.find_all('a', class_='story-card-ctn') # Encontrar todas las etiquetas <a> con la clase 'story-card-ctn'
  
  text = []

  for i, news in enumerate(arrayNews[:10], start = 1):
    print(f"---------- Noticia {i} ----------")
    
    news_url = news.get('href') # URL de la noticia
    
    if news_url:
      if not news_url.startswith('http'): # Verificar si la URL no comienza con 'http'
        news_url = 'https://www.infobae.com' + news_url
        details_news = get_details_news(news_url) # Obtener los detalles de la noticia en el metodo get_details_news
        if details_news:
          # Imprimir los detalles de la noticia
          print("Titulo: ", details_news['title'])
          print("Resumen: ", details_news['summary'])
          print("Cuerpo: ", details_news['content'])
          print("Imagenes: ", details_news['images'])
          print("\n")
          # Agregar a text para el analisis de los terminos frecuentes
          text.append(details_news['title'])
          text.append(details_news['summary'])
          text.append(details_news['content'])
        else:
          print("*** No se encontraron detalles de la noticia ***")
    else:
      print("*** No se encontro la URL de la noticia ***")
else:
  print(f"*** Error al obtener la página principal: {response.status_code} ***")
  
# Concatenar todas las noticias
text_complete = ' '.join(text)

# Tokenizar el texto
tokens = word_tokenize(text_complete)

# Filtrar stopwords
stop_words = set(stopwords.words('spanish'))
filtered_tokens = [word for word in tokens if word.isalnum() and word.lower() not in stop_words]

# Contar la frecuencia de cada palabra
frecuency_words = Counter(filtered_tokens)
most_common_words = frecuency_words.most_common(100)

# Mostrar los 100 términos más frecuentes
print("---------- Los 100 términos más frecuentes ----------")
for word, count in most_common_words:
  print(f"{word}: {count}")

# Crear el grafico de los 100 términos más frecuentes
word_graph = [word for word, _ in most_common_words]
frecuency_graph = [frecuency for _, frecuency in most_common_words]

print("\n*** Mostrando grafico de los 100 terminos mas frecuentes ***")
plt.figure(figsize=(15, 7))
plt.bar(word_graph, frecuency_graph)
plt.xticks(rotation=90)
plt.title('100 términos más frecuentes')
plt.xlabel('Terminos')
plt.ylabel('Frecuencia')
plt.show()

print("\n*** Fin del programa ***") # Mensaje de finalización del programa
