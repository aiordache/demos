import com.google.common.base.Charsets;
import com.google.common.base.Supplier;
import com.google.common.base.Suppliers;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.lang.String;
import java.nio.file.*; 
import java.io.*; 
import java.nio.charset.StandardCharsets; 
import java.net.InetSocketAddress;
import java.sql.*;
import java.util.NoSuchElementException;

public class Main {
    public static int dbPopulateRetry;
    public static HttpServer server;
    public static void main(String[] args) throws Exception {
        dbPopulateRetry = 7;
        Class.forName("org.postgresql.Driver");

        server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/noun", handler(Suppliers.memoize(() -> randomWord("nouns"))));
        server.createContext("/verb", handler(Suppliers.memoize(() -> randomWord("verbs"))));
        server.createContext("/adjective", handler(Suppliers.memoize(() -> randomWord("adjectives"))));
        server.start();
    }
    private static void refreshContext() throws IOException {
        server.removeContext("/noun");
        server.removeContext("/verb");
        server.removeContext("/adjective");
        server.createContext("/noun", handler(Suppliers.memoize(() -> randomWord("nouns"))));
        server.createContext("/verb", handler(Suppliers.memoize(() -> randomWord("verbs"))));
        server.createContext("/adjective", handler(Suppliers.memoize(() -> randomWord("adjectives"))));
    }
    private static String populateDB() throws IOException {
        
        try (Connection connection = DriverManager.getConnection("jdbc:postgresql://db:5432/postgres", "postgres", "")) {
            
            DatabaseMetaData dbm = connection.getMetaData();
            ResultSet table = dbm.getTables(null, null, "nouns", null);
            if (table.next()) {
                return null;
            }
            try (Statement statement = connection.createStatement()) {
                String tables = new String(Files.readAllBytes(Paths.get("/app/resources/table.sql")));
                statement.executeUpdate(tables);
                    
                String words = new String(Files.readAllBytes(Paths.get("/app/resources/words.sql")));
                statement.executeUpdate(words);
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        throw new NoSuchElementException("nouns");
    }


    private static String randomWord(String table) {
        try (Connection connection = DriverManager.getConnection("jdbc:postgresql://db:5432/postgres", "postgres", "")) {
            try (Statement statement = connection.createStatement()) {
                try (ResultSet set = statement.executeQuery("SELECT word FROM " + table + " ORDER BY random() LIMIT 1")) {
                    while (set.next()) {
                        return set.getString(1);
                    }
                }
            }
        } catch (SQLException e) {
            try {
                dbPopulateRetry = dbPopulateRetry - 1;
                if (dbPopulateRetry < 0) {
                    throw new IOException("unable to populate DB");
                }
                populateDB();
                randomWord(table);
            }
            catch(IOException ie) {
                e.printStackTrace();
                ie.printStackTrace();
                }
        }
        throw new NoSuchElementException(table);
    }

    

    private static HttpHandler handler(Supplier<String> word) {
        return t -> {
            String response = "{\"word\":\"" + word.get() + "\"}";
            byte[] bytes = response.getBytes(Charsets.UTF_8);

            System.out.println(response);
            t.getResponseHeaders().add("content-type", "application/json; charset=utf-8");
            t.sendResponseHeaders(200, bytes.length);

            try (OutputStream os = t.getResponseBody()) {
                os.write(bytes);
            }
            refreshContext();
        };
    }
}
