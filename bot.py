import discord
import json
import asyncio
import random
import datetime

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_join(member):
	if member == client.user:
		return
	e = discord.Embed(title="🌟 A new user has joined the server 🌟", description="*Please give a warm welcome to **" + member.name + "**!*", timestamp=datetime.datetime.utcnow())
	e.set_thumbnail(url=member.avatar_url)
	return await member.guild.get_channel(546592885982887936).send(embed=e) # Preferably a system-log channel for messages

@client.event
async def on_member_remove(member):
	if member == client.user:
		return
	e = discord.Embed(title="👋 A user has left the server 👋", description="*We're sorry to see you go, **" + member.name + "**. Please come back again soon.~*", timestamp=datetime.datetime.utcnow())
	e.set_thumbnail(url=member.avatar_url)
	return await member.guild.get_channel(546592885982887936).send(embed=e) # Preferably a system-log channel for messages

@client.event
async def on_message_edit(before, after):
	if before.author == client.user:
		return
	if before.content == after.content:
		return
	e = discord.Embed(title="⚠ A message has been edited on the server ⚠", description="**Author:** " + str(before.author) + "\n**Channel:** " + before.channel.mention + "\n**Before:** " + before.content + "\n**After:** " + after.content, timestamp=datetime.datetime.utcnow())
	e.set_thumbnail(url=before.author.avatar_url)
	return await before.guild.get_channel(546595428326440982).send(embed=e) # Preferably a user-log channel for members

@client.event
async def on_message_delete(message):
	if message.author == client.user:
		return
	e = discord.Embed(title="🚫 A message has been removed from the server 🚫", description="**Author:** " + str(message.author) + "\n**Channel:** " + message.channel.mention + "\n**Content:** " + message.content, timestamp=datetime.datetime.utcnow())
	e.set_thumbnail(url=message.author.avatar_url)
	return await message.guild.get_channel(546595428326440982).send(embed=e) # Preferably a user-log channel for members

client.run("""No... why would I show you all the bot token? Use your own. :<""")
