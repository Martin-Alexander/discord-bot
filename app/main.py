import discord
import asyncio
import os
import fbchat
import random
import re

from fbchat import Client
from fbchat.models import *

previous_questions = {}

# fbchat_client = Client(os.environ["FB_EMAIL"], os.environ["FB_PASSWORD"])
discord_client = discord.Client()

messanger_notification_gang = []
for messanger_member in os.environ["MESSANGER_NOTIFICATION_GANG"].split(","):
	if messanger_member != "":
		messanger_member = messanger_member.split(":")
		messanger_notification_gang.append({"discord_id": messanger_member[0], "fb_id": messanger_member[1]})

word = os.environ["SPECIAL_WORD"]

@discord_client.event
async def on_ready():
	# Find text and voice channel
	for server in discord_client.servers:
		for channel in server.channels:
			if channel.name == "autistesanonymous":
				the_text_channel = channel
			elif channel.name == "voice_discussion":
				voice_one = channel

	# Attach voice_state_update event listen to all memebers
	for server in discord_client.servers:
		for member in server.members:
			@discord_client.event
			async def on_voice_state_update(before, after):
				if (
					before.voice_channel != voice_one and
					after.voice_channel == voice_one and
					len(after.voice_channel.voice_members) == 1
					):
					await discord_client.send_message(the_text_channel, "@here " + before.name + " has started a group call")
					for messanger_member in messanger_notification_gang:
						if after.id != messanger_member["discord_id"]:
							pass
							# fbchat_client.sendMessage(before.name + " has started a group call", thread_id=messanger_member["fb_id"], thread_type=ThreadType.USER)
				elif (
					before.voice_channel == voice_one and 
					len(voice_one.voice_members) == 0
					):
					await discord_client.send_message(the_text_channel, "Group call ended")

@discord_client.event
async def on_message(message):
	message_content = message.content.lower().rstrip()

	# Testing messanger notification gang
	if message_content.startswith("ping:") and message.author.id == "179396248875302912":
		for messanger_member in messanger_notification_gang:
			if messanger_member["discord_id"] != "179396248875302912":
				pass
				# fbchat_client.sendMessage(re.sub("ping: ", "", message_content), thread_id=messanger_member["fb_id"], thread_type=ThreadType.USER)		
	
	# Get history
	if message_content == "history, " + word:
		await discord_client.send_message(message.channel, str(previous_questions))

	# Forget history
	if message_content == "forget it all, " + word and message.author.id == "179396248875302912":
		previous_questions.clear()

	# Ask questions
	if message_content.startswith(word) and message_content.endswith('?'):
		if message_content == word + ", are you there?" or message_content == word + " are you there?":
			await discord_client.send_message(message.channel, "Yes, I am here")
		else:
			already_asked = False
			for question in previous_questions.keys():
				if question == message_content:
					await discord_client.send_message(message.channel, previous_questions[message_content])
					already_asked = True
			if already_asked == False:    
				if random.randint(0, 1) == 1:
					previous_questions[message_content] = "Yes"
				else:
					previous_questions[message_content] = "No"
				await discord_client.send_message(message.channel, previous_questions[message_content])

discord_client.run(os.environ["CLIENT_KEY"])