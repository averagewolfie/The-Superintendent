import discord
import superutils

from discord.ext import commands

class Superintendent(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="))", case_insensitive=True)

	async def on_ready(self):
		superutils.load_extensions(self, False)
		print("\nInitialization complete -\n    User: " + str(self.user) + "\n    ID: " + str(self.user.id))

if __name__ == "__main__":
	Superintendent().run(superutils.fs()["bot_token"])
