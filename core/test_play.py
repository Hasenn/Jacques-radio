import unittest
import core.play as parser

class TestParseUrl(unittest.TestCase):
    def test_parse_youtube(self):
        youtube_urls = [
            "m.youtube.com/watch?v=DFYRQ_zQ-gk",
            "http://www.youtube.com/watch?v=DFYRQ_zQ-gk",
            "https://youtube.com/embed/DFYRQ_zQ-gk",
            "youtu.be/DFYRQ_zQ-gk",
            "https://www.youtube.com/HamdiKickProduction?v=DFYRQ_zQ-gk",
        ]
        for url in youtube_urls:
            parse_result = parser.parse(url)
            self.assertEqual(
                parse_result.type,
                'youtube',
                f"{url} should match a Youtube url"
            )
            self.assertEqual(
                parse_result.data['youtube_id'],
                'DFYRQ_zQ-gk',
                f"{url} should have id `DFYRQ_zQ-gk`"
            )
    def test_parse_filename(self):
        filenames = [
            "mymuSic00.mp3",
            "something",
        ]
        for url in filenames:
            parse_result = parser.parse(url)
            self.assertEqual(
                parse_result.type,
                'filename',
                f"{url} should match a filename"
            )
if __name__ == '__main__':
    unittest.main()