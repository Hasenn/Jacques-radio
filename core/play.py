from collections import namedtuple
import re

ParseResult = namedtuple(
    'ParseResult',
    [
        'type',
        'data',
        'original_url'
    ]
)
#https://stackoverflow.com/questions/19377262/regex-for-youtube-url#answer-37704433
PATTERN_YT = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
PATTERN_FILENAME = r"^([a-zA-Z0-9_\-]+)(\.[a-z0-9]*)?$"

def parse(url):
    m = re.match(PATTERN_YT, url)
    if m:
        id = m.group(5)
        return ParseResult(
            type='youtube',
            data = {
                'youtube_id' : id,
            },
            original_url=url
        )
    m = re.match(PATTERN_FILENAME, url)
    if m: # file.mp3 file
        name = m.group(1)
        ext = m.group(2)
        ext = ext if ext else ".mp3"
        return ParseResult(
            type='filename',
            data = {
                'name' : name,
                'ext'  : ext,
            },
            original_url=url
        )
    return ParseResult(
        type = '',
        data = {},
        original_url=url
    )

