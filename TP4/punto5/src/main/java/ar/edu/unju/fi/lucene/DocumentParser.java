package ar.edu.unju.fi.lucene;

import org.apache.tika.exception.TikaException;
import org.apache.tika.metadata.Metadata;
import org.apache.tika.parser.AutoDetectParser;
import org.apache.tika.sax.BodyContentHandler;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

public class DocumentParser {
    public static String extractContent(File file) throws IOException, TikaException, SAXException {
        // Filtra por extensión si es necesario, aunque Tika es robusto
        String fileName = file.getName().toLowerCase();
        System.out.println("filename..." + fileName);
        //Verifica si el archivo tiene una extension compatible
        if (!(fileName.endsWith(".doc") || fileName.endsWith(".docx") ||
                fileName.endsWith(".pdf") || fileName.endsWith(".txt") ||
                fileName.endsWith(".html"))) {
            System.err.println("Tipo de archivo invalido: " + fileName);
            return null;
        }

        try (FileInputStream inputStream = new FileInputStream(file)) {
            AutoDetectParser parser = new AutoDetectParser();
            BodyContentHandler handler = new BodyContentHandler(-1);  //maneja el contenido con tamaño ilimitado
            Metadata metadata = new Metadata();

            parser.parse(inputStream, handler, metadata); //Tika analiza el archivo y extrae solo el texto

            return handler.toString();
        }
    }
}
