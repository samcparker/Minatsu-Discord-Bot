import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

maxtickets = 5

class Ticket():
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ticket(self, ctx):
        everyone = ""
        support = ""
        
        for role in ctx.message.server.roles:
            if role.name == "@everyone":
                everyone =  role
            elif role.name == "support":
                support = role

        if support == "":
            return await self.bot.send_message(ctx.message.channel, "This command is not set up properly, please contact a developer.")

        tickets = 0
        for channel in ctx.message.server.channels:
            name = channel.name
            if len(name.split("-")) == 2:
                if name.split("-")[0] == "open" and name.split("-")[1] == ctx.message.author.id:
                    tickets += 1
        if tickets >= maxtickets:
            return await self.bot.send_message(ctx.message.channel, "**{}: You have too many open tickets, use the command `!close` to close existing tickets.**".format(ctx.message.author.mention))
        
        channel = await self.bot.create_channel(ctx.message.server, "OPEN-" + ctx.message.author.id)    
            
        overwrite = discord.PermissionOverwrite()
        
        # @everyone : they should not be allowed to read or send messages in this channel
        overwrite.read_messages = False
        await self.bot.edit_channel_permissions(channel, everyone, overwrite)

        # @support : they should be allowed to read and send messages to this channel
        overwrite.read_messages = True
        overwrite.send_messages = True
        await self.bot.edit_channel_permissions(channel, support, overwrite)
        
        # ctx.message.author : they should be allowed to read and send messages to this channel
        await self.bot.edit_channel_permissions(channel, ctx.message.author, overwrite)

        await self.bot.move_channel(channel, 0)
        await self.bot.send_message(channel, "**{}: New ticket created by {}**\n`!close closes the ticket`\n`!reopen reopens a closed ticket`".format(support.mention, ctx.message.author.mention))
        
    @commands.command(pass_context=True)
    async def close(self, ctx):
        if len(ctx.message.channel.name.split("-")) == 2:
            if ctx.message.channel.name.split("-")[0] == "open":
                newname = "closed-" + ctx.message.channel.name.split("-")[1]
                textchannels = -1
                for channel in ctx.message.server.channels:
                    if channel.type == discord.ChannelType.text:
                        textchannels += 1
                await self.bot.edit_channel(channel=ctx.message.channel, name=newname)    
                await self.bot.send_message(ctx.message.channel, "**Ticket has been closed by {}. Use `!reopen` to reopen it.**".format(ctx.message.author.mention))
                return await self.bot.move_channel(ctx.message.channel, textchannels)

    @commands.command(pass_context=True)
    async def reopen(self, ctx):
        if len(ctx.message.channel.name.split("-")) == 2:
            if ctx.message.channel.name.split("-")[0] == "closed":
                for role in ctx.message.server.roles:
                    if role.name == "@everyone":
                        everyone =  role
                    elif role.name == "support":
                        support = role
                if support == "":
                    return await self.bot.send_message(ctx.message.channel, "This command is not set up properly, please contact a developer.")
                
                newname = "open-" + ctx.message.channel.name.split("-")[1]
                await self.bot.edit_channel(channel=ctx.message.channel, name=newname)    
                await self.bot.send_message(ctx.message.channel, "**{}: Ticket reopened by {}**\n`!close closes the ticket`\n`!reopen reopens a closed ticket`".format(support.mention, ctx.message.author.mention))
                return await self.bot.move_channel(ctx.message.channel, 0)
            
def setup(bot):
    bot.add_cog(Ticket(bot))
