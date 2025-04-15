# TP1 - Punto 3 - Fichero Invertido Posicional con Hilos
import fitz  # Manipular archivos PDF
from unidecode import unidecode  # Eliminar acentos y caracteres especiales
import re  # Expresiones regulares
import threading  # Hilos para procesamiento concurrente
pdf_files = ["Doc1.pdf","Doc2.pdf","Doc3.pdf","Doc4.pdf","Doc5.pdf"]
def read_pdf_with_positions(file_name):
    document = fitz.open(file_name)  # Abre el archivo PDF
    text = ""
    positions = {}
    word_index = 0
    for page in document:
        page_text = page.get_text("words")  # Extrae las palabras con su información de posición
        for item in page_text:
            word = item[4]  # La palabra en sí
            cleaned_word = re.sub(r"[^\w\s]", "", unidecode(word.lower()))
            if cleaned_word:
                if cleaned_word not in positions:
                    positions[cleaned_word] = []
                positions[cleaned_word].append(word_index)
                word_index += 1
        text += page.get_text()  # También extraemos el texto completo para stopwords
    return text, positions  # Devolvemos el texto completo y las posiciones

def load_stopwords(stopwords_file):
    with open(stopwords_file, "r", encoding="utf-8") as file:
        stopwords = [line.strip() for line in file]  # Carga las stopwords desde el archivo
    return stopwords  # Devuelve la lista de stopwords

def remove_stopwords_for_positions(positions, stopwords):
    filtered_positions = {}
    for word, pos_list in positions.items():
        if word not in stopwords:
            filtered_positions[word] = pos_list
    return filtered_positions

positional_dictionary = {}  # Diccionario para almacenar las palabras y sus posiciones
sem_positional = threading.Semaphore(1)  # Semáforo para acceso seguro al diccionario posicional

def load_positional_dictionary(positions, name, positional_dictionary, sem):
    for word, pos_list in positions.items():
        sem.acquire()  # Adquiere el semáforo para acceso seguro al diccionario
        if word in positional_dictionary:
            positional_dictionary[word].append([name, pos_list])
        else:
            positional_dictionary[word] = [[name, pos_list]]
        sem.release()  # Libera el semáforo

def read_pdf_thread_positional(location, name, positional_dictionary, sem):
    file_name = location
    pdf_text, word_positions = read_pdf_with_positions(file_name)

    stopwords_file = "spanish.txt"  # Archivo de stopwords en español
    stopwords = load_stopwords(stopwords_file)  # Carga las stopwords

    filtered_positions = remove_stopwords_for_positions(word_positions, stopwords)

    load_positional_dictionary(filtered_positions, name, positional_dictionary, sem)

thread1_pos = threading.Thread(target=read_pdf_thread_positional, args=("Doc1.pdf", "Doc1", positional_dictionary, sem_positional))
thread2_pos = threading.Thread(target=read_pdf_thread_positional, args=("Doc2.pdf", "Doc2", positional_dictionary, sem_positional))
thread3_pos = threading.Thread(target=read_pdf_thread_positional, args=("Doc3.pdf", "Doc3", positional_dictionary, sem_positional))
thread4_pos = threading.Thread(target=read_pdf_thread_positional, args=("Doc4.pdf", "Doc4", positional_dictionary, sem_positional))
thread5_pos = threading.Thread(target=read_pdf_thread_positional, args=("Doc5.pdf", "Doc5", positional_dictionary, sem_positional))

thread1_pos.start()
thread2_pos.start()
thread3_pos.start()
thread4_pos.start()
thread5_pos.start()

thread1_pos.join()
thread2_pos.join()
thread3_pos.join()
thread4_pos.join()
thread5_pos.join()

print("\nFichero Invertido Posicional:")
for word, items in positional_dictionary.items():
    print(f"{word}: {items}")

print("\n--- Consultas ---")

