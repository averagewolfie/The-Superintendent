import json

def fs(data = None):
	try:
		if data is None:
			return json.load(open("data.json")) # might have to make your own data.json
		else:
			json.dump(data, open("data.json", "w"), indent=4)
	except Exception as e:
		print("An error has occurred while attempting to retrieve the data file.\n" + type(e).__name__ + ": " + str(e))

def load_extensions(bot, which):
	print(("Reloading" if which else "Loading"), "extensions:")
	extensions = fs()["extensions"]
	for ext in extensions:
		try:
			if which:
				print("    Unloading extension \"" + ext + "\"...")
				bot.unload_extension(ext)
				print("        Extension unloaded!")
			print("    Loading extension \"" + ext + "\"...")
			bot.load_extension(ext)
			print("        Extension loaded!")
		except Exception as e:
			print("        An error has occurred while trying to load an extension \"" + ext + "\".\n" + type(e).__name__ + ": " + str(e))
	print("\nExtensions", ("reloaded!" if which else "loaded!"))
