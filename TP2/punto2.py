# TP2 - Punto 2

# NTLK
from nltk.stem import PorterStemmer, LancasterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from tabulate import tabulate

# Texto
text = """
Information retrieval is the process of obtaining relevant information from a collection of data. It involves searching for and retrieving information from various sources, such as databases, the Internet, and digital libraries. Information retrieval is a vital aspect of many fields, including business, education, and healthcare. In recent years, technological advances have led to the development of sophisticated information retrieval systems that use artificial intelligence and machine learning algorithms to provide more efficient and accurate results. These systems can understand natural language queries and retrieve information from large and complex data sets. As the amount of data available continues to grow exponentially, the need for effective information retrieval systems becomes increasingly important. Organizations are constantly seeking ways to improve their information retrieval processes to gain a competitive edge and make better-informed decisions. With the right tools and strategies, information retrieval can provide valuable insights and help drive success in various industries. 
"""

text = text.replace('.','').replace(',','')

# Tokenizar el texto 
words_tokenize = word_tokenize(text.lower())

# Eliminar las stopwords del texto
stop_words = set(stopwords.words('english'))
words_filtered = [w for w in words_tokenize if not w.lower() in stop_words]

#print(words_filtered)

# Inicializar los stemmers
porter = PorterStemmer()
lancaster = LancasterStemmer()

# Realizar el stemming con ambos algoritmos
porter_stems = [porter.stem(token) for token in words_filtered]
lancaster_stems = [lancaster.stem(token) for token in words_filtered]

# Crear una lista de listas para la tabla
tabla_data = zip(words_filtered, porter_stems, lancaster_stems)

# Definir los encabezados de la tabla
headers = ["Termino", "Porter", "Lancaster"]

# Imprimir la tabla en formato encolumnado
print(tabulate(tabla_data, headers = headers, tablefmt = "grid"))

print("Fin del programa") # Mensaje de finalización del programa