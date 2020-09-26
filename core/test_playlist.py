import unittest
import core.playlists

class TestPlaylists(unittest.TestCase):
    def test_lifecycle(self):
        playlists = core.playlists.Playlists(db_prefix = "test_")
        playlists.init_schema()
    def test_new_playlist(self):
        guild_id = 684639977925247025
        name = 'My Brand new Playlist'
        playlists = core.playlists.Playlists(db_prefix = "test_")
        p = playlists.new(guild_id, name)
        playlists.init_schema()
        self.assertTrue(p, 'new should return an id')
        playlists.add_to_by_id(p, "youtu.be/Irxr58Q9FUw")
        playlists.print(p)

if __name__ == '__main__':
    unittest.main()