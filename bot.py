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

async def msg(context, user, guild, sys = False):
	e = discord.Embed(title=context[0], description=context[1], timestamp=datetime.datetime.utcnow())
	e.set_thumbnail(url=user.avatar_url)
	if sys:
		channel = discord.utils.get(guild.text_channels, name="system-log")
	else:
		channel = discord.utils.get(guild.text_channels, name="log")
	return await channel.send(embed=e)

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
		return await msg(["🌟 A new user has joined the server 🌟", "*Please give a warm welcome to **" + member.name + "**!*"], member, member.guild)

	async def on_member_remove(self, member):
		if member == self.user:
			return
		return await msg(["👋 A user has left the server 👋", "*We're sorry to see you go, **" + member.name + "**. Please come back again soon.~*"], member, member.guild)

	async def on_member_ban(self, guild, user):
		if user == self.user:
			return
		return await msg(["🔨 A user has been banned from the server 🔨", "*We're sorry to see you go, **" + user.name + "**. We wish things had been better than this...*"], user, guild)

	async def on_member_unban(self, guild, user):
		if user == self.user:
			return
		return await msg(["✅ A user has been unbanned from the server ✅", "*It's your lucky day, **" + user.name + "**! We hope to see you come back!*"], user, guild)

	async def on_message_edit(self, before, after):
		if before.author == self.user:
			return
		if before.content == after.content:
			return
		return await msg(["⚠ A message has been edited on the server ⚠", "**Author:** " + str(before.author) + "\n**Channel:** " + before.channel.mention + "\n**Before:** " + before.content + "\n**After:** " + after.content], before.author, before.guild, True)

	async def on_message_delete(self, message):
		if message.author == self.user:
			return
		return await msg(["🚫 A message has been removed from the server 🚫", "**Author:** " + str(message.author) + "\n**Channel:** " + message.channel.mention + "\n**Content:** " + message.content], message.author, message.guild, True)

	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == "⭐":
			m = await self.get_channel(payload.channel_id).get_message(payload.message_id)
			amt = len(await discord.utils.get(m.reactions, emoji=str(payload.emoji)).users().flatten())
			if amt > 2:
				data = fs()
				if str(m.id) in data["messages"]:
					h = await discord.utils.get(m.guild.text_channels, name="hall-of-fame").get_message(data["messages"][str(m.id)])
					await h.edit(content="⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " stars and counting... ⭐\n\n" + m.content)
				else:
					import io
					import aiohttp

					a = []
					for atch in m.attachments:
						async with aiohttp.ClientSession() as session:
							async with session.get(atch.url) as resp:
								if resp.status != 200:
									print("A file was not found while inducting a message to the Hall of Fame in " + m.guild.name + ".")
								a.append(discord.File(io.BytesIO(await resp.read()), atch.filename))
								await session.close()
					msg = await discord.utils.get(m.guild.text_channels, name="hall-of-fame").send("⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " star" + ("s" if amt > 1 else "") + " and counting... ⭐\n\n" + m.content, files=a)
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
