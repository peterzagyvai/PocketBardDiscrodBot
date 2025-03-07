import discord
from discord.ext import commands
import asyncio
import sounddevice as sd
import numpy as np
import subprocess

def load_token():
    with open("TOKEN.secret", "r") as file:
        return file.read().strip()

TOKEN = load_token()

# Define the bot with a command prefix
intents = discord.Intents.default()
intents.message_content = True  # Make sure this is set
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Audio streaming parameters
SAMPLE_RATE = 48000  # Should match Discord's requirements
CHANNELS = 2
CHUNK_SIZE = 1024  # Buffer size

vc = None  # Voice client reference
stream_process = None  # FFmpeg process


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.command()
async def join(ctx):
    """Joins the voice channel of the user"""
    if ctx.author.voice:
        global vc
        vc = await ctx.author.voice.channel.connect()
        await ctx.send("Joined voice channel!")
    else:
        await ctx.send("You need to be in a voice channel!")


@bot.command()
async def leave(ctx):
    """Leaves the voice channel"""
    global vc, stream_process
    if vc:
        await vc.disconnect()
        vc = None
        await ctx.send("Disconnected from voice channel.")
    if stream_process:
        stream_process.kill()
        stream_process = None

@bot.command()
async def stream(ctx):
    """Streams system audio from a virtual audio cable"""
    global vc, stream_process

    if not vc:
        await ctx.send("I'm not in a voice channel! Use `!join` first.")
        return

    if stream_process:
        await ctx.send("Already streaming!")
        return

    await ctx.send("Starting audio stream...")

    # FFmpeg command to capture audio from the virtual cable
    stream_process = subprocess.Popen(
        [
            "ffmpeg",
            "-f", "dshow",  # Use DirectShow for Windows audio capture
            "-i", "audio=CABLE Output (VB-Audio Virtual Cable)",  # Input device
            "-ac", "2",  # Stereo
            "-ar", "48000",  # Sample rate for Discord
            "-f", "s16le",  # PCM format
            "-acodec", "pcm_s16le",  # Raw PCM audio
            "pipe:1"
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL  # Suppress errors
    )

    # Play the captured audio stream
    vc.play(discord.PCMAudio(stream_process.stdout), after=lambda e: stop_stream())


def stop_stream():
    """Stops the audio stream"""
    global stream_process
    if stream_process:
        stream_process.kill()
        stream_process = None


@bot.command()
async def stop(ctx):
    """Stops the streaming"""
    global vc, stream_process
    if vc and vc.is_playing():
        vc.stop()
        stop_stream()
        await ctx.send("Stopped streaming audio.")
    else:
        await ctx.send("I'm not currently streaming.")

bot.run(TOKEN)
