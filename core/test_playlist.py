import unittest
from core.playlist import Playlist

class TestPlaylist(unittest.TestCase):
    
    def test_lifecycle(self):
        guild_id = 684639977925247025
        name = 'My Brand new Playlist'
        playlist = Playlist(guild_id,name)
    
    @unittest.expectedFailure
    def test_arguments(self):
        Playlist(guild_id)

    def test_songs(self):
        guild_id = 684639977925247025
        name = 'My Brand new Playlist'

        songs = [
        ('Hiroshi Suzuki-Romance', "https://www.youtube.com/watch?v=BFmH7moCL2c&list=PLVBI1q1hkB7IccMqok4hkM-5vA0RgD1Um&index=1"),
        ("Men I Trust - Seven (garage session)","https://www.youtube.com/watch?v=eGwKvxGpLqs&list=PLVBI1q1hkB7IccMqok4hkM-5vA0RgD1Um&index=2")
        ]
        playlist = Playlist.from_songs(
            guild_id,
            name,
            songs
        )
        self.assertEqual(
            len(playlist.songs),
            2
        )
        r = playlist.play()
        self.assertTrue(r)
        playlist.pop()

    

if __name__ == '__main__':
    unittest.main()
