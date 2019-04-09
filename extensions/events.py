import discord
import datetime
import io
import aiohttp
import traceback
import superutils

from discord.ext import commands

async def msg(context, user, guild, sys = False):
	e = discord.Embed(title=context[0], timestamp=datetime.datetime.utcnow(), colour=0x5f7d4e)
	e.set_thumbnail(url=user.avatar_url)
	if type(context[1]) is str:
		e.description = context[1]
	else:
		for i in context:
			if i == e.title:
				continue
			e.add_field(name=i[0], value=i[1])
	if sys:
		channel = discord.utils.get(guild.text_channels, name="system-log")
	else:
		channel = discord.utils.get(guild.text_channels, name="log")
	return await channel.send(embed=e)

class Events(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	"""@commands.Cog.listener()
	async def on_message(self, message):
		if message.author == self.bot.user:
			return"""

	@commands.Cog.listener()
	async def on_member_join(self, member):
		if member == self.bot.user:
			return
		return await msg(["🌟 A new user has joined the server 🌟", "*Please give a warm welcome to **" + member.name + "**!*"], member, member.guild)

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		if member == self.bot.user:
			return
		return await msg(["👋 A user has left the server 👋", "*We're sorry to see you go, **" + member.name + "**. Please come back again soon.~*"], member, member.guild)

	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		if user == self.bot.user:
			return
		return await msg(["🔨 A user has been banned from the server 🔨", "*We're sorry to see you go, **" + user.name + "**. We wish things had been better than this...*"], user, guild)

	@commands.Cog.listener()
	async def on_member_unban(self, guild, user):
		if user == self.bot.user:
			return
		return await msg(["✅ A user has been unbanned from the server ✅", "*It's your lucky day, **" + user.name + "**! We hope to see you come back!*"], user, guild)

	@commands.Cog.listener()
	async def on_message_edit(self, before, after):
		if before.author == self.bot.user or message.author.bot:
			return
		if before.content == after.content:
			return
		return await msg(["⚠ A message has been edited on the server ⚠", ["Author", str(before.author)], ["Channel", before.channel.mention], ["Before", before.content if before.content != "" else "*(   no message content available   )*"], ["After", after.content if after.content != "" else "*(   no message content available   )*"]], before.author, before.guild, True)

	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.author == self.bot.user or message.author.bot:
			return
		arr = ["🚫 A message has been removed from the server 🚫", ["Author", str(message.author)], ["Channel", message.channel.mention]]
		if message.content != "":
			arr.append(["Content", message.content])
		for atch in message.attachments:
			async with aiohttp.ClientSession() as session:
				async with session.get(atch.proxy_url) as resp:
					if not str(resp.status).startswith("2"):
						print("A file was not found while deleting a message from", m.guild.name + ". (" + str(resp.status), str(resp) + ")")
						continue
					arr.append(["Attachment " + str(atch.id), atch.proxy_url])
					await session.close()
		return await msg(arr, message.author, message.guild, True)

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if str(payload.emoji) == "⭐":
			m = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
			amt = len(await discord.utils.get(m.reactions, emoji=str(payload.emoji)).users().flatten())
			if amt > 2:
				data = superutils.fs()
				a = ""
				for atch in m.attachments:
					a += "\n" + atch.url
				if str(m.id) in data["messages"]:
					h = await discord.utils.get(m.guild.text_channels, name="hall-of-fame").fetch_message(data["messages"][str(m.id)])
					await h.edit(content="⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " stars and counting... ⭐" + ("\n\n" + m.content if m.content != "" else m.content) + "\n" + a)
				else:
					msg = await discord.utils.get(m.guild.text_channels, name="hall-of-fame").send("⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " star" + ("s" if amt > 1 else "") + " and counting... ⭐" + ("\n\n" + m.content if m.content != "" else m.content) + "\n" + a)
					data["messages"][str(m.id)] = msg.id
					superutils.fs(data)

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, payload):
		if str(payload.emoji) == "⭐":
			m = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
			data = superutils.fs()
			try:
				h = await discord.utils.get(m.guild.text_channels, name="hall-of-fame").fetch_message(data["messages"][str(m.id)])
			except KeyError:
				print("Disregard reaction remove, the message does not exist in the Hall of Fame.")
			else:
				amt = len(await discord.utils.get(m.reactions, emoji=str(payload.emoji)).users().flatten())
				a = ""
				for atch in m.attachments:
					a += "\n" + atch.url
				if amt > 2:
					await h.edit(content="⭐ " + m.author.mention + " has a post in the Hall of Fame! " + str(amt) + " star" + ("s" if amt > 1 else "") + " and counting... ⭐" + ("\n\n" + m.content if m.content != "" else m.content) + "\n" + a)
				else:
					await h.delete()
					del data["messages"][str(m.id)]
					superutils.fs(data)

	@commands.Cog.listener()
	async def on_error(self, event, *args, **kwargs):
		try:
			guild = discord.utils.get(self.bot.guilds, id=args[0].guild_id)
			channel = discord.utils.get(guild.text_channels, id=args[0].channel_id)
			user = discord.utils.get(self.bot.users, id=args[0].user_id)
		except AttributeError:
			guild = discord.utils.get(self.bot.guilds, id=args[0].guild.id)
			channel = discord.utils.get(guild.text_channels, id=args[0].channel.id)
			if (type(args[0]) == discord.Message):
				user = discord.utils.get(self.bot.users, id=args[0].author.id)
			else:
				user = discord.utils.get(self.bot.users, id=args[0].user.id)
		except Exception as e:
			await self.bot.get_user(397080996312514580).send("While handling an exception for \"" + str(event) + "\", another one has occurred which prevented the process from completing.\n" + type(e).__name__ + ": " + str(e))
		finally:
			return await self.bot.get_user(397080996312514580).send("An exception has occurred during \"" + str(event) + "\".\n\n**Guild:** " + guild.name + "\n**Channel:** " + channel.mention + "\n**User:** " + str(user) + "\n\n`" + traceback.format_exc() + "`")

def setup(bot):
	bot.add_cog(Events(bot))
