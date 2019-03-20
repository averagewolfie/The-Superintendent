# The Superintendent
A bot for "Voli-Tec Station". Also my first open-source project, ever, and my first Git project, ever...

This bot has minimal functionality. It's MOSTLY up to the owner of the server what should be added or changed on the bot, but I will not be denying opportunities for other Gitters to make pull requests or commit issues for the bot. As a matter of fact, have at it. :3

## Here are changes for the build of 18 March 2019:
* "bot.py" is now only used during bot initialization. Nearly all of its code was split between three other files. I won't go into details.
* Added the ability to reload all of the extensions ("hot restarting") without having to reboot the entire bot (or consequently clearing the bot's internal message cache).
* Added a small feature for suggestion making: if a member's message starts with a trigger keyword (say, "suggestion"), then the bot will give other members the option of adding an emoticon, which will allow suggestion authors to cast their own votes if needed.
* For suggestions which haven't been tracked by the bot, a command exists to search through a channel's message history and add the reactions, but it might not be very efficient after twenty straight suggestions.
* The Hall of Fame no longer does uploads either (after making this change with on_message_delete() prior), and instead grabs the link of a post's existing attachment and posts that along with the HOF reiteration of the starred message.
