from header import client, logger, youtube_key
import aiohttp
import asyncio


class queue:
    song_list = []
    page_length = 10

    async def play_queue(message):
        if voice is None:
            voice = client.join_voice_channel(message.user)
        player_loop = asyncio.get_event_loop()
        player_loop.run_until_complete(queue_loop)
        player_loop.close()

    async def queue_loop(loop):
        player = await voice.create_ytdl_player(song_list[0].url)

    @classmethod
    async def add(self, song):
        self.song_list.append(song)
        return song.title + ' queued by ' + song.dj.name

    @classmethod
    async def remove(self, position):
        self.song_list.remove(position)

    @classmethod
    async def get_playing(self, message):
        if len(self.song_list) == 0:
            message = format('nothing is playing. to queue a new song, \
                type +music add \'url\'')
            await client.send_message(message.channel, message)
        return 'Now Playing:' + self.song_list[0].title \
            + ' (' + self.song_list[0].url + ') from ' \
            + self.song_list[0].service + ' queued by ' + \
            self.song_list[0].dj.name

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
    @classmethod  # can't use __init__ because of async
    async def create(self, message):
        self.dj = message.author
        # make sure the dj is in a voice channel
        if self.dj.voice.voice_channel is None:
            msg = 'you are not not in a voice channel.'.format(message)
            await client.send_message(message.channel, msg)
            return False
        else:
            self.voice_channel = self.dj.voice.voice_channel

        # search for the song now
        base = 'https://www.googleapis.com/youtube/v3/search'
        parameters = {
            'q': message.content.split()[2:],
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
        new_song = await song.create(message)
        if not new_song:
            return False
        msg = (await song_queue.add(new_song)).format(message)
        await client.send_message(message.channel, msg)

    elif action == "list":
        await song_queue.list_songs(message, 1)

    elif action == "np":
        msg = (await song_queue.get_playing(message)).format(message)
        await client.send_message(message.channel, msg)

    if action == "play":
        msg = (await song_queue.play_queue(message)).format(message)
        await client.send_message(message.channel, msg)

    elif action == "remove":
        logger.debug(action + " is not implemented yet")
        msg = (action + ' is not implemented yet').format(message)
        await client.send_message(message.channel, msg)

    else:
        logger.debug("no such command")
