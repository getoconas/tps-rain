package ar.edu.unju.fi.lucene;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field.Store;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.tika.exception.TikaException;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;

public class DocumentIndexer {
    private Directory indexDirectory;
    private IndexWriter indexWriter;
    private StandardAnalyzer analyzer;

    public DocumentIndexer(String indexPath) throws IOException {

        this.indexDirectory = FSDirectory.open(Paths.get(indexPath));
        System.out.println("Indice creado en disco: " + indexPath);
        this.analyzer = new StandardAnalyzer(); 
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE_OR_APPEND);

        this.indexWriter = new IndexWriter(indexDirectory, config);
    }

    public void indexDocument(File file) throws IOException, TikaException, SAXException {
        String content = DocumentParser.extractContent(file);

        if (content != null && !content.trim().isEmpty()) {
            Document doc = new Document();

            doc.add(new StringField("path", file.getAbsolutePath(), Store.YES)); //guarda la ruta del archivo
            doc.add(new TextField("filename", file.getName(), Store.YES)); // guarda el nombre del archivo
            doc.add(new TextField("contents", content, Store.NO)); //Indexa el contenido pero no lo guarda

            indexWriter.addDocument(doc);
            System.out.println("Indexado: " + file.getName());
        } else {
            System.err.println("No se pudo extraer contenido de: " + file.getName());
        }
    }

    public void close() throws IOException {
        if (indexWriter != null) {
            indexWriter.close();
        }
        if (indexDirectory != null) {
            indexDirectory.close();
        }
    }

    public void createIndex(String directoryToIndex) {
        File folder = new File(directoryToIndex);
        if (!folder.isDirectory()) {
            System.err.println("La ruta proporcionada no es un directorio valido");
            return;
        }

        File[] files = folder.listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isFile()) {  // Solo procesa archivos, no subdirectorios
                    try {
                        indexDocument(file);
                    } catch (IOException | TikaException | SAXException e) {
                        System.err.println("Error indexando: " + file.getName());
                    }
                }
            }
        }
    }

}
