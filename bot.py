import discord
from discord.ext import commands

token = open("../minatsutoken.txt", "r")

startup_extensions = ["ticket"]

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print("----------")
    print("Logged in as: {}.".format(bot.user.name))
    print("Invite link: https://discordapp.com/oauth2/authorize?&client_id={}&scope=bot&permissions=0".format(bot.user.id))
    print("----------")

    for m in startup_extensions:
        bot.load_extension(m)
        print("Loaded {0}.py".format(m))

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token.read())