def search_phrase(phrase, positional_dictionary):
    stopwords = load_stopwords("spanish.txt")
    words = [re.sub(r"[^\w\s]", "", unidecode(word.lower())) for word in phrase.split() if word.lower() not in stopwords]

    if not words:
        return "No se encontraron términos relevantes en la consulta."

    if words[0] not in positional_dictionary:
        return f"No se encontraron ocurrencias de la frase '{phrase}'."

    results = {}

    for doc_name, positions in positional_dictionary[words[0]]:
        for start_pos in positions:
            match = True
            for i, word in enumerate(words[1:], start=1):
                expected_pos = start_pos + i
                if word not in positional_dictionary or not any(
                    doc == doc_name and expected_pos in pos_list
                    for doc, pos_list in positional_dictionary[word]
                ):
                    match = False
                    break
            if match:
                results.setdefault(doc_name, []).append(list(range(start_pos, start_pos + len(words))))

    return results if results else f"No se encontraron ocurrencias de la frase  '{phrase}'."


def word_frequency(positional_dictionary, word):
    normalized_word = re.sub(r"[^\w\s]", "", unidecode(word.lower()))
    results = {}

    # Verifica si la palabra existe en el diccionario posicional
    if normalized_word in positional_dictionary:
        for document, positions in positional_dictionary[normalized_word]:
            results[document] = len(positions)  # Cuenta cuántas veces aparece en cada documento
    else:
        print(f"La palabra '{word}' no se encuentra en el diccionario.")
    
    return results

def proximity_query(positional_dictionary, word1, word2, max_distance):
    word1 = re.sub(r"[^\w\s]", "", unidecode(word1.lower()))
    word2 = re.sub(r"[^\w\s]", "", unidecode(word2.lower()))
    
    nearby_documents = []

    if word1 not in positional_dictionary or word2 not in positional_dictionary:
        print(f"Una o ambas palabras no están en el diccionario.")
        return nearby_documents

    occurrences_word1 = {doc: pos for doc, pos in positional_dictionary[word1]}
    occurrences_word2 = {doc: pos for doc, pos in positional_dictionary[word2]}

    common_documents = set(occurrences_word1.keys()) & set(occurrences_word2.keys())

    for doc in common_documents:
        positions1 = occurrences_word1[doc]
        positions2 = occurrences_word2[doc]

        for p1 in positions1:
            for p2 in positions2:
                if abs(p1 - p2) <= max_distance:
                    nearby_documents.append(doc)
                    break  
            else:
                continue
            break

    return nearby_documents

# Realizar 4 consultas distintas
#quest1 = "arxiv"
print("\nConsulta 1: ")
quest1 = input("Ingrese la palabra de la cual quiere saber la frecuencia en los documentos: ")
frequencies = word_frequency(positional_dictionary, quest1)
if len(frequencies)!=0:
    print(f"\nEn que documentos aparece '{quest1}' y con que frecuencia?")
    for doc, freq in frequencies.items():
        print(f"- {doc}: {freq} veces")

#quest2 = proximity_query(positional_dictionary, "aprendizaje", "automático", 5)
print("\nConsulta 2: ")
word1, word2=input("Ingrese las palabras de la cuales quiere saber si son proximas en el documento separadas por un espacio: ").split()
distance=int(input("Ingrese la distancia maxima entre las cuales pueden estar el par de palabras ingresadas: "))
quest2 = proximity_query(positional_dictionary, word1, word2, distance)
if quest2:
    print(f"\nDocumentos donde {word1} aparece cerca de {word2} (máx. {distance} palabras):")
    for doc in quest2:
        print(f"- {doc}")

#quest3 = "inteligencia artificial"
quest3 = input("\nIngrese la palabra o frase de la cual quiere saber la posicion en los documentos: ")
response3 = search_phrase(quest3, positional_dictionary)
print(f"\nConsulta 3: '{quest3}'")
print(f"Resultados: {response3}")

#quest4 = "aprendizaje automático"
quest4 = input("\nIngrese la palabra o frase de la cual quiere saber la posicion en los documentos: ")
response4 = search_phrase(quest4, positional_dictionary)
print(f"\nConsulta 4: '{quest4}'")
print(f"Resultados: {response4}")

