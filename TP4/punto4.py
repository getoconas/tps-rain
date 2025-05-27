from sickle import Sickle # Importar Sickle para OAI-PMH
import pandas as pd
from datetime import datetime

# Conexión con CORA con el protocolo OAI-PMH
sickle = Sickle('https://dataverse.csuc.cat/oai')

# inicializacion del iterador de registros
records = sickle.ListRecords(metadataPrefix='oai_dc')
iterator = iter(records) # Crear un iterador para recorrer los registros

data = []
count = 0

print("Iniciando la recolección...")
while count < 100:
  try:
    record = next(iterator) 
    metadata = record.metadata # Obtener los metadatos del registro
    title = metadata.get('title', [''])[0]
    description = metadata.get('description', [''])[0]
    author = '; '.join(metadata.get('creator', []))
    keywords = '; '.join(metadata.get('subject', []))
    date = metadata.get('date', [''])[0]

    data.append(
      {
        'title': title,
        'description': description,
        'author': author,
        'keywords': keywords,
        'date': date
      }
    )
    count += 1
    print(f" Se agregaron {count} registros")
  
  except StopIteration:
    print("No hay más registros disponibles.")
    break

  except Exception as e:
    print(f"Registro omitido por un error")
    continue
 
# Guardar en CSV
df = pd.DataFrame(data)
filename = f'metadata_cora_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
df.to_csv(filename, index=False, encoding='utf-8-sig')

print(f"Archivo CSV generado con {count} registros en {filename}")
