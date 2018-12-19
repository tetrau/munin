import sqlite3


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
