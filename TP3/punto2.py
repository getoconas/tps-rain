import re # re es una biblioteca para trabajar con expresiones regulares
import requests # requests es una biblioteca para realizar solicitudes HTTP
from bs4 import BeautifulSoup # BeautifulSoup es una biblioteca para analizar documentos HTML y XML
from unidecode import unidecode # unidecode es una biblioteca para convertir caracteres Unicode a ASCII
import nltk

# Descargar datos necesarios para NLTK
nltk.download('punkt')
nltk.download('stopwords')

# URL de la sección de economía de Infobae
url = 'https://www.infobae.com/economia/'

# Función para obtener los detalles de la noticia que se manda por la URL
def get_details_news(url):
  response = requests.get(url) # Realizar la solicitud HTTP a la página web
  if response.status_code == 200: # Verificar si la solicitud fue exitosa (código de estado 200)
    soup = BeautifulSoup(response.content, 'html.parser') # Crear un objeto BeautifulSoup para analizar el contenido HTML

    # Titulo de la noticia
    title_element_news = soup.find('h1', class_='display-block article-headline text_align_left').text.strip() 
    title_news = unidecode(title_element_news).lower() if title_element_news else "*** No se encontro titulo de la noticia ***" # Convertir el título a ASCII, eliminar acentos y convertir a minúsculas
    #print('*** Titulo noticia: ***', title_news)

    # Resumen de la noticia
    summary_element_news = soup.find('h2', class_='article-subheadline text_align_left').text.strip()
    summary_news = unidecode(summary_element_news).lower() if summary_element_news else "*** No se encontro resumen de la noticia ***"
    #print('*** Resumen noticia: ***', summary_news)

    # Contenido de la noticia
    content_element_news = soup.find('div', class_='body-article')

    if content_element_news:
      content = content_element_news.find_all(['p', 'h2'])
      content_news = [unidecode(c.get_text(separator=" ", strip=True)).lower() for c in content]
      #print (content_news)

    # Imagenes dentro de la noticia
    images_news = []
    if content_element_news:
      images_element_news = content_element_news.find_all('img')
      for img in images_element_news:
        img_url = img.get('src')
        if img_url:
          images_news.append(img_url)
    
    #print('*** Imagenes noticia: ***', images_news)

    # Eliminar signos de puntuacion del titulo, resumen y contenido
    title_news = re.sub(r'[^\w\s]', '', title_news)
    summary_news = re.sub(r'[^\w\s]', '', summary_news)
    content_news = [re.sub(r'[^\w\s]', '', c) for c in content_news]
    content_total_news = ""
    for i in range(len(content_news)):
      content_total_news += content_news[i] + " "

    print("------------------------------------------------------------------------------------------------------------")
    print('*** Titulo noticia: ***', title_news)
    print('*** Resumen noticia: ***', summary_news)
    print('*** Contenido noticia: ***', content_total_news)


# Programa principal
# Realizar la solicitud HTTP a la página web
response = requests.get(url)
#print(response)

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
  soup = BeautifulSoup(response.content, 'html.parser') # Crear un objeto BeautifulSoup para analizar el contenido HTML
  arrayNews = soup.find_all('a', class_='story-card-ctn') # Encontrar todas las etiquetas <a> con la clase 'story-card-ctn'
  
  textos = []

  for i, news in enumerate(arrayNews[:2], start = 1):
    print(f"Noticia {i}:")
    # URL de la noticia
    news_href = news.get('href')
        
    if news_href:
      if not news_href.startswith('http'):
        news_href = 'https://www.infobae.com' + news_href
        print('*** vinculo noticia: ***', news_href)
        get_details_news(news_href)
        print("------------------------------------------------------------------------------------------------------------")

