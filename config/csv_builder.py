import discord
import asyncio

discord_client = discord.Client()

@discord_client.event
async def on_ready():
  MEMBERS = open("members.csv", "w")
  for server in discord_client.servers:
    for member in server.members:
      MEMBERS.write(member.name + "," + str(member.id) + "," "NULL" + "\n")
  MEMBERS.close()
  print("done")

discord_client.run("MzQ5NzUzMjExODA2MTU0NzUz.DH6FVw.HQ5GCZYuwNdbLRZn-Bh27COrVg4")