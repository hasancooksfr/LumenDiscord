import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# ----- PREFIX COMMANDS FROM HERE -----
@bot.command(name="ping")
async def ping(ctx):
    await ctx.reply("Pong! Working!")

@bot.command(name="hello")
async def hello(ctx, member: discord.Member = None):
    if member != None:
        try:
            await member.send(f"<@{ctx.author.id}> asked me to say you **Hello!**")
            await ctx.reply(f"DM sent to user.")
        except discord.Forbidden:
            await ctx.reply("Unable to DM that user :(")
    else:
        embed = discord.Embed(
            title="Invalid Command Usage!",
            description="Usage:\n!hello [@user]",
            color=0xFF0000
        )
        await ctx.reply(embed=embed)

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason: str = "No reason provided"):
    if member is None:
        embed = discord.Embed(
            title="Invalid Command Usage!",
            description="Usage:\n!ban [@user] (reason)",
            color=0xFF0000
        )
        await ctx.reply(embed=embed)
        return

    if member == ctx.author:
        await ctx.reply("You cannot ban yourself.")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.reply("❌ You cannot ban someone with an equal or higher role.")
        return

    if member == bot.user:
        await ctx.reply("I cannot ban myself.")
        return

    if member.top_role >= ctx.guild.me.top_role:
        await ctx.reply("❌ I cannot ban someone with an equal or higher role than me.")
        return

    try:
        try:
            embed = discord.Embed(
                title="You have been BANNED!",
                description=f"You have been BANNED from {ctx.guild.name}\nAdmin: <@{ctx.author.id}>\nReason: {reason}",
                color=0xFF0000
            )
            embed.set_footer(text=ctx.guild.name)
            await member.send(embed=embed)
        except discord.Forbidden:
            pass
        reason = f"Banned by {ctx.author.id}. Reason: {reason}"
        await member.ban(reason=reason)
        await ctx.reply("User has been banned!")
    except discord.Forbidden:
        await ctx.reply("Couldn't ban that user. :(")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
@commands.bot_has_permissions(ban_members=True)
async def unban(ctx, user_id: int = None):
    if user_id is None:
        embed = discord.Embed(
            title="Invalid Command Usage!",
            description="Usage:\n!unban [user id]",
            color=0xFF0000
        )
        await ctx.reply(embed=embed)
        return

    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.reply(f"Unbanned {user.name}")

    except discord.NotFound:
        await ctx.send("User not found.")

    except discord.Forbidden:
        await ctx.send("Unable to unban.")

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
@commands.bot_has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason: str = "No reason provided."):
    if member is None:
        embed = discord.Embed(
            title="Invalid Command Usage!",
            description="Usage:\n!kick [@user] (reason)",
            color=0xFF0000
        )
        await ctx.reply(embed=embed)
        return
    
    if member == ctx.author:
        await ctx.reply("You cannot kick yourself.")
        return
    
    if member.top_role >= ctx.author.top_role:
        await ctx.reply("You cannot kick someone with an equal or higher role.")
        return

    if member == bot.user:
        await ctx.reply("I cannot kick myself.")
        return

    if member.top_role >= ctx.guild.me.top_role:
        await ctx.reply("I cannot kick someone with an equal or higher role than me.")
        return

    try:
        try:
            embed = discord.Embed(
                title="You have been KICKED!",
                description=f"You have been KICKED from {ctx.guild.name}\nAdmin: <@{ctx.author.id}>\nReason: {reason}",
                color=0xFF0000
            )
            embed.set_footer(text=ctx.guild.name)
            await member.send(embed=embed)
        except discord.Forbidden:
            pass
        reason = f"Kicked by {ctx.author.id}. Reason: {reason}"
        await member.kick(reason=reason)
        await ctx.reply("User has been kicked!")
    except discord.Forbidden:
        await ctx.reply("Couldn't kick that user. :(")

@bot.command(name="timeout", aliases=["mute", "tm"])
@commands.has_permissions(moderate_members=True)
@commands.bot_has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member = None, minutes: int = None, *, reason: str = "No reason provided"):
    if member is None or minutes is None:
        embed = discord.Embed(
            title="Invalid Command Usage!",
            description=f"Usage:\n!{ctx.invoked_with} [@user] [minutes] (reason)",
            color=0xFF0000
        )
        await ctx.reply(embed=embed)
        return

    if member == ctx.author:
        await ctx.reply("You cannot timeout yourself.")
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.reply("You cannot timeout someone with an equal or higher role than you.")
        return
    
    if member == bot.user:
        await ctx.reply("I cannot timeout myself.")
        return

    if member.top_role >= ctx.guild.me.top_role:
        await ctx.reply("I cannot timeone someone with an equal or higher role than me.")
        return

    try:
        reason = f"Timed out by {ctx.author.id}. Reason: {reason}"
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        await ctx.reply(f"{member.mention} has been timed out for {minutes} minutes.")

    except discord.Forbidden:
        await ctx.reply("Unable to timeout that user.")

@bot.command(name="untimeout")
@commands.has_permissions(moderate_members=True)
@commands.bot_has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member = None):
    if member is None:
        embed = discord.Embed(
            title="Invalid Command Usage!",
            description="Usage:\n!untimeout [@user]",
            color=0xFF0000
        )
        await ctx.reply(embed=embed)
        return

    if member.top_role >= ctx.author.top_role:
        await ctx.reply("You cannot remove timeout of someone with an equal or higher role than you.")
        return

    if member.top_role >= ctx.guild.me.top_role:
        await ctx.reply("I cannot remove timeout of someone with an equal or higher role than me.")
        return

    try:
        await member.timeout(None)
        await ctx.reply(f"Removed timeout from {member.mention}")
    
    except discord.Forbidden:
        await ctx.reply("Unable to remove timeout from that user.")



