import discord
import json
import asyncio
import random
import datetime

client = discord.Client()

@client.event
async def on_ready():
	print("We have logged in as " + str(client.user))

def fs(data = None):
	try:
		if data is None:
			return json.load(open("data.json")) # might have to make your own data.json
		else:
			json.dump(data, open("data.json", "w"), indent=4)
	except Exception as e:
		print("An error has occurred while attempting to retrieve the data file.\n" + type(e).__name__ + ": " + str(e))

@client.event
async def on_message(message):
	try:
		if client.user == message.author:
			return
		if message.content.lower().startswith("prune "):
			amt = message.content.lower()[6:]
			try:
				hst = await message.channel.history(limit=int(amt) + 1).flatten()
			except:
				return await message.channel.send("You need to specify an *integer* value of messages to prune.")
			test = await message.channel.send("Pruning messages...")
			for i in hst:
				await i.delete()
			return await test.edit(content=amt + " messages deleted! One additional removal has also occurred, for the message which you sent to invoke the command.")
	except Exception as e:
		print("An error has occurred during \"on_message()\".\n" + type(e).__name__ + ": " + str(e))

@client.event
async def on_member_join(member):
	try:
		if member == client.user:
			return
		e = discord.Embed(title="🌟 A new user has joined the server 🌟", description="*Please give a warm welcome to **" + member.name + "**!*", timestamp=datetime.datetime.utcnow())
		e.set_thumbnail(url=member.avatar_url)
		return await member.guild.get_channel(546592885982887936).send(embed=e) # Preferably a system-log channel for messages
	except Exception as e:
		print("An error has occurred during \"on_member_join()\".\n" + type(e).__name__ + ": " + str(e))

@client.event
async def on_member_remove(member):
	try:
		if member == client.user:
			return
		e = discord.Embed(title="👋 A user has left the server 👋", description="*We're sorry to see you go, **" + member.name + "**. Please come back again soon.~*", timestamp=datetime.datetime.utcnow())
		e.set_thumbnail(url=member.avatar_url)
		return await member.guild.get_channel(546592885982887936).send(embed=e) # Preferably a system-log channel for messages
	except Exception as e:
		print("An error has occurred during \"on_member_remove()\".\n" + type(e).__name__ + ": " + str(e))

@client.event
async def on_message_edit(before, after):
	try:
		if before.author == client.user:
			return
		if before.content == after.content:
			return
		e = discord.Embed(title="⚠ A message has been edited on the server ⚠", description="**Author:** " + str(before.author) + "\n**Channel:** " + before.channel.mention + "\n**Before:** " + before.content + "\n**After:** " + after.content, timestamp=datetime.datetime.utcnow())
		e.set_thumbnail(url=before.author.avatar_url)
		return await before.guild.get_channel(546595428326440982).send(embed=e) # Preferably a user-log channel for members
	except Exception as e:
		print("An error has occurred during \"on_message_edit()\".\n" + type(e).__name__ + ": " + str(e))

@client.event
async def on_message_delete(message):
	try:
		if message.author == client.user:
			return
		e = discord.Embed(title="🚫 A message has been removed from the server 🚫", description="**Author:** " + str(message.author) + "\n**Channel:** " + message.channel.mention + "\n**Content:** " + message.content, timestamp=datetime.datetime.utcnow())
		e.set_thumbnail(url=message.author.avatar_url)
		return await message.guild.get_channel(546595428326440982).send(embed=e) # Preferably a user-log channel for members
	except Exception as e:
		print("An error has occurred during \"on_message_delete()\".\n" + type(e).__name__ + ": " + str(e))

@client.event
async def on_raw_reaction_add(payload):
	try:
		if str(payload.emoji) == "⭐":
			m = await client.get_channel(payload.channel_id).get_message(payload.message_id)
			amt = len(await discord.utils.get(m.reactions, emoji=str(payload.emoji)).users().flatten())
			print(amt)
			if amt > 0:
				data = fs()
				if str(m.id) in data["messages"]:
					h = await m.guild.get_channel(546988876007473162).get_message(data["messages"][str(m.id)]) # Preferably a Starboard rehash channel
					await h.edit(content="⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " stars and counting... ⭐\n\n" + m.content)
				else:
					a = m.attachments
					msg = await m.guild.get_channel(546988876007473162).send("⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " star" + ("s" if amt > 1 else "") + " and counting... ⭐\n\n" + m.content, files=a) # Preferably a Starboard rehash channel
					data["messages"][str(m.id)] = msg.id
					fs(data)
	except Exception as e:
		print("An error has occurred during \"on_raw_reaction_add()\".\n" + type(e).__name__ + ": " + str(e))

@client.event
async def on_raw_reaction_remove(payload):
	try:
		if str(payload.emoji) == "⭐":
			m = await client.get_channel(payload.channel_id).get_message(payload.message_id)
			data = fs()
			h = await m.guild.get_channel(546988876007473162).get_message(data["messages"][str(m.id)]) # Preferably a Starboard rehash channel
			try:
				amt = len(await discord.utils.get(m.reactions, emoji=str(payload.emoji)).users().flatten())
				await h.edit(content="⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " star" + ("s" if amt > 1 else "") + " and counting... ⭐\n\n" + m.content)
			except: # because if there are no more stars, then it won't be able to find the message using that method, so just chuck it.
				await h.delete()
				del data["messages"][str(m.id)]
				fs(data)
	except Exception as e:
		print("An error has occurred during \"on_raw_reaction_remove()\".\n" + type(e).__name__ + ": " + str(e))

client.run(fs()["bot_token"])
