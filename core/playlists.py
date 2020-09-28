import sqlite3
from core.decorators import singleton
from core.playlist import Playlist, Song
from typing import List
@singleton
class Playlists():
    DB_PREFIX = "dev_"
    """
    Manages a connection to SQLite to persist playlist data
    """
    def __init__(self, db_prefix = DB_PREFIX):
        """
        db_prefix is a convenience for testing, set DB_PREFIX instead
        """
        self.conn = sqlite3.connect(f'sqlite/{db_prefix}playlists.db')
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        #print("Connection to database initiated")

    def __del__(self):
        self.conn.close()

    def init_schema(self):
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY,
            guild_id blob not null,
            name text(255),
            time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.c.execute(
            """
            CREATE TABLE IF NOT EXISTS playlist_songs (
            id INTEGER PRIMARY KEY,
            playlist INTEGER not null,
            name text,
            url text,
            time_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(playlist) REFERENCES playlist(id)
            );
            """
        )
        self.conn.commit()
        return 

    def new(self,guild_id, name : str):
        entry = {
            "id" : str(guild_id),
            "name" : name
        }
        self.c.execute(
            """
            INSERT INTO playlists (guild_id, name)
            SELECT :id , :name
            WHERE NOT EXISTS(SELECT 1 from playlists WHERE guild_id =:id AND name =:name);
            """,
            entry
        )
        self.conn.commit()
        self.c.execute(
            "SELECT id FROM playlists WHERE guild_id =:id AND name =:name;",
            entry
        )
        return self.c.fetchone()[0]

    def exists(self,playlist_name):
        entry = (playlist_name,)
        self.c.execute(
            "SELECT EXISTS(SELECT 1 FROM playlists WHERE name = ?);",
            entry
        )
        return bool(self.c.fetchone()[0])
    
    def exists_in_guild(self,guild_id,playlist_name):
        entry = (str(guild_id), playlist_name)
        self.c.execute(
            "SELECT EXISTS(SELECT 1 FROM playlists WHERE guild_id = ? AND name = ?);",
            entry
        )
        return bool(self.c.fetchone()[0])
    
    def get_in_guild(self,guild_id,playlist_name):
        entry = (str(guild_id), playlist_name)
        self.c.execute(
            "SELECT id FROM playlists WHERE guild_id = ? AND name = ?;",
            entry
        )
        ans = self.c.fetchone()
        return ans[0] if ans else None
    
    def add_to(self,playlist_id, song : Song):
        entry = {
            "pid" : str(playlist_id),
            "name": str(song.name),
            "url" : str(song.url)
        }
        self.c.execute(
            """
            INSERT INTO playlist_songs (playlist, name, url)
            SELECT :pid,:name,:url
            WHERE NOT EXISTS(SELECT 1 FROM playlist_songs 
                WHERE playlist =:pid AND name=:name AND url=:url
            )
            """,
            entry
        )
        self.conn.commit()
    
    def add_to_batch(self,playlist_id, songs : List[Song]):
        entries = [{
            "pid" : str(playlist_id),
            "name": str(song.name),
            "url" : str(song.url)
        } for song in songs]
        self.c.executemany(
            """
            INSERT INTO playlist_songs (playlist, name, url)
            SELECT :pid,:name,:url
            WHERE NOT EXISTS(SELECT 1 FROM playlist_songs 
                WHERE playlist =:pid AND name=:name AND url=:url
            )
            """,
            entries
        )
        self.conn.commit()

    def load(self,guild_id,name):
        if not(self.exists_in_guild(guild_id, name)):
            return None
        playlist = Playlist(guild_id,name)
        pid = self.get_in_guild(guild_id,name)
        entry = (str(pid),)
        rows = self.c.execute(
            """
            SELECT name,url FROM playlist_songs WHERE playlist = ?
            ORDER BY time_stamp ASC
            """,
            entry
        )
        return Playlist.from_songs(
            guild_id,
            name,
            songs = rows.fetchmany()
        )
    
    def delete(self,guild_id, playlist_id):
        entry = (str(playlist_id))
        self.c.execute(
            """
            DELETE FROM playlist_songs
            WHERE playlist = ?
            """,
            entry
        )
        entry = (str(guild_id), str(playlist_id))
        self.c.execute(
            """
            DELETE FROM playlists
            WHERE guild_id = ? and id = ?
            """,
            entry
        )