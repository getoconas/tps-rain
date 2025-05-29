from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import fitz  # PyMuPDF
from unidecode import unidecode
import re
import threading
import requests
from bs4 import BeautifulSoup
import time

# --- Funciones para cargar PDFs (sin eliminar stopwords todavía) ---
def read_pdf(file_name):
    """Lee un PDF y devuelve su texto en formato string."""
    document = fitz.open(file_name)
    text = ""
    for page in document:
        text += page.get_text()
    return text

def load_pdfs(pdf_files):
    """Carga múltiples PDFs en paralelo usando hilos."""
    docs = []
    
    def process_pdf(file_name):
        text = read_pdf(file_name)
        docs.append(text)
    
    threads = []
    for file_name in pdf_files:
        thread = threading.Thread(target=process_pdf, args=(file_name,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    return docs

# --- Función para eliminar stopwords (solo se usará en el análisis) ---
def load_stopwords(stopwords_file="spanish.txt"):
    """Carga stopwords desde un archivo."""
    with open(stopwords_file, "r", encoding="utf-8") as file:
        return set(line.strip() for line in file)

def remove_stopwords(text, stopwords):
    """Elimina stopwords de un texto."""
    words = re.findall(r'\b\w+\b', unidecode(text.lower()))
    return ' '.join(word for word in words if word not in stopwords)

# URL de la sección de economía de Infobae
url = 'https://www.infobae.com/economia/'

# Función para obtener los detalles de la noticia (igual a la que proporcionaste)
def get_details_news(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Titulo de la noticia
        title_element_news = soup.find('h1', class_='display-block article-headline text_align_left')
        title_news = unidecode(title_element_news.text.strip()).lower() if title_element_news else "*** No se encontro titulo de la noticia ***" 
        
        # Resumen de la noticia
        summary_element_news = soup.find('h2', class_='article-subheadline text_align_left')
        summary_news = unidecode(summary_element_news.text.strip()).lower() if summary_element_news else "*** No se encontro resumen de la noticia ***"

        # Contenido de la noticia
        content_element_news = soup.find('div', class_='body-article')
        if content_element_news:
            content = content_element_news.find_all(['p', 'h2'])
            content_news = [unidecode(c.get_text(separator=" ", strip=True)).lower() for c in content]

        # Eliminar signos de puntuacion
        title_news = re.sub(r'[^\w\s]', '', title_news)
        summary_news = re.sub(r'[^\w\s]', '', summary_news)
        content_news = [re.sub(r'[^\w\s]', '', c) for c in content_news]
        content_total_news = " ".join(content_news)
        
        return {
            'title': title_news,
            'summary': summary_news,
            'content': content_total_news
        }
    else:
        print(f"*** Error al obtener la noticia: {response.status_code} ***")
        return None

# Función para obtener y procesar las 10 noticias de economia
def get_economy_news():
    docs_repB = []
    
    # Realizar la solicitud HTTP a la página web
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        array_news = [a for a in soup.find_all('a', class_='story-card-ctn') 
                     if a.get('class') == ['story-card-ctn']][:10]  # Limitar a 10 noticias
        
        for i, news in enumerate(array_news, start=1):
            #print(f"Procesando noticia {i}/10...")
            news_url = news.get('href')
            
            if news_url:
                if not news_url.startswith('http'):
                    news_url = 'https://www.infobae.com' + news_url
                
                details_news = get_details_news(news_url)
                
                if details_news:
                    # Combinar título, resumen y contenido para el documento
                    doc = f"{details_news['title']}. {details_news['summary']}. {details_news['content']}"
                    docs_repB.append(doc)
                
                time.sleep(1)  # Espera para no saturar el servidor
            else:
                print(f"*** No se encontró URL para la noticia {i} ***")
                
    else:
        print(f"*** Error al obtener la página principal: {response.status_code} ***")
    
    return docs_repB

# RepB: Noticias económicas de Infobae
print("Extrayendo noticias económicas de Infobae...")
docs_repB = get_economy_news()

# --- Cargar documentos ---
# RepA: Desde PDFs (texto original)
pdf_files_repA = ["Doc1.pdf", "Doc2.pdf", "Doc3.pdf", "Doc4.pdf", "Doc5.pdf"]
docs_repA = load_pdfs(pdf_files_repA)  # Usa la función load_pdfs definida anteriormente

# --- Función principal para comparar documentos ---
def vectorize_and_query(docs, query_idx, **vectorizer_args):
    """Compara documentos usando TF-IDF y cosine similarity."""
    corpus = [doc for i, doc in enumerate(docs) if i != query_idx]
    query = docs[query_idx]
    
    if 'stop_words' in vectorizer_args and vectorizer_args['stop_words'] == 'custom':
        stopwords = load_stopwords()
        corpus = [remove_stopwords(doc, stopwords) for doc in corpus]
        query = remove_stopwords(query, stopwords)
        del vectorizer_args['stop_words']
    
    vectorizer = TfidfVectorizer(**vectorizer_args)
    tfidf_matrix = vectorizer.fit_transform(corpus + [query])
    
    cosine_similarities = cosine_similarity(tfidf_matrix[-1:], tfidf_matrix[:-1]).flatten()
    top_indices = cosine_similarities.argsort()[-3:][::-1]
    
    print("\n--- Configuración:", vectorizer_args, "---")
    print("***************************************************")
    print(f"Consulta (Documento {query_idx}):\n{query[:200]}\n")
    print("***************************************************")
    print("Top 3 documentos similares:")
    for idx in top_indices:
        print(f"\n[Score: {cosine_similarities[idx]:.4f}] Documento: {corpus[idx][:400]}")

# --- Análisis para RepA ---
print("****************************************")
print("\n=== Análisis para RepA ===")
print("****************************************")

print("\n🔹 a) Texto original")
vectorize_and_query(docs_repA, query_idx=0)  # Texto original
print("\n🔹 b) Sin stop-words")
vectorize_and_query(docs_repA, query_idx=0, stop_words='custom')  # Usa nuestra función remove_stopwords
print("\n🔹 c) Con bigramas")
vectorize_and_query(docs_repA, query_idx=0, ngram_range=(2, 2))  # Bigramas

# --- Análisis para RepB ---
print("****************************************")
print("\n\n=== Análisis para RepB ===")
print("****************************************")

print("\n🔹 a) Texto original")
vectorize_and_query(docs_repB, query_idx=0)
print("\n🔹 b) Sin stop-words")
vectorize_and_query(docs_repB, query_idx=0, stop_words='custom')
print("\n🔹 c) Con bigramas")
vectorize_and_query(docs_repB, query_idx=0, ngram_range=(2, 2))