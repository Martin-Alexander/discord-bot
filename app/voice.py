import discord
import asyncio
import websockets
import json

def new_poll_event(self):
  try:
    msg = yield from asyncio.wait_for(self.recv(), timeout=30.0, loop=self.loop)
    print(json.loads(msg))
    on_talk_event(json.loads(msg))
    yield from self.received_message(json.loads(msg))
  except:
    pass
  

discord.gateway.DiscordVoiceWebSocket.poll_event = new_poll_event

discord_client = discord.Client()
discord.opus.load_opus("libopus.so.0")
voice_client = None
player = None
player_status = "stopped"
in_voice_channel = False

word = os.environ["SPECIAL_WORD"]

@discord_client.event
async def on_ready():
  print("READY")

@discord_client.event
async def on_message(message):
  global voice_client, in_voice_channel, player, player_status
  if message.content.lower().rstrip() == "invite " + word:
    for server in discord_client.servers:
      for channel in server.channels:
        if channel.name == "voice_discussion":
          voice_client = await discord_client.join_voice_channel(channel)
          player = voice_client.create_ffmpeg_player('tone.wav')
          player.volume = 2
          player_status = "stopped"
          in_voice_channel = True
  elif message.content.lower().rstrip() == "remove " + word:
    for server in discord_client.servers:
      for channel in server.channels:
        if channel.name == "voice_discussion":
          player.stop()
          in_voice_channel = False
          player_status = "stopped"
          await voice_client.disconnect()

def on_talk_event(message_json): 
  global player, player_status
  if in_voice_channel and isinstance(message_json, dict) and "d" in message_json and isinstance(message_json["d"], dict) and "user_id" in message_json["d"]:
    if message_json["d"]["user_id"] == "266738403876274186" and message_json["d"]["speaking"] == True:
      if player_status == "stopped":
        player.start()
      else:
        player.resume()
      player_status = "running"
    elif message_json["d"]["user_id"] == "266738403876274186" and message_json["d"]["speaking"] == False:
      player.pause()
      player_status = "paused"


discord_client.run("MzQ5NzUzMjExODA2MTU0NzUz.DH6FVw.HQ5GCZYuwNdbLRZn-Bh27COrVg4")
