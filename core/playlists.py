import sqlite3
DB_PREFIX = "dev_"
class Playlists():
    """
    Manages a connection to SQLite to persist playlist data
    """
    def __init__(self, db_prefix = DB_PREFIX):
        self.conn = sqlite3.connect(f'sqlite/{db_prefix}playlists.db')
        self.c = self.conn.cursor()
        #print("Connection to database initiated")

    def __del__(self):
        self.conn.close()
        #print("Connection to database terminated")

    def init_schema(self):
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY,
            guild_id blob not null,
            name text(255)
            );
            """
        )
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS playlist_songs (
            id INTEGER PRIMARY KEY,
            playlist INTEGER not null,
            url text,
            FOREIGN KEY(playlist) REFERENCES playlist(id)
            );
            """
        )
        self.conn.commit()
        return 

    def new(self,guild_id, name : str):
        entry = (str(guild_id),name)
        self.c.execute(
            "INSERT INTO playlists (guild_id, name) VALUES (?,?)",
            entry
        )
        self.conn.commit()
        entry = (self.c.lastrowid,)
        self.c.execute(
            "SELECT id FROM playlists where rowid=?",
            entry
        )
        return self.c.fetchone()

    def add_to_by_id(self,playlist_id, url):
        entry = (str(playlist_id),str(url))
        self.c.execute(
            "INSERT INTO playlist_songs (playlist, url) VALUES (?,?)",
            entry
        )
        self.conn.commit()

    def print(self,playlist_id):
        entry = (str(playlist_id),)
        rows = self.c.execute(
            "SELECT url FROM playlist_songs WHERE playlist = ?",
            entry
        )
        for row in rows:
            print(row)

