import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from discord.utils import get
from discord import FFmpegPCMAudio
import asyncio
import time

intent = discord.Intents.default()
intent.message_content = True

bot = commands.Bot(command_prefix='!', intents= intent)

@bot.event
async def on_ready():
    print('로그인합니다')
    print('봇 이름 : ', bot.user.name)
    print('연결 성공')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("음악 재생"))


@bot.command()
async def 자기소개(ctx):
    await ctx.send(embed = discord.Embed(title = '자기소개', description = '저는 디스코드 노래봇입니다.',color = 0x0000ff))

@bot.command()
async def join(ctx):
    try:
        global vc
        vc = await ctx.message.author.voice.channel.connect()
        await ctx.send(embed = discord.Embed(title = 'O', description = '통화방 접속 성공!', color = 0x00ff00))
    except:
        try:
            await vc.move_to(ctx.message.author.voice.channel)
        except:
            await ctx.send(embed = discord.Embed(title = 'X', description = '아무도 통화방에 없네요..', color = 0xff0000))

@bot.command()
async def leave(ctx):
    try:
        await vc.disconnect()
    except:
        await ctx.send(embed = discord.Embed(title = 'X', description = '이미 그 통방에 속해있지 않아요..', color = 0xff0000))

@bot.command()
async def purl(ctx, *, url):
    YDL_OPTIONS = {'format': 'bestaudio','noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not vc.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        await ctx.send(embed = discord.Embed(title= "Play Music", description = "현재 " + url + "을(를) 재생하고 있습니다.", color = 0x00ff00))
    else:
        await ctx.send("노래가 이미 재생되고 있습니다!")

@bot.command()
async def p(ctx, *, msg):
    if not vc.is_playing():

        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        global entireText
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
            
        chromedriver_dir = r"C:\Users\joypd\OneDrive\바탕 화면\discordBot\discordMusicBot\chromedriver.exe"
        driver = webdriver.Chrome(chromedriver_dir, options = options)
        driver.get("https://www.youtube.com/results?search_query="+msg+"+lyrics")
        source = driver.page_source
        bs = BeautifulSoup(source, 'lxml')
        entire = bs.find_all('a', {'id': 'video-title'})
        entireNum = entire[1]
        entireText = entireNum.text.strip()
        musicurl = entireNum.get('href')
        url = 'https://www.youtube.com'+musicurl

        driver.quit()

        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        await ctx.send(embed = discord.Embed(title= "Play Music", description = "현재 " + entireText + "을(를) 재생하고 있습니다.", color = 0x00ff00))
        vc.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
    else:
        await ctx.send("이미 노래가 재생 중이라 노래를 재생할 수 없어요!")

@bot.command()
async def stop(ctx):
    if vc.is_playing():
        vc.stop()
        await ctx.send(embed = discord.Embed(title= "Stop Music", description = entireText + "을(를) 종료했습니다.", color = 0x00ff00))
    else:
        await ctx.send("지금은 노래가 재생되지 않네요")

bot.run('bot tkn')
