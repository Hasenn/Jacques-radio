import unittest
import core.playlists
from core.playlist import Playlist, Song
class TestPlaylists(unittest.TestCase):
    def test_lifecycle(self):
        playlists = core.playlists.Playlists(db_prefix = "test_")
        playlists.init_schema()
        # the destructor is called at the very end of the program
        # because Playlists is a singleton
        
    def test_playlist(self):
        guild_id = 684639977925247025
        name = 'My Brand new Playlist'
        song = Song("japanese math rock when you strategically move the pawn",
        "youtu.be/Irxr58Q9FUw")
        playlists = core.playlists.Playlists(db_prefix = "test_")
        p = playlists.new(guild_id, name)

        playlists.init_schema()
        self.assertTrue(p, 'new should return an id')

        pp = playlists.get_in_guild(guild_id, name)
        self.assertTrue(p == pp, "get_in_guild and new ids should match")

        playlists.add_to(p, song)
        playlists.add_to_batch(p,[song,song,song,song])
        b = playlists.exists('My Brand new Playlist')
        self.assertTrue(b)
        b = playlists.exists_in_guild(guild_id,'My Brand new Playlist')
        self.assertTrue(b)
        b = playlists.exists('My Brt')
        self.assertFalse(b)

        print(playlists.load(guild_id, name))

        playlists.delete(guild_id, p)

        self.assertEqual(
            playlists.load(guild_id, name),
            None,
            "playlists.Load should return None if the playlist doesn't exist"
        )
    


if __name__ == '__main__':
    unittest.main()