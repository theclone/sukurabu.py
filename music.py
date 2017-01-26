from header import client, logger, youtube_key
import aiohttp
import asyncio
import time


class queue:
    song_list = []
    page_length = 10
    is_playing = False
    song_progress = 0
    current_player = None
    start_time = None
    voice = None

    @classmethod
    async def async_song_done(self):
        title = self.song_list.pop(0).title
        self.current_player = None
        await client.send_message(self.message.channel, title + " is done!")

        if len(self.song_list) != 0:
            await self.toggle_queue(self.message)
        else:
            await client.send_message(self.message.channel,
                                      "the end of the road")

    @classmethod
    def song_done(self):
        coro = self.async_song_done()
        fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
        try:
            fut.result(1)
        except:
            pass

    @classmethod
    async def toggle_queue(self, message):
        # join voice channel
        if self.voice is None:
            self.vchannel = message.author.voice.voice_channel
            self.voice = await client.join_voice_channel(self.vchannel)
        # create player if it doesn't exist
        if self.current_player is None:
            self.message = message
            self.current_player = await self.voice.create_ytdl_player(
                    self.song_list[0].url, after=self.song_done)
            self.current_player.start()
            self.start_time = time.time()
            self.is_playing = True
            await client.send_message(self.message.channel, "playing " +
                                      self.song_list[0].title)
        else:
            # is playing
            if self.current_player.is_playing():
                self.current_player.pause()
                await client.send_message(self.message.channel, "pausing "
                                          + self.song_list[0].title)
            # is not playing
            if not self.current_player.is_playing():
                self.current_player.resume()
                await client.send_message(self.message.channel, "resuming "
                                          + self.song_list[0].title)

    @classmethod
    async def next(self, message):
        if self.current_player is not None:
            self.current_player.stop()
        else:
            await client.send_message(message.channel,
                                      "there's nothing to skip")

    @classmethod
    async def add(self, song, message):
        self.song_list.append(song)
        if len(self.song_list) == 1:
            await self.toggle_queue(message)
        return song.title + ' queued by ' + song.dj.name

    @classmethod
    async def remove(self, message, position):
        self.song_list.pop(position)

    @classmethod
    async def get_playing(self, message):
        if len(self.song_list) == 0:
            msg = 'nothing is playing. to queue a new song, \
                    type +music add \'url\''
            await client.send_message(message.channel, msg)
        msg = 'Now Playing:' + self.song_list[0].title + ' (' + \
              self.song_list[0].url + ') from ' +               \
              self.song_list[0].service + ' queued by ' +       \
              self.song_list[0].dj.name
        await client.send_message(message.channel, msg)

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
        await client.send_message(message.channel, msg)

    elif action == "next":
        await song_queue.next(message)

    elif action == "np":
        await song_queue.get_playing(message)

    if action in ["toggle", "pause", "play"]:
        await song_queue.toggle_queue(message)

    elif action == "remove":
        logger.debug(action + " is not implemented yet")
        msg = (action + ' is not implemented yet').format(message)
        await client.send_message(message.channel, msg)

    else:
        logger.debug("no such command")
