import discord
from discord.ext import commands
import json
from pprint import pprint

token = open("../minatsutoken.txt", "r")
startup_extensions = ["ticket"]
bot = commands.Bot(command_prefix='!')

# welcome messages will be in the format "Welcome @mention to the server. Funny Minecraft related quote".
welcomemessages = ["Remember not to dig straight down!", "You will *nether* want to leave this place."]

@bot.event
async def on_ready():
    print("----------")
    print("Logged in as: {}.".format(bot.user.name))
    print("Invite link: https://discordapp.com/oauth2/authorize?&client_id={}&scope=bot&permissions=0".format(bot.user.id))
    print("----------")

    for m in startup_extensions:
        bot.load_extension(m)
        print("Loaded {0}.py".format(m))

@bot.event
async def on_member_join(member):
    with open("config.json") as f:
        config = json.load(f)
    for channel in member.server.channels:
        if channel.id == data["welcomeMessageChannelID"]:
            welcomeMessage = random.choice(data["welcomeMessages"])
            await bot.send_message(channel, "Welcome {} to the server! {}".format(member.mention, welcomeMessage))

@bot.command(pass_context=True)
async def adddev(ctx, message):
    with open("config.json") as f:
        config = json.load(f)
    if ctx.message.author.id not in config["devIDs"]:
        return

    for member in ctx.message.server.members:
        if member.mention == message:
            config["devIDs"].append(member.id)
    await bot.send_message(ctx.message.channel, "**{} added to devs.**".format(member.mention))

    
@bot.command(pass_context=True)
async def setwelcomechannel(ctx):
    with open("config.json") as f:
        config = json.load(f)
        
    if ctx.message.author.id not in config["devIDs"]:
        return
    
    
    
    channelid = ctx.message.channel.id
    config["welcomeMessageChannelID"] = channelid
    
    with open('config.json', 'w') as outfile:
        json.dump(config, outfile)

    await bot.delete_message(ctx.message)
    await bot.send_message(ctx.message.channel, "**{} has been set to the welcome channel.**\n*Users who join this channel will be greeted with a welcome message.*".format(ctx.message.channel.mention))
    

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))

    bot.run(token.read())
