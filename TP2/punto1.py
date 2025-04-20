# TP2 - Punto 1

# NTLK
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import FreqDist

import matplotlib.pyplot as plt # Para mostrar el grafico
import unicodedata

# Texto
text = """
Los sistemas recomendadores son herramientas enfocadas a ayudar a los usuarios a obtener aquella información que mejor se corresponda con sus intereses y preferencias. Mientras que un buscador habitual se centra en encontrar aquello que el usuario solicita, un sistema recomendador ayuda al usuario a tomar una decisión, que puede ser la compra de un producto en un portal de comercio electrónico, la lectura de un libro, la revisión de un artículo científico, el acceso a una página web en específico, o el estudio de determinado recurso educativo en una plataforma virtual de aprendizaje.
La clasificación más popular de los sistemas recomendadores está asociada al algoritmo que emplean para realizar la tarea de minería correspondiente y divide a los métodos de recomendación en métodos de filtrado basado en el contenido, métodos de filtrado colaborativo, métodos de filtrado demográfico y métodos híbridos [1-4]. En adición, la literatura ha desarrollado tanto sistemas recomendadores para la sugerencia de ítems para usuarios individuales, como enfocados en grupos de usuarios []. Así, los sistemas recomendadores enfocados en grupos de usuarios se centran en la sugerencia de determinados tipos de ítems que tienden a ser consumidos en grupos y no por usuarios individuales, tales como programas de televisión y paquetes turísticos [].
De manera general, los dominios iniciales de aplicación de los sistemas recomendadores han sido el e-commerce[]y el e-learning[, ], aunque en los últimos tiempos estos sistemas están siendo aplicados a escenarios cada vez más diversos []. Así, son relevantes las aplicaciones de los sistemas recomendadores en escenarios de e-health[] y de e-tourism[], como dos contextos relevantes de particular importancia.
Específicamente, resulta importante en los últimos años el desarrollo de sistemas recomendadores en el dominio del turismo[]. En este dominio existe mucha información en línea disponible y por tanto los sistemas recomendadores juegan un papel muy importante con vistas a ayudar a los usuarios en la toma de decisiones sobre qué paquete turístico comprar, qué instalación hotelera visitar, o qué recorrido turístico elegir, entre otras decisiones similares a tomar con vistas a lograr la satisfacción final del cliente [].
"""

puntuactions = "][:!.,;?[]"

words_tokenize = word_tokenize(text.lower()) # Tokenizar el texto y convertirlo a minúsculas
words_tokenize = [word for word in words_tokenize if word not in puntuactions]

# Quitar acentos y letras "ñ" de las palabras tokenizadas
words_tokenize = [unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore').decode('utf-8') for word in words_tokenize]

# Eliminar las stopwords del texto
stop_words = set(stopwords.words('spanish'))
words_filtered = [w for w in words_tokenize if not w.lower() in stop_words]
words_filtered = []

for w in words_tokenize:
  if w not in stop_words:
    words_filtered.append(w)

#Obtener las frecuencias luego de la tokenizacion y quitar las stopwords
frecuency = FreqDist(words_filtered)

# Ordenar las frecuenncia en orden descendente
frecuency_ordered = dict(sorted(frecuency.items(), key = lambda item: item[1], reverse = True))

# Mostrar las frecuencias
print("   *** Terminos mas frecuentes ***")
for word, freq in frecuency_ordered.items():
  print(f"{word}: {freq}")

# Mostrar gráfico con los 20 términos más frecuentes
top_20 = frecuency.most_common(20)
labels, values = zip(*top_20) # Desempaquetar los valores
plt.figure(figsize = (10, 6)) # Definir el tamaño de la figura
plt.bar(labels, values) # Crear el grafico de barras
plt.xticks(rotation = 45, ha = 'right') # Rotar las etiquetas del eje x
plt.title("Top 20 terminos mas frecuentes") # Titulo del grafico
plt.xlabel("Terminos") # Etiqueta del eje x
plt.ylabel("Frecuencia") # Etiqueta del eje y
plt.show() # Mostrar el grafico

print("   *** Fin del programa ***") # Mensaje de finalización del programa
