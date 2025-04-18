# TP2 - Punto 4

import re
from nltk.corpus import stopwords 
import unicodedata 
from nltk import ngrams

text = """
Los sistemas recomendadores son herramientas enfocadas a ayudar a los usuarios a obtener aquella información que mejor se corresponda con sus intereses y preferencias. Mientras que un buscador habitual se centra en encontrar aquello que el usuario solicita, un sistema recomendador ayuda al usuario a tomar una decisión, que puede ser la compra de un producto en un portal de comercio electrónico, la lectura de un libro, la revisión de un artículo científico, el acceso a una página web en específico, o el estudio de determinado recurso educativo en una plataforma virtual de aprendizaje.
"""

text = text.replace('[','').replace(']','').replace('.','').replace(',','') #.replace('-','')

# Texto normalizado y sin acentos
text_normalized = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')

stopwords = set(stopwords.words('spanish')) # Obtener las stop words en español

words = text_normalized.split() # Dividir el texto en palabras

words_filtered = [word for word in words if word.lower() not in stopwords] # Eliminar las stop words

# Mostrar el resultado
print("------------------------------------------------------------------")
print("   Texto normalizado y filtrado   ")
print("------------------------------------------------------------------")
print(' '.join(words_filtered))
print("------------------------------------------------------------------")

# Obtener los bigramas
bigrams = list(ngrams(words_filtered, 2))

# Obtener los trigramas
trigrams = list(ngrams(words_filtered, 3))

# Mostrar los resultados obtenidos de bigrama y trigrama

print("   *** Bigramas ***  ")
for bigram in bigrams:
  print(' '.join(bigram))
print("------------------------------------------------------------------")
print("  *** Trigramas ***  ")
for trigram in trigrams:
  print(' '.join(trigram))

print("------------------------------------------------------------------")
print("Fin del programa") # Mensaje de finalización del programa
