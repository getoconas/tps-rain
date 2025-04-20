# TP2 - Punto 5

# NTLK
import nltk
from nltk.data import find # Para verificar si el corpus está descargado
from nltk.corpus import brown # Para el corpus de Brown

import re # Para expresiones regulares

try:
  find('corpora/brown')
except nltk.download.DownloadError: # Si el corpus no está descargado, lo descargamos
  try:
    nltk.download('brown')
    print("El corpus 'brown' se ha descargado exitosamente.")
  except Exception as e:
    print(f"Error al descargar el corpus 'brown': {e}")

files = brown.fileids() # Obtener los nombres de los archivos en el corpus
text_tokenized = brown.words('cg73') # Tokenizar el texto del archivo 'cg73' del corpus de Brown

text_constructed= ' '.join(text_tokenized)
text_constructed = re.sub(r'\s([.,!?;:\'"])', r'\1', text_constructed) # Elimina espacios antes de puntuación
text_constructed = re.sub(r'([([{«<])\s', r'\1', text_constructed) # Elimina espacios después de paréntesis/corchetes de apertura
text_constructed = re.sub(r'\s([)\]}>»])', r'\1', text_constructed) # Elimina espacios antes de paréntesis/corchetes de cierre
text_constructed = re.sub(r'(``)\s', r"''", text_constructed) # Elimina espacios después de comillas dobles

print("------------------------------------------------------------------")
print('   *** Texto cg73 construido totalmente ***')
print("------------------------------------------------------------------")
print(text_constructed)
print("------------------------------------------------------------------")

prayers_tokenized = nltk.sent_tokenize(text_constructed) # Especifica el idioma si es diferente al inglés

# Imprimir las oraciones tokenizadas
print("------------------------------------------------------------------")
print("   *** 10 primeras oraciones del texto cg73 ***")
print("------------------------------------------------------------------")
for i, prayer in enumerate(prayers_tokenized[:10]):
  num = i + 1  # Los índices comienzan en 0, así que sumamos 1
  print(f"{num}: {prayer}")
print("------------------------------------------------------------------")

print("   *** Fin del programa ***") # Mensaje de finalización del programa