# ----- SLASH COMMANDS FROM HERE -----
@bot.tree.command(name="ping", description="Check bot latency")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message("Pong! Working!")

@bot.tree.command(name="hello", description="Send Hello to any user")
async def hello_slash(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.send(f"<@{interaction.user.id}> asked to say you **Hello!**")
        await interaction.response.send_message("DM sent!", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("Unable to send DM", ephemeral=True)
    
@bot.tree.command(name="ban", description="Ban users from this server")
@app_commands.checks.bot_has_permissions(ban_members=True)
@app_commands.checks.has_permissions(ban_members=True)
async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        await interaction.response.send_message("You cannot ban yourself.", ephemeral=True)
        return
    
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("You cannot ban someone with an equal or higher role than you.", ephemeral=True)
        return

    if member == bot.user:
        await interaction.response.send_message("I cannot ban myself.", ephemeral=True)
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("I cannot ban someone with an equal or higher role than me.", ephemeral=True)
        return
    
    try:
        try:
            embed = discord.Embed(
                title="You have been BANNED!",
                description=f"You have been BANNED from {interaction.guild.name}\nAdmin: <@{interaction.user.id}>\nReason: {reason}",
                color=0xFF0000
            )
            embed.set_footer(text=interaction.guild.name)
            await member.send(embed=embed)
        except discord.Forbidden:
            pass
        reason = f"Banned by {interaction.user.id}. Reason: {reason}"
        await member.ban(reason=reason)
        await interaction.response.send_message("User has been banned.")
    except:
        await interaction.response.send_message("Couldn't ban that user. :(")

@bot.tree.command(name="unban", description="Unban member from this server")
@app_commands.checks.bot_has_permissions(ban_members=True)
@app_commands.checks.has_permissions(ban_members=True)
async def unban_slash(interaction: discord.Interaction, userid: int):
    try:
        user = bot.fetch_user(userid)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Unbanned {user.name}")

    except discord.NotFound:
        await interaction.response.send_message("User not found.", ephemeral=True)

    except discord.Forbidden:
        await interaction.response.send_message("Unable to unban", ephemeral=True)

@bot.tree.command(name="kick", description="Kick users from this server")
@app_commands.checks.bot_has_permissions(kick_members=True)
@app_commands.checks.has_permissions(kick_members=True)
async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        await interaction.response.send_message("You cannot kick yourself!", ephemeral=True)
        return

    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("You cannot kick someone with an equal or higher role.", ephemeral=True)
        return

    if member == bot.user:
        await interaction.response.send_message("I cannot kick myself.", ephemeral=True)
        return

    
    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("I cannot kick someone with an equal or higher role than me.", ephemeral=True)
        return

    try:
        try:
            embed = discord.Embed(
                title="You have been KICKED!",
                description=f"You have been KICKED from {ctx.guild.name}\nAdmin: <@{ctx.author.id}>\nReason: {reason}",
                color=0xFF0000
            )
            embed.set_footer(text=ctx.guild.name)
            await member.send(embed=embed)
        except discord.Forbidden:
            pass
        reason = f"Kicked by {interaction.user.id}. Reason: {reason}"
        await member.kick(reason=reason)
        await interaction.response.send_message("User has been kicked!")
    except discord.Forbidden:
        await interaction.response.send_message("Couldn't ban that user :(")

@bot.tree.command(name="timeout", description="Timeout member from this server")
@app_commands.checks.bot_has_permissions(moderate_members=True)
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout_slash(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str) = "No reason provided":
    if interaction.user == member:
        await interaction.response.send_message("You cannot timeout youself.", ephemeral=True)
        return

    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("You cannot timeout someone with an equal or higher role than you.", ephemeral=True)
        return

    if member == bot.user:
        await interaction.response.send_message("I cannot timeout myself.", ephemeral=True)
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("I cannot timeout someone with an equal or higher role than me.", ephemeral=True)3
        return

    try:
        reason = f"Timed out by {interaction.user.id}. Reason: {reason}"
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        await interaction.response.send_message(f"Timed out {member.mention} for {minutes} minutes.")

    except discord.Forbidden:
        await interaction.response.send_message("Could not timeout that user.", ephemeral=True)

@bot.tree.command(name="untimeout", description="Remove timeout from member")
@app_commands.checks.has_permissions(moderate_members=True)
@app_commands.checks.bot_has_permissions(moderate_members=True)
async def untimeout_slash(interaction: discord.Interaction, member: disord.Member):
    
    if member.top_role >= interaction.user.top_role:
        await interaction.response.send_message("You cannot remove timeout of someone with an equal or higher role than you.", ephemeral=True)
        return

    if member.top_role >= interaction.guild.me.top_role:
        await interaction.response.send_message("I cannot remove timeout of someone with an equal or higher role than me.", ephemeral=True)
        return

    try:
        await member.timeout(None)
        await interaction.response.send_message(f"Timeout removed from {member.mention}")
    
    except discord.Forbidden:
        await interaction.response.send_message("Could not remove timeout of that user.", ephemeral=True)

# ----- Error Handling -----
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("❌ You don't have enough permissions to use this command.")
    
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.reply("❌ I don't have enough permissions.")

    elif isinstance(error, commands.MemberNotFound):
        await ctx.reply("❌ Member not found.")

    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply("❌ Command not found.")

    else:
        print(error)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("❌ You don't have enough permissions to use this command.", ephemeral=True)
    
    elif isinstance(error, app_commands.BotMissingPermissions):
        await interaction.response.send_message("❌ I don't have enough permissions.", ephemeral=True)
    
    else:
        print(error)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="theysaykings 👀"
        )
    )
    print(f"Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash commands")
    except Exception as e:
        print(e)

bot.run(TOKEN)