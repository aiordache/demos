import os
import flask

from flask_cors import CORS, cross_origin
import json
import mysql.connector
#import ptvsd
#ptvsd.enable_attach(address=('0.0.0.0', 3000))

class DBManager:
    def __init__(self, database='example', host="db", user="root", password_file=None):
        pf = open(password_file, 'r')
        self.connection = mysql.connector.connect(
            user=user, 
            password=pf.read(),
            host=host, # name of the mysql service as set in the docker-compose file
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
cors = CORS(server, resorces={r'*': {"origins": '*'}})
server.config['CORS_HEADERS'] = 'Content-Type'
conn = None

@server.route('/')
@cross_origin()
def listBlog():
    global conn
    if not conn:
        conn = DBManager(password_file='/run/secrets/db-password')
        conn.populate_db()
    rec = conn.query_titles()

    result = ''
    for c in rec:
        result = result  + '<div>   Hello  ' + c + '</div>'
    return result
   
    response = flask.jsonify({"response": result})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=5000)
