import discord

import superutils

from discord.ext import commands

class New(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["purge","remove","delete"])
	async def prune(self, ctx, amount):
		try:
			amount = int(amount)
		except:
			return await ctx.channel.send("You need to specify an *integer* value of messages to prune.")
		await ctx.channel.purge(limit=amount + 1, bulk=True)
		return await ctx.channel.send(content=str(amount) + " messages deleted! One additional removal has also occurred, for the message which you sent to invoke the command.")

	@commands.command(aliases=["about","bullshit"])
	async def info(self, ctx):
		e = discord.Embed(title="The Superintendent", description="A bot.", colour=0x5f7d4e)
		e.add_field(name="Umm... could you be more specific?", value="I am a Discord bot with the task of tracking people who join, leave, and say things on " + ctx.message.guild.name + ".")
		e.add_field(name="And who is your creator?", value="I am not allowed to say Toron's name when that question is asked.")
		e.set_thumbnail(url=self.bot.user.avatar_url)
		await ctx.channel.send(embed = e)

	@commands.command(aliases=["reload", "re"])
	async def reload_extensions(self, ctx):
		return superutils.load_extensions(self.bot, True)

	@commands.command()
	async def suggestions(self, ctx):
		try:
			hst = await ctx.channel.history().flatten()
			for i in hst:
				if i.content.lower().startswith() == "suggestion":
					await i.add_reaction("👍")
					await i.add_reaction("👎")
		except:
			print("Something went wrong, dumbass.")

def setup(bot):
	bot.add_cog(New(bot))
