import discord
from discord.ext import commands

class New:
	def __init__(self, bot):
		self.bot = bot

	@commands.command()
	async def prune(self, ctx, amount:int):
		try:
			if not type(amount) is int:
				return await ctx.channel.send("You need to specify an *integer* value of messages to prune.")
			await ctx.channel.purge(limit=amount + 1, bulk=True)
			return await ctx.channel.send(content=str(amount) + " messages deleted! One additional removal has also occurred, for the message which you sent to invoke the command.")
		except Exception as e:
			print("An error has occurred during \"on_message()\".\n" + type(e).__name__ + ": " + str(e))

def setup(bot):
	bot.add_cog(New(bot))
