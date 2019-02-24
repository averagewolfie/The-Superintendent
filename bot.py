import discord
import json
import asyncio
import random
import datetime
import traceback

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
		if member == self.user:
			return
		e = discord.Embed(title="🌟 A new user has joined the server 🌟", description="*Please give a warm welcome to **" + member.name + "**!*", timestamp=datetime.datetime.utcnow())
		e.set_thumbnail(url=member.avatar_url)
		return await discord.utils.get(member.guild.text_channels, name="log").send(embed=e)

	async def on_member_remove(self, member):
		if member == self.user:
			return
		e = discord.Embed(title="👋 A user has left the server 👋", description="*We're sorry to see you go, **" + member.name + "**. Please come back again soon.~*", timestamp=datetime.datetime.utcnow())
		e.set_thumbnail(url=member.avatar_url)
		return await discord.utils.get(member.guild.text_channels, name="log").send(embed=e)

	async def on_message_edit(self, before, after):
		if before.author == self.user:
			return
		if before.content == after.content:
			return
		e = discord.Embed(title="⚠ A message has been edited on the server ⚠", description="**Author:** " + str(before.author) + "\n**Channel:** " + before.channel.mention + "\n**Before:** " + before.content + "\n**After:** " + after.content, timestamp=datetime.datetime.utcnow())
		e.set_thumbnail(url=before.author.avatar_url)
		return await discord.utils.get(before.guild.text_channels, name="system-log").send(embed=e)

	async def on_message_delete(self, message):
		if message.author == self.user:
			return
		e = discord.Embed(title="🚫 A message has been removed from the server 🚫", description="**Author:** " + str(message.author) + "\n**Channel:** " + message.channel.mention + "\n**Content:** " + message.content, timestamp=datetime.datetime.utcnow())
		e.set_thumbnail(url=message.author.avatar_url)
		return await discord.utils.get(message.guild.text_channels, name="system-log").send(embed=e)

	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == "⭐":
			m = await self.get_channel(payload.channel_id).get_message(payload.message_id)
			amt = len(await discord.utils.get(m.reactions, emoji=str(payload.emoji)).users().flatten())
			if amt > 2:
				print(m.author.name, amt)
				data = fs()
				if str(m.id) in data["messages"]:
					h = await discord.utils.get(m.guild.text_channels, name="hall-of-fame").get_message(data["messages"][str(m.id)])
					await h.edit(content="⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " stars and counting... ⭐\n\n" + m.content)
				else:
					import io
					import aiohttp

					a = m.attachments
					a2 = []
					for atch in m.attachments:
						async with aiohttp.ClientSession() as session:
							async with session.get(atch.url) as resp:
								if resp.status != 200:
									print("A file was not found while inducting a message to the Hall of Fame in " + m.guild.name + ".")
								a2.append(discord.File(io.BytesIO(await resp.read()), atch.filename))
								await session.close()
					msg = await discord.utils.get(m.guild.text_channels, name="hall-of-fame").send("⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " star" + ("s" if amt > 1 else "") + " and counting... ⭐\n\n" + m.content, files=a2)
					data["messages"][str(m.id)] = msg.id
					fs(data)

	async def on_raw_reaction_remove(self, payload):
		if str(payload.emoji) == "⭐":
			m = await self.get_channel(payload.channel_id).get_message(payload.message_id)
			data = fs()
			h = await discord.utils.get(m.guild.text_channels, name="hall-of-fame").get_message(data["messages"][str(m.id)])
			try:
				amt = len(await discord.utils.get(m.reactions, emoji=str(payload.emoji)).users().flatten())
				await h.edit(content="⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " star" + ("s" if amt > 1 else "") + " and counting... ⭐\n\n" + m.content)
			except: # because if there are no more stars, then it won't be able to find the message using that method, so just chuck it.
				await h.delete()
				del data["messages"][str(m.id)]
				fs(data)

	async def on_error(self, event, *args, **kwargs):
		try:
			guild = discord.utils.get(self.guilds, id=args[0].guild_id)
			channel = discord.utils.get(guild.text_channels, id=args[0].channel_id)
			user = discord.utils.get(self.users, id=args[0].user_id)
		except AttributeError:
			guild = discord.utils.get(self.guilds, id=args[0].guild.id)
			channel = discord.utils.get(guild.text_channels, id=args[0].channel.id)
			if (type(args[0]) == discord.Message):
				user = discord.utils.get(self.users, id=args[0].author.id)
			else:
				user = discord.utils.get(self.users, id=args[0].user.id)
		except Exception as e:
			await self.get_user(397080996312514580).send("While handling an exception for \"" + str(event) + "\", another one has occurred which prevented the process from completing.\n" + type(e).__name__ + ": " + str(e))
		finally:
			return await self.get_user(397080996312514580).send("An exception has occurred during \"" + str(event) + "\".\n\n**Guild:** " + guild.name + "\n**Channel:** " + channel.mention + "\n**User:** " + str(user) + "\n\n`" + traceback.format_exc() + "`")

if __name__ == "__main__":
	Superintendent().run(fs()["bot_token"])
