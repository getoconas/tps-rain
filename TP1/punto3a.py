# TP1 - Punto 3
# Fichero invertido por frecuencia

import fitz # Manipular archivos PDF
from unidecode import unidecode # Eliminar acentos y caracteres especiales
import re # Expresiones regulares
import threading # Hilos para procesamiento concurrente

def read_pdf(file_name):
  document = fitz.open(file_name) # Abre el archivo PDF
  text = ""
  for page in document:
    text += page.get_text() # Extrae el texto de cada página
  return text # Devuelve el texto completo del PDF

def load_stopwords(stopwords_file):
  with open(stopwords_file, "r", encoding="utf-8") as file:
    stopwords = [line.strip() for line in file] # Carga las stopwords desde el archivo
  return stopwords # Devuelve la lista de stopwords

def remove_stopwords(text, stopwords):
  # Remueve caracteres especiales y convierte a minúsculas sin acentos
  text = re.sub(r"[^\w\s]", "", unidecode(text.lower()))
  words = text.split() # Divide el texto en palabras
  filtered_words = [word for word in words if word not in stopwords] # Filtra las stopwords
  filtered_text = " ".join(filtered_words) # Une las palabras filtradas en un solo string
  return filtered_text # Devuelve el texto filtrado

dictionary = {} # Diccionario para almacenar las palabras y sus conteos
sem = threading.Semaphore(1) # Semáforo para acceso seguro al diccionario

def load_dictionary(text, name, dictionary, sem):
  words = text.split() # Divide el texto en palabras
  word_count = {} # Diccionario para contar las palabras

  for word in words:
    word_count[word] = word_count.get(word, 0) + 1 # Cuenta la frecuencia de cada palabra
    
  for word, count in word_count.items(): 
    sem.acquire() # Adquiere el semáforo para acceso seguro al diccionario
    if word in dictionary:
      dictionary[word].append([name, count]) # Agrega la palabra y su conteo al diccionario
    else:
      dictionary[word] = [[name, count]] # Crea una nueva entrada en el diccionario
    sem.release() # Libera el semáforo

def read_pdf_thread(location, name, dictionary, sem):
  file_name = location 
  pdf_text = read_pdf(file_name) # Lee el PDF
  
  stopwords_file = "spanish.txt"  # Archivo de stopwords en español
  stopwords = load_stopwords(stopwords_file) # Carga las stopwords
  text = remove_stopwords(pdf_text, stopwords) # Remueve las stopwords del texto del PDF
  load_dictionary(text, name, dictionary, sem) # Carga el texto filtrado en el diccionario

thread1 = threading.Thread(target = read_pdf_thread, args = ("Doc1.pdf", "Doc1.pdf", dictionary, sem))
thread2 = threading.Thread(target = read_pdf_thread, args = ("Doc2.pdf", "Doc2.pdf", dictionary, sem))
thread3 = threading.Thread(target = read_pdf_thread, args = ("Doc3.pdf", "Doc3.pdf", dictionary, sem))
thread4 = threading.Thread(target = read_pdf_thread, args = ("Doc4.pdf", "Doc4.pdf", dictionary, sem))
thread5 = threading.Thread(target = read_pdf_thread, args = ("Doc5.pdf", "Doc5.pdf", dictionary, sem))

thread1.start() # Inicia el hilo 1
thread2.start() # Inicia el hilo 2
thread3.start() # Inicia el hilo 3
thread4.start() # Inicia el hilo 4
thread5.start() # Inicia el hilo 5

thread1.join() # Espera a que el hilo 1 termine
thread2.join() # Espera a que el hilo 2 termine
thread3.join() # Espera a que el hilo 3 termine
thread4.join() # Espera a que el hilo 4 termine
thread5.join() # Espera a que el hilo 5 termine
# El diccionario contiene las palabras y sus conteos

print("\nFichero Invertido por Frecuencia:")
for word, items in dictionary.items():
  print(word, items) # Imprime el diccionario con las palabras y sus conteos
# El formato de salida es: palabra: [[nombre_del_documento, conteo], ...]

print("Fin del programa") # Mensaje de finalización del programa