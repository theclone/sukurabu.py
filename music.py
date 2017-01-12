from header import client, logger, youtube_key
import aiohttp
import asyncio
import time
import threading


class queue:
    song_list = []
    page_length = 10
    is_playing = False
    song_progress = 0
    current_player = None
    start_time = None
    voice = None

    @classmethod
    async def toggle_queue(self, message):
        # join voice channel
        if self.voice is None:
            self.voice = await client.join_voice_channel(message.author.voice.voice_channel)
        # create player if it doesn't exist
        if self.current_player is None:
            self.current_player = await self.voice.create_ytdl_player(self.song_list[0].url, after=lambda: self.song_done(message))
            print("NOT PLAYING YET")
            self.current_player.start()
            print("PLAYING NOW")
            self.start_time = time.time()
            self.is_playing = True
            return "playing " + self.song_list[0].title
        else:
            # is playing
            if self.current_player.is_playing():
                self.current_player.pause()
                return "pausing " + self.song_list[0].title
            # is not playing
            if not self.current_player.is_playing():
                self.current_player.resume()
                return "playing " + self.song_list[0].title

    @classmethod
    async def song_done(self, message):
        print("I HOPE I WORK!!!!!")
        self.current_player.stop()
        self.song_list.pop[0]

        if len(self.song_list) != 0:
            self.toggle_queue(message)
        else:
            await client.send_message(message.channel, format("end of queue"))

    @classmethod
    async def add(self, song, message):
        self.song_list.append(song)
        # TODO: properly handle through configuration
        if self.voice is not None:
            self.toggle_queue(message)
        return song.title + ' queued by ' + song.dj.name

    @classmethod
    async def remove(self, message, position):
        self.song_list.remove(position)

    @classmethod
    async def get_playing(self, message):
        if len(self.song_list) == 0:
            msg = format('nothing is playing. to queue a new song, \
                type +music add \'url\'')
            await client.send_message(message.channel, msg)
        msg = 'Now Playing:' + self.song_list[0].title \
            + ' (' + self.song_list[0].url + ') from ' \
            + self.song_list[0].service + ' queued by ' + \
            self.song_list[0].dj.name
        await client.send_message(channel, msg.format(message))

    @classmethod
    async def list_songs(self, message, page):
        channel = message.channel
        if len(self.song_list) == 0:
            msg = 'you need to queue some songs first you dummy! ' +\
                  'to queue a new song, type +music add \'url\''
            await client.send_message(channel, msg.format(message))

        song_msgs = []
        for i in range(0, len(self.song_list)):
            song_msg = str(i) + '. ' \
                + self.song_list[i].title \
                + ' added by ' + self.song_list[i].dj.name
            print(song_msg)
            song_msgs.append(song_msg)
        songs_out = '\n'.join(song_msgs).format(message)
        await client.send_message(channel, songs_out)


class song:
    def __init__(self, message):
        self.message = message
    async def init(self):
        self.dj = self.message.author
        # make sure the dj is in a voice channel
        if self.dj.voice.voice_channel is None:
            msg = 'you are not not in a voice channel.'.format(self.message)
            await client.send_message(self.message.channel, msg)
        else:
            self.voice_channel = self.dj.voice.voice_channel

        # search for the song now
        base = 'https://www.googleapis.com/youtube/v3/search'
        parameters = {
            'q': self.message.content.split()[2:],
            'type': 'video',
            'key': youtube_key,
            'part': 'snippet',
            'order': 'relevance'
        }
        async with aiohttp.get(base, params=parameters) as r:
            if r.status == 200:
                json = await r.json()
                songs = json['items']
                print(songs)
                song = songs[0]  # choose first result
                self.title = song['snippet']['title']
                print(song['id'])
                self.url = 'youtu.be/' + song['id']['videoId']
                self.service = 'youtube'
                self.length = 9001
                logger.debug("added song " + self.title + ", " + self.url)
                return self
            else:
                logger.debug("error searching for song!")
                return

song_queue = queue()
async def music(message):
    action = message.content.split()[1].strip()

    if action == "add":
        new_song = song(message)
        await new_song.init()
        msg = (await song_queue.add(new_song, message)).format(message)
        await client.send_message(message.channel, msg)

    elif action == "list":
        await song_queue.list_songs(message, 1)

    elif action == "np":
        msg = (await song_queue.get_playing(message)).format(message)
        await client.send_message(message.channel, msg)

    if action in ["toggle", "pause", "play"]:
        msg = (await song_queue.toggle_queue(message)).format(message)
        await client.send_message(message.channel, msg)

    elif action == "remove":
        logger.debug(action + " is not implemented yet")
        msg = (action + ' is not implemented yet').format(message)
        await client.send_message(message.channel, msg)

    else:
        logger.debug("no such command")
