import nltk
from nltk.corpus import inaugural
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string

nltk.download('inaugural')

# Cargar discurso inaugural de Obama
inaugural_obama = inaugural.raw('2009-Obama.txt') # Obtener el discurso inaugural de Obama de 2009 con raw()

# Tokenizar el discurso
tokens_obama = nltk.sent_tokenize(inaugural_obama)

# Metodo 1 - TF-IDF con algoritmos de clasificación
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(tokens_obama) # Matriz TF-IDF de las oraciones
similarity_matrix = cosine_similarity(X, X) # Matriz para calcular similitudes
sentence_scores_tfidf = similarity_matrix.sum(axis=1) # Suma de similitudes por oración
top_sentence_indices_tfidf = sentence_scores_tfidf.argsort()[-10:][::-1] # Top 10 oraciones
top_sentence_tfidf = [tokens_obama[i] for i in sorted(top_sentence_indices_tfidf)] # Oraciones más relevantes
summary_tfidf = ' '.join(top_sentence_tfidf) # Resumen con TF-IDF

# Metodo 2 - Clasificacion por puntuacion de frases basada en frecuencia de palabras claves
stopwords = stopwords.words('english')
punctuation = set(string.punctuation)
words_obama = nltk.word_tokenize(inaugural_obama)
filtered_words_obama = [word.lower() for word in words_obama if word.lower() not in stopwords and word not in punctuation]
word_freq_obama = nltk.FreqDist(filtered_words_obama) # Frecuencia de palabras
sentence_scores_freq = {}

for sentence in tokens_obama: # Tokenizar oraciones
  words_in_sentence = nltk.word_tokenize(sentence)
  score = sum(word_freq_obama[word] for word in words_in_sentence if word in word_freq_obama)
  sentence_scores_freq[sentence] = score

top_sentences_freq = sorted(sentence_scores_freq, key=sentence_scores_freq.get, reverse=True)[:10] # Top 10 oraciones
summary_freq = ' '.join(top_sentences_freq) # Resumen con frecuencia de palabras

# Imprimir resúmenes
print("********** Resumen con TF-IDF **********")
print(summary_tfidf)
print("\n********** Resumen con frecuencia de palabras **********")
print(summary_freq)