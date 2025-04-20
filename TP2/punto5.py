import re
import nltk
from nltk.corpus import stopwords 
import unicodedata 
try:
    nltk.data.find('corpora/brown')
except nltk.downloader.DownloadError:
    try:
        nltk.download('brown')
        print("El corpus 'brown' se ha descargado exitosamente.")
    except Exception as e:
        print(f"Error al descargar el corpus 'brown': {e}")

files = nltk.corpus.brown.fileids()
text_tokenized = nltk.corpus.brown.words('cg73')
# text_constructed111= ' '.join(text_tokenized)
# print('text construido111 totalmente')
# print(text_constructed111)
text_constructed= ' '.join(text_tokenized)
text_constructed = re.sub(r'\s([.,!?;:\'"])', r'\1', text_constructed)
text_constructed = re.sub(r'([([{«<])\s', r'\1', text_constructed) # Elimina espacios después de paréntesis/corchetes de apertura
text_constructed = re.sub(r'\s([)\]}>»])', r'\1', text_constructed) # Elimina espacios antes de paréntesis/corchetes de cierre
text_constructed = re.sub(r'^\s+``', r'``', text_constructed)

print("------------------------------------------------------------------")
print('Texto construido totalmente')
print("------------------------------------------------------------------")
print(text_constructed)
prayers_tokenized = nltk.sent_tokenize(text_constructed) # Especifica el idioma si es diferente al inglés

# Imprimir las oraciones tokenizadas
print("------------------------------------------------------------------")
print("Texto en oraciones")
print("------------------------------------------------------------------")
for i, prayer in enumerate(prayers_tokenized[:10]):
    num = i + 1  # Los índices comienzan en 0, así que sumamos 1
    print(f"{num}: {prayer}")