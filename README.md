# What does the app do?
It helps you stream the Pocket Bard Desktop apps audio to your discord voice channels with a Bot

# Requirements
## python libraries
- discord.py
- discord.ext.commands
- ffmpeg
- soundddevice
- numpy

## other requirements
- Virtual Audio Cable
- PocketBard

# Setup
1. Virtual Audio Cable setup:
  In the Win11 Settings:
  "Sysytem -> Sound -> Volume Mixer"
  Set the 'Pocket Bard' application's output device to the Virtual Cable's Input (by default: "CABLE INPUT (VB-Audio Virtual Cable)").
  Make sure nothing else uses the virtual cable. 

3. Bot setup:
  Create a TOKEN.secret in the same directory where the pocket_bard.py is and copy your bot's token in it

4. Discord setup
   Make your bot join your server and give it the "Connect" and "Speak" permisions.

# Starting the bot
In the commandline type: "python pocket_bard.py".

# Bot commands
!join: joins the voice channel
!leave: leaves the voice cahnnel
!stream: streams the audio output of pocket bard
!stop: stops the audio stream
