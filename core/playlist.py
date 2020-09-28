from dataclasses import dataclass, field
from collections import deque, namedtuple
import random
from typing import List, Deque
"""

S0   S1   S2   S3   S4
^ Playing            ^ Last pushed
"""
Song = namedtuple('Song', ['name', 'url'])

@dataclass
class Playlist:
    guild_id : int
    name     : str
    loop     : bool = False
    shuffle  : bool = False
    # use a default factory to avoid instances
    # sharing the same mutables
    songs   : List[Song]  = field(
        default_factory = lambda: []
    )
    to_play : Deque[Song] = field(
        default_factory = lambda: deque([])
    )
    playing = None

    @classmethod
    def from_songs(cls,guild_id,name,songs):
        instance = cls(guild_id,name)
        for song in songs:
            instance.songs.append(Song(song[0],song[1]))
        return instance

    def play(self,loop = False, shuffle = False):
        if len(self.songs) == 0:
            return None
        self.loop = loop
        self.shuffle = shuffle
        self.to_play = deque(self.songs)
        if shuffle:
            _shuffle()
        return self.to_play[0]
        
    def clear(self):
        self.songs = []
        self.to_play = deque([])

    def push(song : Song):
        self.songs.append(song)
        self.to_play.append(song)
    
    def pop(self):
        song_to_pop = self.to_play.pop()
        for song, i in self.songs:
            if song == song_to_pop:
                self.songs.pop(i)
        return song_to_pop
    
    def next(self):
        if len(self.to_play) == 0:
            return None
        if loop:
            current = self.to_play.popleft()
            self.to_play.append(current)
            return self.to_play([0])
        return self.to_play.popleft()

    def _shuffle():
        random.shuffle(self.to_play)


        
        
    
