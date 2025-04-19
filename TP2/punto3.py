# TP2 - Punto 2

# NTLK
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from tabulate import tabulate
import unicodedata

# Texto
text = """
Los sistemas recomendadores son herramientas enfocadas a ayudar a los usuarios a obtener aquella información que mejor se corresponda con sus intereses y preferencias. 
Mientras que un buscador habitual se centra en encontrar aquello que el usuario solicita, un sistema recomendador ayuda al usuario a tomar una decisión, que puede ser la compra de un producto en un portal de comercio electrónico, la lectura de un libro, la revisión de un artículo científico, el acceso a una página web en específico, o el estudio de determinado recurso educativo en una plataforma virtual de aprendizaje.
La clasificación más popular de los sistemas recomendadores está asociada al algoritmo que emplean para realizar la tarea de minería correspondiente y divide a los métodos de recomendación en métodos de filtrado basado en el contenido, métodos de filtrado colaborativo, métodos de filtrado demográfico y métodos híbridos [1-4]. 
En adición, la literatura ha desarrollado tanto sistemas recomendadores para la sugerencia de ítems para usuarios individuales, como enfocados en grupos de usuarios []. 
Así, los sistemas recomendadores enfocados en grupos de usuarios se centran en la sugerencia de determinados tipos de ítems que tienden a ser consumidos en grupos y no por usuarios individuales, tales como programas de televisión y paquetes turísticos [].
De manera general, los dominios iniciales de aplicación de los sistemas recomendadores han sido el e-commerce[]y el e-learning[, ], aunque en los últimos tiempos estos sistemas están siendo aplicados a escenarios cada vez más diversos []. Así, son relevantes las aplicaciones de los sistemas recomendadores en escenarios de e-health[] y de e-tourism[], como dos contextos relevantes de particular importancia.
Específicamente, resulta importante en los últimos años el desarrollo de sistemas recomendadores en el dominio del turismo[]. En este dominio existe mucha información en línea disponible y por tanto los sistemas recomendadores juegan un papel muy importante con vistas a ayudar a los usuarios en la toma de decisiones sobre qué paquete turístico comprar, qué instalación hotelera visitar, o qué recorrido turístico elegir, entre otras decisiones similares a tomar con vistas a lograr la satisfacción final del cliente [].
"""

text = text.replace('[','').replace(']','').replace('.','').replace(',','')

# Tokenizar el texto 
words_tokenize = word_tokenize(text.lower())

# Quitar acentos y letras "ñ" de las palabras tokenizadas
words_tokenize = [unicodedata.normalize('NFKD', word).encode('ASCII', 'ignore').decode('utf-8') for word in words_tokenize]

# Eliminar las stopwords del texto
stop_words = set(stopwords.words('spanish'))
words_filtered = [w for w in words_tokenize if not w.lower() in stop_words]

#print(words_filtered)

# Inicializar los stemmers
porter = PorterStemmer()
lancaster = LancasterStemmer()

# Realizar el stemming con ambos algoritmos
porter_stems = [porter.stem(token) for token in words_filtered]
lancaster_stems = [lancaster.stem(token) for token in words_filtered]

#print(porter_stems)
print("------------------------------------------------------------------")
#print(lancaster_stems)

# Crear una lista de listas para la tabla
table_data = zip(words_filtered, porter_stems, lancaster_stems)

# Definir los encabezados de la tabla
headers = ["Termino", "Porter", "Lancaster"]

# Imprimir la tabla en formato encolumnado
print(tabulate(table_data, headers = headers, tablefmt = "grid"))

# Incializar el stemmer de español
snowball = SnowballStemmer('spanish')

# Realizar el stemming con el algoritmo Snowball
snowball_stems = [snowball.stem(token) for token in words_filtered]

print("------------------------------------------------------------------")
#print(snowball_stems)

# Crear una lista de listas para la tabla
table_data_snowball = zip(words_filtered, snowball_stems)

# Definir los encabezados de la tabla
headers = ["Termino", "Snowball"]

# Imprimir la tabla en formato encolumnado
print(tabulate(table_data_snowball, headers = headers, tablefmt = "grid"))

print("Fin del programa") # Mensaje de finalización del programa
