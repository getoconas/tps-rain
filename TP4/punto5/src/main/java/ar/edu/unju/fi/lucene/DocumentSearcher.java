package ar.edu.unju.fi.lucene;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class DocumentSearcher {
    private IndexReader reader;
    private IndexSearcher searcher;
    private StandardAnalyzer analyzer;

    public DocumentSearcher(String indexPath, boolean useRAM) throws IOException {
        this.analyzer = new StandardAnalyzer();
        Directory indexDirectory;
        indexDirectory = FSDirectory.open(Paths.get(indexPath));
        this.reader = DirectoryReader.open(indexDirectory);
        this.searcher = new IndexSearcher(reader);
    }

    public List<SearchResult> search(String queryString, int maxResults) throws IOException, ParseException {
        QueryParser parser = new QueryParser("contents", analyzer);
        Query query = parser.parse(queryString);

        TopDocs hits = searcher.search(query, maxResults);
        List<SearchResult> results = new ArrayList<>();

        for (ScoreDoc scoreDoc : hits.scoreDocs) {
            Document doc = searcher.doc(scoreDoc.doc);
            results.add(new SearchResult(doc.get("filename"), doc.get("path"), scoreDoc.score));
        }
        return results;
    }

    public void close() throws IOException {
        if (reader != null) {
            reader.close();
        }
    }

    public static class SearchResult {
        private String filename;
        private String path;
        private float score;

        public SearchResult(String filename, String path, float score) {
            this.filename = filename;
            this.path = path;
            this.score = score;
        }

        public String getFilename() {
            return filename;
        }

        public String getPath() {
            return path;
        }

        public float getScore() {
            return score;
        }

        @Override
        public String toString() {
            return "Archivo: " + filename + ", Ruta: " + path + ", Relevancia: " + String.format("%.2f", score);
        }
    }
}
