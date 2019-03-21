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

	@commands.group()
	async def suggestion(self, ctx):
		if ctx.invoked_subcommand is None:
			return await ctx.channel.send("The correct usage of this command is `))suggestion add/edit/respond`.")

	@suggestion.command()
	async def add(self, ctx, *, content):
		if len(content) < 32:
			return await ctx.channel.send("Please offer a suggestion at least 32 characters in length, to explain the context of the suggestion.")
		data = superutils.fs()
		if not str(ctx.guild.id) in data["suggestions"]:
			data["suggestions"][str(ctx.guild.id)] = {}
		e = discord.Embed(title=("Suggestion #" + str(len(data["suggestions"][str(ctx.guild.id)]) + 1)), description=content, colour=0x5f7d4e)
		e.set_thumbnail(url=ctx.author.avatar_url)
		e.add_field(name="This suggestion is open!", value="Please vote on it and share your thoughts in <#555440421149474829>!")
		e.set_author(name=str(ctx.author),icon_url=ctx.author.avatar_url)
		msg = await discord.utils.get(ctx.guild.channels, name="suggestions_box").send(embed=e)
		await msg.add_reaction("👍")
		await msg.add_reaction("👎")
		data["suggestions"][str(ctx.guild.id)][("#" + str(len(data["suggestions"][str(ctx.guild.id)]) + 1))] = {"id":msg.id, "outcome":"open", "response":""}
		superutils.fs(data)

	@suggestion.command()
	async def edit(self, ctx, number, *, content):
		try:
			data = superutils.fs()
			msg = await discord.utils.get(ctx.guild.channels, name="suggestions_box").get_message(data["suggestions"][str(ctx.guild.id)][("#" + number)]["id"])
		except:
			return await ctx.channel.send(number + " does not seem to be a valid suggestion index.")
		e = msg.embeds[0]
		if e.author.name != str(ctx.author):
			return await ctx.channel.send("You cannot edit someone else's suggestion, only your own!")
		if data["suggestions"][str(ctx.guild.id)][("#" + number)]["outcome"] != "open":
			return await ctx.channel.send("Suggestion #" + number + " has already been closed. Please contact a staff member if you need to reopen the suggestion.")
		if len(content) < 32:
			return await ctx.channel.send("Please offer a suggestion at least 32 characters in length, to explain the context of the suggestion.")
		e.description = content
		await msg.edit(embed=e)

	@suggestion.command()
	async def respond(self, ctx, number, outcome, *, response = None):
		if not ctx.author.guild_permissions.manage_messages:
			return await ctx.channel.send("You do not have the applicable permissions to use this command!")
		try:
			data = superutils.fs()
			msg = await discord.utils.get(ctx.guild.channels, name="suggestions_box").get_message(data["suggestions"][str(ctx.guild.id)][("#" + number)]["id"])
		except:
			await ctx.channel.send(number + " does not seem to be a valid suggestion index.")
		outcomes = {"approve": {"response":"has been approved:", "colour": 0x00cc00},"deny": {"response":"has been denied:", "colour": 0xcc0000},"existing": {"response":"has already been addressed:", "colour": 0xff6600},"duplicate": {"response":"has already been submitted:", "colour": 0x9900cc},"inappropriate": {"response":"was considered inappropriate:", "colour": 0x990000},"reopen": {"response":"is open!", "colour": 0x5f7d4e}}
		if not outcome.lower() in outcomes:
			return await ctx.channel.send("\"" + outcome.capitalize() + "\" does not seem to be a valid suggestion closure type.")
		if outcome != "reopen" and (response is None or len(response) < 32):
			return await ctx.channel.send("Please offer a reason at least 32 characters in length, to explain the context of the desired outcome.")
		e = msg.embeds[0]
		e.colour = outcomes[outcome.lower()]["colour"]
		e.set_field_at(0, name=("The suggestion " + outcomes[outcome.lower()]["response"]), value="Please vote on it and share your thoughts in <#555440421149474829>!" if response is None else response)
		await msg.edit(embed=e)
		data["suggestions"][str(ctx.guild.id)][("#" + number)]["outcome"] = outcome
		data["suggestions"][str(ctx.guild.id)][("#" + number)]["response"] = response
		superutils.fs(data)

def setup(bot):
	bot.add_cog(New(bot))
