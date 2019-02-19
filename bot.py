import discord
import json
import asyncio
import random
import datetime

from discord.ext import commands

extensions = {
	"extensions.new"
}

def fs(data = None):
	try:
		if data is None:
			return json.load(open("data.json")) # might have to make your own data.json
		else:
			json.dump(data, open("data.json", "w"), indent=4)
	except Exception as e:
		print("An error has occurred while attempting to retrieve the data file.\n" + type(e).__name__ + ": " + str(e))

class Superintendent(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="))", case_insensitive=True)

	async def on_ready(self):
		for ext in extensions:
			try:
				print("Loading extension \"" + ext + "\"...")
				self.load_extension(ext)
			except Exception as e:
				print("An error has occurred while trying to load an extension \"" + ext + "\".\n" + type(e).__name__ + ": " + str(e))
		print("Initialization complete -\nUser: " + str(self.user) + "\nID: " + str(self.user.id))

	async def on_member_join(self, member):
		try:
			if member == self.user:
				return
			e = discord.Embed(title="🌟 A new user has joined the server 🌟", description="*Please give a warm welcome to **" + member.name + "**!*", timestamp=datetime.datetime.utcnow())
			e.set_thumbnail(url=member.avatar_url)
			return await member.guild.get_channel(546592885982887936).send(embed=e) # Preferably a system-log channel for messages
		except Exception as e:
			print("An error has occurred during \"on_member_join()\".\n" + type(e).__name__ + ": " + str(e))

	async def on_member_remove(self, member):
		try:
			if member == self.user:
				return
			e = discord.Embed(title="👋 A user has left the server 👋", description="*We're sorry to see you go, **" + member.name + "**. Please come back again soon.~*", timestamp=datetime.datetime.utcnow())
			e.set_thumbnail(url=member.avatar_url)
			return await member.guild.get_channel(546592885982887936).send(embed=e) # Preferably a system-log channel for messages
		except Exception as e:
			print("An error has occurred during \"on_member_remove()\".\n" + type(e).__name__ + ": " + str(e))

	async def on_message_edit(self, before, after):
		try:
			if before.author == self.user:
				return
			if before.content == after.content:
				return
			e = discord.Embed(title="⚠ A message has been edited on the server ⚠", description="**Author:** " + str(before.author) + "\n**Channel:** " + before.channel.mention + "\n**Before:** " + before.content + "\n**After:** " + after.content, timestamp=datetime.datetime.utcnow())
			e.set_thumbnail(url=before.author.avatar_url)
			return await before.guild.get_channel(546595428326440982).send(embed=e) # Preferably a user-log channel for members
		except Exception as e:
			print("An error has occurred during \"on_message_edit()\".\n" + type(e).__name__ + ": " + str(e))

	async def on_message_delete(self, message):
		try:
			if message.author == self.user:
				return
			e = discord.Embed(title="🚫 A message has been removed from the server 🚫", description="**Author:** " + str(message.author) + "\n**Channel:** " + message.channel.mention + "\n**Content:** " + message.content, timestamp=datetime.datetime.utcnow())
			e.set_thumbnail(url=message.author.avatar_url)
			return await message.guild.get_channel(546595428326440982).send(embed=e) # Preferably a user-log channel for members
		except Exception as e:
			print("An error has occurred during \"on_message_delete()\".\n" + type(e).__name__ + ": " + str(e))

	async def on_raw_reaction_add(self, payload):
		try:
			if str(payload.emoji) == "⭐":
				m = await self.get_channel(payload.channel_id).get_message(payload.message_id)
				amt = len(await discord.utils.get(m.reactions, emoji=str(payload.emoji)).users().flatten())
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

	async def on_raw_reaction_remove(self, payload):
		try:
			if str(payload.emoji) == "⭐":
				m = await self.get_channel(payload.channel_id).get_message(payload.message_id)
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

if __name__ == "__main__":
	Superintendent().run(fs()["bot_token"])
