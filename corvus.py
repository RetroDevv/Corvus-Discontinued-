import discord
from discord.ext import commands
from discord.utils import get
import chalk
import discord
import youtube_dl
import random
import os
import shutil

bot = commands.Bot(command_prefix='!', status=discord.Status.idle, activity=discord.Game(name="Booting.."))

bot.remove_command("help")

@bot.event
async def on_ready():
    print("Ayame is ready for action!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Active!"))

    
@bot.command()
async def user(ctx, member:discord.User = None):
    if member == None:
        member = ctx.message.author
    name = f"{member.name}#{member.discriminator}"
    await ctx.channel.send (f"What? You want me to say your's or someone's name? Okay! {name}")   

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send (f'I kicked {member.mention} from SOX!')

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send (f'I banned {member.mention} from SOX!')

@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user 


        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send (f'I unbanned {user.mention}')
            return


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')


@bot.command()
async def flipcoin(ctx):
    choices = ["Heads", "Tails"]
    rancoin = random.choice(choices)
    await ctx.send(rancoin) 
    
@bot.command() 
async def rannumber(ctx):
    choices = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    rancoin = random.choice(choices)
    await ctx.send(rancoin)

@bot.command()
async def creeper(ctx):
    await ctx.send(f"Aww man")

@bot.command(pass_context=True, aliases=["j", "joi"])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        
    await voice.disconnect()
    
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"Joined {channel}\n")
        
    await ctx.send(f"I have joined {channel}!")



@bot.command(pass_context=True, aliases=["l", "lea"])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
         await voice.disconnect()
         print(f"Left {channel}")
         await ctx.send(f"I have left {channel}!")
    else:
        print("I was told to leave the voice channel, but I was not inside one!")
        await ctx.send("I am not in a voice channel!")

        
@bot.command(pass_context=True, aliases=["p", "pla"])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print ("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but is being played")
        await ctx.send("ERROR: Music playing.")
        return 

    await ctx.send("Getting everything ready now! Please keep in mind this will take some time depending on the length of your song!")

    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        "format": 'bestaudio/best',
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }       
    
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File!: {file}\n") 
            os.rename(file, "song.mp3") 

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing!")) 
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.value = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing {nname}")
    print("Playing!\n")
 

@bot.command(pass_context=True, aliases=["pa", "pau"])
async def pause(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused!")
        voice.pause()
        await ctx.send("Music paused!")
    else:
        print("Music not paused failed pause")
        await ctx.send("I cannot pause non-existant music!")


@bot.command(pass_context=True, aliases=["r", "res"])
async def resume(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed your music!")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused!") 

@bot.command(pass_context=True, aliases=["s", "sto"]) 
async def stop(ctx):

    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("I have stopped your music!")

    else:
        print("No music playing failed to stop")
        await ctx.send("I can't stop non-existant music!")
                             

bot.run("")