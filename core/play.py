import re
import asyncio

import discord
import youtube_dl

from discord.ext import commands


FS_BASEDIR = "music/"
# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': 'tmp/%(id)s.%(ext)s',
    #'outtmpl': 'tmp/%(id)s_%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(url, download=not stream)
            )
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class FSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_name(cls, name, ext):
        data = {
            "title": name,
            "url": f"/{name + ext}"
        }
        filename = FS_BASEDIR + name + ext
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


#https://stackoverflow.com/questions/19377262/regex-for-youtube-url#answer-37704433
YT_PATTERN = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$"
async def youtube(url, bot):
    return await YTDLSource.from_url(url, loop=bot.loop,stream=True)
FILE_PATTERN = r"^([a-zA-Z0-9_-]+)(\.[a-z0-9]*)?$"
async def ffile(name, ext, bot):
    return await FSource.from_name(name,ext)


async def parse(url, bot):
    """
    returns an AudioSource based on the url.
    url can be:
    - A youtube url
    """
    m = re.match(YT_PATTERN, url)
    if m:
        id = m.group(5)
        print(id)
        return await(youtube(url, bot))
    m = re.match(FILE_PATTERN, url)
    if m:
        name = m.group(1)
        ext = m.group(2)
        ext = ext if ext else ".mp3"
        print(name + ext)
        return await(ffile(name,ext,bot))
    raise ValueError("Argument doesn't match a valid pattern")
    




