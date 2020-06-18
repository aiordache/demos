import os
import flask
import json
import mysql.connector

# for debugging from Visual Studio Code -- turn off flask debugger first
# import ptvsd
# ptvsd.enable_attach(address=('0.0.0.0', 3000))

class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host,
            database=database,
            auth_plugin='mysql_native_password'
        )
        pf.close()
        self.cursor = self.connection.cursor()
    
    def populate_db(self):
        self.cursor.execute('DROP TABLE IF EXISTS blog')
        self.cursor.execute('CREATE TABLE blog (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255))')
        self.cursor.executemany('INSERT INTO blog (id, title) VALUES (%s, %s);', [(i, 'Blog post #%d'% i) for i in range (1,5)])
        self.connection.commit()
    
    def query_titles(self):
        self.cursor.execute('SELECT title FROM blog')
        rec = []
        for c in self.cursor:
            rec.append(c[0])
        return rec


server = flask.Flask(__name__)
conn = None

@server.route('/blogs')
def listBlog():
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    rec = conn.query_titles()

    result = []
    for c in rec:
        result.append(c)

    return flask.jsonify({"response": result})

@server.route('/')
def hello():
    return flask.jsonify({"response": "Hello from Docker!"})


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=5000)
