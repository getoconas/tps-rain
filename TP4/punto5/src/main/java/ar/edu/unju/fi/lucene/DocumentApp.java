package ar.edu.unju.fi.lucene;
import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;

public class DocumentApp extends JFrame {
    private JTextField directoryPathField;
    private JTextField queryField;
    private JTable resultsTable;
    private DefaultTableModel tableModel;
    private JTextArea consoleOutput;

    private String indexPath = "./lucene_index";

    public DocumentApp() {
        super("Indexador y Buscador de Documentos Lucene");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(900, 700);
        setLocationRelativeTo(null);

        JPanel controlPanel = new JPanel(new GridLayout(4, 1, 5, 5)); // 4 filas para más espacio
        controlPanel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        JPanel indexDirPanel = new JPanel(new BorderLayout(5, 5));
        indexDirPanel.add(new JLabel("Directorio a Indexar:"), BorderLayout.WEST);
        directoryPathField = new JTextField(System.getProperty("user.dir") + File.separator + "documentos");
        indexDirPanel.add(directoryPathField, BorderLayout.CENTER);
        JButton browseButton = new JButton("Examinar");
        browseButton.addActionListener(e -> chooseDirectory());
        indexDirPanel.add(browseButton, BorderLayout.EAST);
        controlPanel.add(indexDirPanel);

        JPanel actionButtonsPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 0));
        JButton indexButton = new JButton("1. Indexar Documentos");
        indexButton.setFont(new Font("Arial", Font.BOLD, 14));
        indexButton.addActionListener(e -> startIndexing());
        actionButtonsPanel.add(indexButton);

        JButton clearIndexButton = new JButton("Limpiar Índice");
        clearIndexButton.addActionListener(e -> clearIndex());
        actionButtonsPanel.add(clearIndexButton);

        controlPanel.add(actionButtonsPanel);

        JPanel queryPanel = new JPanel(new BorderLayout(5, 5));
        queryPanel.add(new JLabel("Consulta de Búsqueda:"), BorderLayout.WEST);
        queryField = new JTextField();
        queryField.setToolTipText("Introduce aquí tu consulta de búsqueda (ej. 'lucene', 'informe AND 2023')");
        queryField.addActionListener(e -> startSearching());
        queryPanel.add(queryField, BorderLayout.CENTER);
        JButton searchButton = new JButton("2. Buscar");
        searchButton.setFont(new Font("Arial", Font.BOLD, 14));
        searchButton.addActionListener(e -> startSearching());
        queryPanel.add(searchButton, BorderLayout.EAST);
        controlPanel.add(queryPanel);

        add(controlPanel, BorderLayout.NORTH);

        tableModel = new DefaultTableModel(new Object[]{"Nombre de Archivo", "Ruta Absoluta", "Relevancia"}, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        resultsTable = new JTable(tableModel);
        resultsTable.setAutoCreateRowSorter(true);
        resultsTable.setFillsViewportHeight(true);
        JScrollPane scrollPane = new JScrollPane(resultsTable);
        add(scrollPane, BorderLayout.CENTER);

        consoleOutput = new JTextArea(8, 20);
        consoleOutput.setEditable(false);
        consoleOutput.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 12));
        consoleOutput.setBorder(BorderFactory.createTitledBorder("Consola de Actividad"));
        JScrollPane consoleScrollPane = new JScrollPane(consoleOutput);
        add(consoleScrollPane, BorderLayout.SOUTH);

        setVisible(true);
    }

    private void chooseDirectory() {
        JFileChooser fileChooser = new JFileChooser();
        fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        int option = fileChooser.showOpenDialog(this);
        if (option == JFileChooser.APPROVE_OPTION) {
            File selectedDirectory = fileChooser.getSelectedFile();
            directoryPathField.setText(selectedDirectory.getAbsolutePath());
        }
    }

    private void startIndexing() {
        String dirToIndex = directoryPathField.getText();
        if (dirToIndex.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Por favor, selecciona un directorio a indexar.", "Error de Directorio", JOptionPane.ERROR_MESSAGE);
            return;
        }

        File checkDir = new File(dirToIndex);
        if (!checkDir.exists() || !checkDir.isDirectory()) {
            JOptionPane.showMessageDialog(this, "El directorio especificado no existe o no es válido: " + dirToIndex, "Error de Directorio", JOptionPane.ERROR_MESSAGE);
            return;
        }

        boolean useRAM = false;

        consoleOutput.setText("");
        appendToConsole("Iniciando indexación de: " + dirToIndex);
        appendToConsole("Usando disco para el índice.");

        new Thread(() -> {
            DocumentIndexer indexer = null;
            try {
                indexer = new DocumentIndexer(indexPath, useRAM);
                indexer.createIndex(dirToIndex);
                appendToConsole("Indexación completada exitosamente.");
            } catch (IOException e) {
                appendToConsole("Error durante la indexación: " + e.getMessage());
                e.printStackTrace();
            } finally {
                if (indexer != null) {
                    try {
                        indexer.close();
                    } catch (IOException e) {
                        appendToConsole("Error al cerrar el indexador: " + e.getMessage());
                    }
                }
            }
        }).start();
    }

    private void clearIndex() {
        int confirm = JOptionPane.showConfirmDialog(this,
                "¿Estás seguro de que quieres eliminar el índice actual en disco (" + indexPath + ")?",
                "Confirmar Limpieza de Índice", JOptionPane.YES_NO_OPTION);

        if (confirm == JOptionPane.YES_OPTION) {
            try {
                File indexDir = new File(indexPath);
                if (indexDir.exists() && indexDir.isDirectory()) {
                    Files.walk(Paths.get(indexPath))
                            .sorted(java.util.Comparator.reverseOrder())
                            .map(java.nio.file.Path::toFile)
                            .forEach(File::delete);
                    appendToConsole("Índice en disco limpiado: " + indexPath);
                } else {
                    appendToConsole("El directorio del índice no existe o no es un directorio: " + indexPath);
                }
            } catch (IOException e) {
                appendToConsole("Error al limpiar el índice: " + e.getMessage());
                e.printStackTrace();
            }
        }
    }

    private void startSearching() {
        String query = queryField.getText();
        if (query.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Por favor, introduce una consulta de búsqueda.", "Advertencia", JOptionPane.WARNING_MESSAGE);
            return;
        }

        tableModel.setRowCount(0);
        consoleOutput.setText("");
        appendToConsole("Buscando: \"" + query + "\"...\n");

        new Thread(() -> {
            DocumentSearcher searcher = null;
            try {
                searcher = new DocumentSearcher(indexPath, false);
                java.util.List<DocumentSearcher.SearchResult> results = searcher.search(query, 100);

                if (results.isEmpty()) {
                    appendToConsole("No se encontraron resultados para: \"" + query + "\"\n");
                } else {
                    SwingUtilities.invokeLater(() -> {
                        for (DocumentSearcher.SearchResult result : results) {
                            tableModel.addRow(new Object[]{result.getFilename(), result.getPath(), String.format("%.2f", result.getScore())});
                        }
                    });
                    appendToConsole("Búsqueda completada. Se encontraron " + results.size() + " resultados.\n");
                }

            } catch (IOException e) {
                appendToConsole("Error durante la búsqueda: " + e.getMessage());
                e.printStackTrace();
            } finally {
                if (searcher != null) {
                    try {
                        searcher.close();
                    } catch (IOException e) {
                        appendToConsole("Error al cerrar el buscador: " + e.getMessage());
                    }
                }
            }
        }).start();
    }

    private void appendToConsole(String text) {
        SwingUtilities.invokeLater(() -> consoleOutput.append(text + "\n"));
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new DocumentApp());
    }
}
