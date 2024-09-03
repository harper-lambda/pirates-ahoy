import discord
from discord.ext import commands
import asyncio
import os
from youtubesearchpython import VideosSearch
import yt_dlp
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.current_song = None
        self.voice_client = None
        self.last_search_user = None

    @commands.command()
    async def play(self, ctx, *, query=None):
        if not query:
            await ctx.send("Please provide a search query or YouTube URL. Usage: `!play <query or URL>`")
            return

        if not ctx.author.voice:
            await ctx.send("You need to be in a voice channel to use this command.")
            return

        try:
            if not self.voice_client:
                self.voice_client = await ctx.author.voice.channel.connect()
                await asyncio.sleep(1)
                source = discord.FFmpegPCMAudio('bluetooth_pairing.wav')
                self.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
        except discord.errors.ClientException:
            await ctx.send("I'm already connected to a voice channel.")
            return
        except Exception as e:
            await ctx.send(f"An error occurred while connecting to the voice channel: {str(e)}")
            return

        if query.startswith('https://www.youtube.com/watch?v='):
            # It's a YouTube URL
            await self.add_to_queue(ctx, query)
        else:
            # It's a search query
            results = await self.search_videos(query)
            if not results:
                await ctx.send("No results found for your search query.")
                return
            
            await self.send_search_results(ctx, results)

    async def send_search_results(self, ctx, results):
        self.last_search_user = ctx.author
        
        # Create an embed to display the search results
        embed = discord.Embed(title="Select a song to play:", color=discord.Color.blue())
        for i, result in enumerate(results, 1):
            truncated_title = result['title'][:70]
            if len(result['title']) > 70:
                truncated_title += '...'
            # Include the title (bolded) and channel name
            embed.add_field(
                name=f"**{i}. {truncated_title}**",
                value=f"{result['channel']}",
                inline=False
            )

        # Create a custom view with buttons in a column
        view = discord.ui.View(timeout=30)
        for i, result in enumerate(results):
            button = discord.ui.Button(label=f"{i+1}", style=discord.ButtonStyle.primary, custom_id=str(i))
            button.callback = lambda interaction, i=i: self.button_callback(interaction, results[i]['url'], results[i]['title'])
            view.add_item(button)

        # Send the embed with the view
        message = await ctx.send(embed=embed, view=view)

        async def on_timeout():
            try:
                await message.delete()
            except discord.errors.NotFound:
                # Message has already been deleted, ignore the error
                pass
            except Exception as e:
                # Log any other unexpected errors
                print(f"An error occurred while deleting the message: {str(e)}")

        view.on_timeout = on_timeout

    async def button_callback(self, interaction, url, title):
        if interaction.user != self.last_search_user:
            await interaction.response.send_message("You can't use this button.", ephemeral=True)
            return

        await interaction.response.defer()
        await interaction.message.delete()  # Delete the message with buttons
        await self.add_to_queue(interaction.channel, url, title)

    async def add_to_queue(self, ctx, url, title=None):
        if title:
            await ctx.send(f"Adding **{title}** to queue. Please wait while I download the audio...")
        else:
            await ctx.send(f"Adding song to queue. Please wait while I download the audio...")
        try:
            song_info = await self.download_audio(url)
            if song_info:
                self.queue.append(song_info)
                await ctx.send(f"Successfully added to queue: **{song_info['title']}**")
                if not self.current_song:
                    await self.play_next(ctx)
            else:
                await ctx.send("Failed to download the audio. Please try again with a different link or search query.")
        except Exception as e:
            await ctx.send(f"An error occurred while adding the song to the queue: {str(e)}")

    async def play_next(self, ctx):
        if self.queue:
            self.current_song = self.queue.pop(0)
            try:
                source = discord.FFmpegPCMAudio(self.current_song['filename'])
                self.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop))
                await ctx.send(f"Now playing: **{self.current_song['title']}**")
            except Exception as e:
                await ctx.send(f"An error occurred while playing the song: {str(e)}")
                await self.play_next(ctx)
        else:
            self.current_song = None
            await ctx.send("Queue is empty. Use `!play` to add more songs!")

    @commands.command()
    async def stop(self, ctx):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            await ctx.send("Playback stopped.")
        else:
            await ctx.send("Nothing is currently playing.")

    @commands.command()
    async def skip(self, ctx):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.stop()
            await ctx.send("Skipped the current song.")
            await self.play_next(ctx)
        else:
            await ctx.send("Nothing is currently playing.")

    @commands.command()
    async def queue(self, ctx):
        if not self.queue:
            await ctx.send("The queue is empty. Use `!play` to add songs!")
        else:
            queue_list = "Current queue:\n"
            for i, song in enumerate(self.queue, 1):
                queue_list += f"{i}. {song['title']}\n"
            await ctx.send(queue_list)

    async def search_videos(self, query, max_results=5):
        try:
            videos_search = VideosSearch(query, limit=max_results)
            results = []
            for video in videos_search.result()['result']:
                results.append({
                    'title': video['title'],
                    'url': video['link'],
                    'duration': video['duration'],
                    'channel': video['channel']['name']
                })
            return results
        except Exception as e:
            print(f"An error occurred during video search: {str(e)}")
            return []

    async def download_audio(self, url, output_path='./downloads'):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).rsplit('.', 1)[0] + '.mp3'
                return {
                    'title': info['title'],
                    'filename': filename
                }
        except Exception as e:
            print(f"An error occurred during audio download: {str(e)}")
            return None

async def setup(bot):
    await bot.add_cog(Music(bot))

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await setup(bot)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Unknown command. Use `!help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param.name}")
    else:
        await ctx.send(f"An error occurred: {str(error)}")

def load_credentials():
    with open('creds.json') as f:
        return json.load(f)

credentials = load_credentials()
bot.run(credentials['token'])