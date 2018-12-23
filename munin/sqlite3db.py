import sqlite3
import time


class SQLite3Database:
    def init_database(self):
        c = self._connection.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS responses ( \n"
                  "id INTEGER PRIMARY KEY,\n"
                  "timestamp REAL,\n"
                  "url TEXT,\n"
                  "response BLOB\n"
                  ")\n")
        self._connection.commit()
        if self._index:
            c.execute("CREATE INDEX IF NOT EXISTS url_index "
                      "ON responses (url);")
            self._connection.commit()
        if not self._synchronous:
            c.execute("PRAGMA synchronous = OFF;")
            self._connection.commit()

    def __init__(self, database, index=True, synchronous=True):
        self._index = index
        self._synchronous = synchronous
        self._connection = sqlite3.connect(database)

    def put_response(self, url, response):
        c = self._connection.cursor()
        c.execute("INSERT INTO responses (timestamp, url, response) "
                  "VALUES (?, ?, ?)", (time.time(), url, response))
        self._connection.commit()

    def get_response(self, url):
        c = self._connection.cursor()
        c.execute("SELECT response FROM responses WHERE url = ? "
                  "ORDER BY timestamp DESC LIMIT 1", (url,))
        row = c.fetchone()
        if row is None:
            return row
        else:
            return row[0]

    def get_many_responses(self, url):
        c = self._connection.cursor()
        c.execute("SELECT response FROM responses WHERE url = ?", (url,))
        rows = c.fetchall()
        return [r[0] for r in rows]
