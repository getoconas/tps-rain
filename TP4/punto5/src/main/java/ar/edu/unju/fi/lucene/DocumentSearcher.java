package ar.edu.unju.fi.lucene;

import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.*;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.search.similarities.BM25Similarity;

import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class DocumentSearcher {
    private IndexReader reader;
    private IndexSearcher searcher;
    private StandardAnalyzer analyzer;

    public DocumentSearcher(String indexPath) throws IOException {
        this.analyzer = new StandardAnalyzer();
        Directory indexDirectory = FSDirectory.open(Paths.get(indexPath));
        this.reader = DirectoryReader.open(indexDirectory);
        this.searcher = new IndexSearcher(reader);
        searcher.setSimilarity(new BM25Similarity(2.0f, 0.1f)); // Ajustado para dar más peso a términos exactos
    }

    public List<SearchResult> search(String queryString, int maxResults) throws IOException {
        Query query = buildCombinedQuery(queryString);
        TopDocs hits = searcher.search(query, maxResults);
        List<SearchResult> results = new ArrayList<>();
        // Itera sobre los resultados y recupera la información de cada documento.
        for (ScoreDoc scoreDoc : hits.scoreDocs) {
            Document doc = searcher.doc(scoreDoc.doc); // Obtiene el documento Lucene por su ID interno
            results.add(new SearchResult(doc.get("filename"), doc.get("path"), scoreDoc.score));
        }
        return results;
    }

    private Query buildCombinedQuery(String queryString) {
        String[] terms = queryString.toLowerCase().split("\\s+");

        // Frase exacta
        PhraseQuery.Builder phraseBuilder = new PhraseQuery.Builder();
        for (int i = 0; i < terms.length; i++) {
            phraseBuilder.add(new Term("contents", terms[i]), i);
        }
        PhraseQuery phraseQuery = phraseBuilder.build();
        BoostQuery boostedPhrase = new BoostQuery(phraseQuery, 5.0f); // Le damos alto peso

        // Palabras individuales
        BooleanQuery.Builder individualTermsBuilder = new BooleanQuery.Builder();
        for (String term : terms) {
            TermQuery termQuery = new TermQuery(new Term("contents", term));
            individualTermsBuilder.add(new BooleanClause(termQuery, BooleanClause.Occur.SHOULD));
        }
        BooleanQuery individualTermsQuery = individualTermsBuilder.build();

        // Combinación final
        BooleanQuery.Builder finalQuery = new BooleanQuery.Builder();
        finalQuery.add(boostedPhrase, BooleanClause.Occur.SHOULD);
        finalQuery.add(individualTermsQuery, BooleanClause.Occur.SHOULD);

        return finalQuery.build();
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
