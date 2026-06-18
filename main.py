import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import random
import time

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

# ----- PREFIX COMMANDS FROM HERE -----
# -- UTILITY --
@bot.command(name="help")
async def help(ctx, command: str = None):
    if command is None:

        embed = discord.Embed(
            title="🌟 Lumen Discord",
            description="Multi-functional moderation and utility bot\nUse `!help <command>` for more information",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=bot.user.display_avatar.url)

        embed.add_field(
            name="🛡️ Moderation",
            value="""
`!ban`
`!unban`
`!kick`
`!timeout`
`!untimeout`
`!clear`
`!lock`
`!unlock`
`!nickname`
`!role`
            """,
            inline=False
        )

        embed.add_field(
            name="⚙️ Utility",
            value="""
`!ping`
`!userinfo`
`!serverinfo`
`!hello`
            """,
            inline=False
        )

        embed.add_field(
            name="🎮 Fun",
            value="""
`!coinflip`
            """
        )

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        return await ctx.reply(embed=embed)
    
    command = command.lower()

    help_data = {
        "ban": {
            "description": "Ban a member from the server.",
            "usage": "!ban [@member] <reason>",
            "aliases": []
        },
        "unban": {
            "description": "Unban a member from the server.",
            "usage": "!unban [userid]",
            "aliases": []
        },
        "kick": {
            "description": "Kick a member from the server.",
            "usage": "!kick [@member] <reason>",
            "aliases": []
        },
        "timeout": {
            "description": "Timeout a member from the server.",
            "usage": "!timeout [@member] <minutes> <reason>",
            "aliases": ["mute", "tm"]
        },
        "untimeout": {
            "description": "Remove timeout from a member.",
            "usage": "!untimeout [@member]",
            "aliases": ["untimeout"]
        },
        "clear": {
            "description": "Delete number of messages of a channel. (Default: 10 messages)",
            "usage": "!clear <amount> <#channel>",
            "aliases": ["purge"]
        },
        "lock": {
            "description": "Prevents members from messaging in a channel.",
            "usage": "!lock <#channel>",
            "aliases": []
        },
        "unlock": {
            "description": "Enables messaging for members in a channel.",
            "usage": "!unlock <#channel>",
            "aliases": []
        },
        "nickname": {
            "description": "Change/Remove someone's nickname in this server.",
            "usage": "!nickname [@member] <nickname>",
            "aliases": ["nick"]
        },
        "ping": {
            "description": "Pings the bot.",
            "usage": "!ping",
            "aliases": []
        },
        "userinfo": {
            "description": "Displays brief information about an user of this server.",
            "usage": "!userinfo [@member]",
            "aliases": ["ui", "whois"]
        },
        "serverinfo": {
            "description": "Displays brief information about the server.",
            "usage": "!serverinfo",
            "aliases": ["si"]
        },
        "hello": {
            "description": "Greet someone by the help of the bot. Bot sends hello DM to a member.",
            "usage": "!hello [@member]",
            "aliases": []
        },
        "role":{
            "description": "Give/Remove role from a member of the server.",
            "usage": "!role [@member] [@role]",
            "aliases": ["giverole", "ar"]
        },
        "coinflip": {
            "description": "Flip a coin!",
            "usage": "!coinflip <guess: Heads or Tails>",
            "aliases": ["cf"]
        }
    }

    if command not in help_data:
        return await ctx.reply(f"❌ No help found for `{command}`")

    data = help_data[command]
    
    embed = discord.Embed(
        title=f"📖 Command: {command}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(
        name="Description",
        value=data["description"],
        inline=False
    )
    embed.add_field(
        name="Usage",
        value=data["usage"],
        inline=False
    )
    embed.add_field(
        name="Aliases",
        value=", ".join(data["aliases"]) or "None",
        inline=False
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )

    await ctx.reply(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    await ctx.reply(f"Pong! Latency :`{round(bot.latency * 1000)}ms`")

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

@bot.command(name="userinfo", aliases=["ui", "whois"])
async def userinfo(ctx, member: discord.Member = None):
    member = member or ctx.author

    embed = discord.Embed(
        title="👤 User Information",
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)

    embed.add_field(
        name="Username",
        value=f"{member}",
        inline=True
    )
    embed.add_field(
        name="User ID",
        value=member.id,
        inline=True
    )
    embed.add_field(
        name="Nickname",
        value=member.nick or "None",
        inline=True
    )
    embed.add_field(
        name="Account Created",
        value=f"<t:{int(member.created_at.timestamp())}:F>",
        inline=True
    )
    embed.add_field(
        name="Joined Server",
        value=f"<t:{int(member.joined_at.timestamp())}:F>",
        inline=False
    )
    embed.add_field(
        name="Top Role",
        value=member.top_role.mention,
        inline=True
    )
    embed.add_field(
        name="Roles",
        value=len(member.roles) - 1,
        inline=True
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )

    await ctx.reply(embed=embed)

@bot.command(name="serverinfo", aliases=["si"])
async def serverinfo(ctx):

    guild = ctx.guild

    embed = discord.Embed(
        title=f"🏠 {guild.name}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(
        name="Owner",
        value=guild.owner.mention,
        inline=True
    )
    embed.add_field(
        name="Server ID",
        value=guild.id,
        inline=True
    )
    embed.add_field(
        name="Members",
        value=guild.member_count,
        inline=True
    )
    embed.add_field(
        name="Channels",
        value=len(guild.channels),
        inline=True 
    )
    embed.add_field(
        name="Roles",
        value=len(guild.roles),
        inline=True
    )
    embed.add_field(
        name="Boost Level",
        value=guild.premium_tier,
        inline=True
    )
    embed.add_field(
        name="Created",
        value=f"<t:{int(guild.created_at.timestamp())}:F>",
        inline=False
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )

    await ctx.reply(embed=embed)

# -- MODERATION --

@bot.command(name="role", aliases=["giverole", "ar"])
@commands.has_permissions(manage_roles=True)
@commands.bot_has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member = None, *, role: discord.Role = None):
    if member is None or role is None:
        embed=discord.Embed(
            title="Invalid Command Usage!",
            description=f"Usage:\n!{ctx.invoked_with} [@user] [@role]",
            color=0xFF0000
        )
        return await ctx.reply(embed=embed)

    if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot manage roles equal to or higher than your highest role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if role >= ctx.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot manage roles equal to or higher than my highest role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.author.top_role and member != ctx.author:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot manage members with roles equal to or higher than your highest role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot manage members with roles equal to or higher than my highest role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    try:
        if role in member.roles:
            await member.remove_roles(role, reason=f"Requested by {ctx.author}")
            embed = discord.Embed(
                title="Role Removed",
                description=f"Removed {role.mention} from {member.mention}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )

        else:
            await member.add_roles(role, reason=f"Requested by {ctx.author}")
            embed = discord.Embed(
                title="Role Added",
                description=f"Added {role.mention} to {member.mention}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )

        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)

    except discord.Forbidden:
        embed=discord.Embed(
            title="❌ Unexpected Error",
            description="Couldn't manage that role",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)

@bot.command(name="clear", aliases=["purge"])
@commands.has_permissions(manage_messages=True)
@commands.bot_has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10, channel: discord.TextChannel = None):
    if amount < 1 or amount > 100:
        await ctx.reply("Please enter a valid amount. (> 1 and < 100)")
        return

    channel = channel or ctx.channel
    deleted = await channel.purge(limit=amount)
    embed=discord.Embed(
        title="Cleared ✅",
        description=f"Deleted {len(deleted)} messages from {channel.mention}",
        color=discord.Color.green()
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )
    await ctx.send(embed=embed, delete_after=10)

@bot.command(name="lock")
@commands.has_permissions(manage_channels=True)
@commands.bot_has_permissions(manage_channels=True)
async def lock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False

    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed= discord.Embed(
        title="Locked 🔒",
        description=f"Locked {channel.mention}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )
    await ctx.reply(embed=embed)

@bot.command(name="unlock")
@commands.has_permissions(manage_channels=True)
@commands.bot_has_permissions(manage_channels=True)
async def unlock(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel

    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = True

    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed=discord.Embed(
        title="Unlocked 🔓",
        description=f"Unlocked {channel.mention}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )

    await ctx.reply(embed=embed)

@bot.command(name="nickname", aliases=["nick"])
@commands.has_permissions(manage_nicknames=True)
@commands.bot_has_permissions(manage_nicknames=True)
async def nickname(ctx, member: discord.Member = None, *, nickname: str = None):
    if member is None:
        embed = discord.Embed(
            title="Invalid Command Usage!",
            description=f"Usage:\n!{ctx.invoked_with} [@user] (nickname)",
            color=0xFF0000
        )
        await ctx.reply(embed=embed)
        return

    if member != ctx.author and member.top_role >= ctx.author.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot nickname someone with an equal or higher role than you.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot nickname someone with an equal or higher role than me.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    await member.edit(nick=nickname, reason=f"Changed by {ctx.author.id}")
    embed=discord.Embed(
        title="✅ Nickname Changed",
        description=f"Changed {member.mention}'s nickname to **{nickname}**",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Requested by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )

    await ctx.send(embed=embed)

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
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="You cannot ban yourself!",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.author.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot ban someone with an equal or higher role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member == bot.user:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="I cannot ban myself.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot ban someone with an equal or higher role than me.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    try:
        try:
            embed = discord.Embed(
                title="You have been BANNED!",
                description=f"You have been BANNED from {ctx.guild.name}\nModerator: <@{ctx.author.id}>\nReason: {reason}",
                color=0xFF0000
            )
            embed.set_footer(text=ctx.guild.name)
            await member.send(embed=embed)
            dm = True
        except discord.Forbidden:
            pass
            dm = False
        nreason = f"Banned by {ctx.author.id}. Reason: {reason}"
        await member.ban(reason=nreason)
        embed=discord.Embed(
            title="✅ User Banned",
            description=f"Banned User: `{member}`\nModerator: {ctx.author.mention}\nDM User: {"✅" if dm else "❌"}\nReason: {reason}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )
        await ctx.reply(embed=embed)
    except discord.Forbidden:
        embed=discord.Embed(
            title="❌ Unexpected Error",
            description="Couldn't ban that user :(",
            color=discord.Color.red()
        )
        await ctx.reply(embed=embed)

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
        embed=discord.Embed(
            title="✅ User Unbanned",
            description=f"{user} has been unbanned successfully.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)

    except discord.NotFound:
        await ctx.reply(embed=discord.Embed(title="❌ Member not found", description="Please enter a valid userid.", color=discord.Color.red()))

    except discord.Forbidden:
        await ctx.reply(embed=discord.Embed(title="❌ Unexpected Error", description="Unable to unban due to some error.", color=discord.Color.red()))

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
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="You cannot kick yourself.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )
    
    if member.top_role >= ctx.author.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot kick someone with an equal or higher role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member == bot.user:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="I cannot kick myself.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot kick someone with an equal or higher role than me.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    try:
        try:
            embed = discord.Embed(
                title="You have been KICKED!",
                description=f"You have been KICKED from {ctx.guild.name}\nModerator: <@{ctx.author.id}>\nReason: {reason}",
                color=0xFF0000
            )
            embed.set_footer(text=ctx.guild.name)
            await member.send(embed=embed)
            dm = True
        except discord.Forbidden:
            pass
            dm = False
        nreason = f"Kicked by {ctx.author.id}. Reason: {reason}"
        await member.kick(reason=nreason)
        embed= discord.Embed(
            title="✅ User Kicked",
            description=f"Kicked User: `{member}`\nModerator: {ctx.author.mention}\nDM User: {"✅" if dm else "❌"}\nReason: {reason}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )
        await ctx.reply(embed=embed)

    except discord.Forbidden:
        await ctx.reply(embed=discord.Embed(title="❌ Unexpected Error", description="Unable to kick due to some error.", color=discord.Color.red()))

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
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="You cannot timeout yourself.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.author.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot timeout someone with an equal or higher role than your highest role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )
    
    if member == bot.user:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="I cannot timeout myself.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot timeout someone with an equal or higher role than me.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    try:
        nreason = f"Timed out by {ctx.author.id}. Reason: {reason}"
        await member.timeout(timedelta(minutes=minutes), reason=nreason)
        embed= discord.Embed(
            title="✅ Timeout Successful",
            description=f"Timed out User: {member.mention}\nModerator: {ctx.author.mention}\nDuration: {minutes} minutes\nReason: {reason}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )

        await ctx.reply(embed=embed)

    except discord.Forbidden:
        await ctx.reply(
            embed=discord.Embed(title="❌ Unexpected Error", description="Unable to timeout due to some error.", color=discord.Color.red())
        )

@bot.command(name="untimeout", aliases=["unmute"])
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
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot remove timeout of someone with an equal or higher role than your highest role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    if member.top_role >= ctx.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot remove timeout of someone with an equal or higher role than my highest role.",
            color=discord.Color.red()
        )
        return await ctx.reply(
            embed=embed
        )

    try:
        await member.timeout(None)
        embed= discord.Embed(
            title="✅ Timeout Removed",
            description=f"User: {member.mention}\nModerator: {ctx.author.mention}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {ctx.author}",
            icon_url=ctx.author.display_avatar.url
        )
        await ctx.reply(embed=embed)
    
    except discord.Forbidden:
        await ctx.reply(
            embed=discord.Embed(title="❌ Unexpected Error", description="Unable to remove timeout due to some error.", color=discord.Color.red())
        )

# -- FUN --

@bot.command(name="coinflip", aliases=["cf"])
async def coinflip(ctx, guess: str = "heads"):
    guess = guess.capitalize()

    if guess not in ["Heads", "Tails"]:
        return await ctx.reply(
            "Invalid Choice\nChoose `Heads` or `Tails` only."
        )

    result = random.choice(["Heads", "Tails"])
    time.sleep(1)

    won = guess == result


    embed=discord.Embed(
        title="🪙 Coin Flip",
        description=(
            f"Your Guess: **{guess}**\n"
            f"Result: **{result}**\n\n"
            f"{"🎉 You won!" if won else '❌ You lost!'}"
        ),
        color=discord.Color.green() if won else discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Flipped by {ctx.author}",
        icon_url=ctx.author.display_avatar.url
    )

    await ctx.reply(embed=embed)


# ----- SLASH COMMANDS FROM HERE -----

# -- UTILITIES --

@bot.tree.command(name="help", description="Displays commands of Lumen")
async def help_slash(interaction: discord.Interaction, command: str = None):
    if command is None:
        embed = discord.Embed(
            title="🌟 Lumen Discord",
            description="Multi-functional moderation and utility bot\nUse `/help <command>` for more information",
            color=discord.Color.gold(),
            timestamp=discord.utils.utcnow()
        )

        embed.set_thumbnail(url=bot.user.display_avatar.url)

        embed.add_field(
            name="🛡️ Moderation",
            value="""
`/ban`
`/unban`
`/kick`
`/timeout`
`/untimeout`
`/clear`
`/lock`
`/unlock`
`/nickname`
`/role`
            """,
            inline=False
        )

        embed.add_field(
            name="⚙️ Utility",
            value="""
`/ping`
`/userinfo`
`/serverinfo`
`/hello`
            """,
            inline=False
        )

        embed.add_field(
            name="🎮 Fun",
            value="""
`/coinflip`
            """,
            inline=False
        )

        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )

        return await interaction.response.send_message(embed=embed)
    
    command = command.lower()

    help_data = {
        "ban": {
            "description": "Ban a member from the server.",
            "usage": "/ban [@member] <reason>"
        },
        "unban": {
            "description": "Unban a member from the server.",
            "usage": "/unban [userid]"
        },
        "kick": {
            "description": "Kick a member from the server.",
            "usage": "/kick [@member] <reason>"
        },
        "timeout": {
            "description": "Timeout a member from the server.",
            "usage": "/timeout [@member] <minutes> <reason>"
        },
        "untimeout": {
            "description": "Remove timeout from a member.",
            "usage": "/untimeout [@member]"
        },
        "clear": {
            "description": "Delete number of messages of a channel. (Default: 10 messages)",
            "usage": "/clear <amount> <#channel>"
        },
        "lock": {
            "description": "Prevents members from messaging in a channel.",
            "usage": "/lock <#channel>"
        },
        "unlock": {
            "description": "Enables messaging for members in a channel.",
            "usage": "/unlock <#channel>"
        },
        "nickname": {
            "description": "Change/Remove someone's nickname in this server.",
            "usage": "/nickname [@member] <nickname>"
        },
        "ping": {
            "description": "Pings the bot.",
            "usage": "/ping"
        },
        "userinfo": {
            "description": "Displays brief information about an user of this server.",
            "usage": "/userinfo [@member]"
        },
        "serverinfo": {
            "description": "Displays brief information about the server.",
            "usage": "/serverinfo"
        },
        "hello": {
            "description": "Greet someone by the help of the bot. Bot sends hello DM to a member.",
            "usage": "/hello [@member]"
        },
        "role":{
            "description": "Give/Remove role from a member of the server.",
            "usage": "/role [@member] [@role]"
        },
        "coinflip": {
            "description": "Flip a coin!",
            "usage": "/coinflip <guess: Heads or Tails>"
        }
    }

    if command not in help_data:
        return await interaction.response.send_message(embed=discord.Embed(description=f"❌ No help found for `{command}`"), ephemeral=True)

    data = help_data[command]
    
    embed = discord.Embed(
        title=f"📖 Command: {command}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(
        name="Description",
        value=data["description"],
        inline=False
    )
    embed.add_field(
        name="Usage",
        value=data["usage"],
        inline=False
    )
    embed.set_footer(
        text=f"Requested by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Check bot latency")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong! Latency :`{round(bot.latency * 1000)}ms`")

@bot.tree.command(name="hello", description="Send Hello to any user")
async def hello_slash(interaction: discord.Interaction, member: discord.Member):
    try:
        await member.send(f"<@{interaction.user.id}> asked to say you **Hello!**")
        await interaction.response.send_message("DM sent!")
    except discord.Forbidden:
        await interaction.response.send_message("Unable to send DM", ephemeral=True)

@bot.tree.command(name="userinfo", description="Displays information about an user")
async def userinfo_slash(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user

    embed = discord.Embed(
        title="👤 User Information",
        color=discord.Color.blurple(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_thumbnail(url=member.display_avatar.url)

    embed.add_field(
        name="Username",
        value=f'{member}',
        inline=True
    )
    embed.add_field(
        name="User ID",
        value=member.id,
        inline=True
    )
    embed.add_field(
        name="Nickname",
        value=member.nick or "None",
        inline=True
    )
    embed.add_field(
        name="Account Created",
        value=f"<t:{int(member.created_at.timestamp())}:F>",
        inline=True
    )
    embed.add_field(
        name="Joined Server",
        value=f"<t:{int(member.joined_at.timestamp())}:F>",
        inline=False
    )
    embed.add_field(
        name="Top Role",
        value=member.top_role,
        inline=True
    )
    embed.add_field(
        name="Roles",
        value=len(member.roles) - 1,
        inline=True
    )
    embed.set_footer(
        text=f"Requested by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="Displays information about server")
async def serverinfo_slash(interaction: discord.Interaction):
    guild = interaction.guild

    embed = discord.Embed(
        title=f"🏠 {guild.name}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)

    embed.add_field(
        name="Owner",
        value=guild.owner.mention,
        inline=True
    )
    embed.add_field(
        name="Server ID",
        value=guild.id,
        inline=True
    )
    embed.add_field(
        name="Members",
        value=guild.member_count,
        inline=True
    )
    embed.add_field(
        name="Channels",
        value=len(guild.channels),
        inline=True
    )
    embed.add_field(
        name="Roles",
        value=len(guild.roles),
        inline=True
    )
    embed.add_field(
        name="Boost Level",
        value=guild.premium_tier,
        inline=True
    )
    embed.add_field(
        name="Created at",
        value=f"<t:{int(guild.created_at.timestamp())}:F>",
        inline=False
    )
    embed.set_footer(
        text=f"Requested by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )

    await interaction.response.send_message(embed=embed)

# -- MODERATION --

@bot.tree.command(name="role", description="Gives or Removes role from a member of the server")
@app_commands.checks.has_permissions(manage_roles=True)
@app_commands.checks.bot_has_permissions(manage_roles=True)
async def role_slash(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
    if role >= interaction.user.top_role and interaction.user != interaction.guild.owner:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot manage roles equal to or higher than your highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if role >= interaction.user.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot manage roles equal to or higher than my highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member.top_role >= interaction.user.top_role and member != interaction.user:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot manage roles of someone with an equal or higher role than your highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member.top_role >= interaction.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot manage roles of someone with an equal or higher role than my highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
    try:
        if role in members.roles:
            await member.remove_roles(role, reason=f"Requested by {interaction.user}")
            embed = discord.Embed(
                title="Role Removed",
                description=f"Removed {role.mention} from {member.mention}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )

        else:
            await member.add_roles(role, reason=f"Requested by {interaction.user}")
            embed= discord.Embed(
                title="Role Added",
                description=f"Added {role.mention} to {member.mention}",
                color=discord.Color.green(),
                timestamp=discord.utils.utcnow()
            )

        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.send_message(embed=embed)
    
    except discord.Forbidden:
        embed=discord.Embed(
            title="❌ Unexpected Error",
            description="Couldn't manage that role",
            color=discord.Color.red()
        )
        await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )


@bot.tree.command(name="clear", description="Clears messages from a channel")
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.checks.bot_has_permissions(manage_messages=True)
async def clear_slash(interaction: discord.Interaction, amount: int = 10, channel: discord.TextChannel = None):
    if amount < 1 or amount > 100:
        await interaction.response.send_message("Please enter a valid amount. (> 1 and < 100)", ephemeral=True)
        return

    channel = channel or interaction.channel
    deleted = await channel.purge(limit=amount)
    embed=discord.Embed(
        title="Cleared ✅",
        description=f"Deleted {len(deleted)} messages from {channel.mention}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Requested by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="lock", description="Prevents members to send messages in a channel")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.checks.bot_has_permissions(manage_channels=True)
async def lock_slash(interaction: discord.Interaction, channel: discord.TextChannel = None):
    channel = channel or interaction.channel

    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False

    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed=discord.Embed(
        name="Locked 🔒",
        description=f"Locked {channel.mention}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Requested by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="unlock", description="Allows members to send messages in a channel")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.checks.bot_has_permissions(manage_channels=True)
async def unlock_slash(interaction: discord.Interaction, channel:discord.TextChannel = None):
    channel = channel or interaction.channel

    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True

    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    embed=discord.Embed(
        title="Unlocked 🔓",
        description=f"Unlocked {channel.mention}",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Requested by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="nickname", description="Change or Clear someone's nickname")
@app_commands.checks.has_permissions(manage_nicknames=True)
@app_commands.checks.bot_has_permissions(manage_nicknames=True)
async def nickname_slash(interaction: discord.Interaction, member: discord.Member, nickname: str = None):
    if member != interaction.user and member.top_role >= interaction.user.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot nickname someone with an equal or higher role than your highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member.top_role >= interaction.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot nickname someone with an equal or higher role than my highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    await member.edit(nick=nickname, reason=f"Changed by {interaction.user.id}")
    embed=discord.Embed(
        title="✅ Nickname Changed",
        description=f"Changed {member.mention}'s nickname to **{nickname}**",
        color=discord.Color.green(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Requested by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ban", description="Ban users from this server")
@app_commands.checks.bot_has_permissions(ban_members=True)
@app_commands.checks.has_permissions(ban_members=True)
async def ban_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="You cannot ban youself",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
    
    if member.top_role >= interaction.user.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot ban someone with an equal or higher role than you.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member == bot.user:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="I cannot ban myself",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member.top_role >= interaction.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot ban someone with an equal or higher role than me.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )
    
    try:
        try:
            embed = discord.Embed(
                title="You have been BANNED!",
                description=f"You have been BANNED from {interaction.guild.name}\nAdmin: <@{interaction.user.id}>\nReason: {reason}",
                color=0xFF0000
            )
            embed.set_footer(text=interaction.guild.name)
            await member.send(embed=embed)
            dm=True
        except discord.Forbidden:
            pass
            dm=False
        nreason = f"Banned by {interaction.user.id}. Reason: {reason}"
        await member.ban(reason=nreason)
        embed=discord.Embed(
            title="✅ User Banned",
            description=f"Banned User: `{member}`\nModerator: {interaction.user.mention}\nDM User: {"✅" if dm else "❌"}\nReason: {reason}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed)
    except:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unexpected Error",
                description="Couldn't ban that user :(",
                color=discord.Color.red()
            ),
            ephemeral=True
        )

@bot.tree.command(name="unban", description="Unban member from this server")
@app_commands.checks.bot_has_permissions(ban_members=True)
@app_commands.checks.has_permissions(ban_members=True)
async def unban_slash(interaction: discord.Interaction, userid: int):
    try:
        user = bot.fetch_user(userid)
        await interaction.guild.unban(user)
        embed= discord.Embed(
            title="✅ User Unbanned",
            description=f"{user} has been unbanned successfully.",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )

        await interaction.response.send_message(embed=embed)

    except discord.NotFound:
        await interaction.response.send_message(embed=discord.Embed(title="❌ Member not found", description="Please enter a valid userid", color=discord.Color.red()), ephemeral=True)

    except discord.Forbidden:
        await interaction.response.send_message(embed=discord.Embed(title="❌ Unexpected Error", description="Unable to unban due to some error.", color=discord.Color.red()), ephemeral=True)

@bot.tree.command(name="kick", description="Kick users from this server")
@app_commands.checks.bot_has_permissions(kick_members=True)
@app_commands.checks.has_permissions(kick_members=True)
async def kick_slash(interaction: discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
    if member == interaction.user:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="You cannot kick yourself",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member.top_role >= interaction.user.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot kick someone with an equal or higher role than your highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member == bot.user:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="I cannot kick myself.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    
    if member.top_role >= interaction.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot kick someone with an equal or higher role than me.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    try:
        try:
            embed = discord.Embed(
                title="You have been KICKED!",
                description=f"You have been KICKED from {ctx.guild.name}\nAdmin: <@{ctx.author.id}>\nReason: {reason}",
                color=0xFF0000
            )
            embed.set_footer(text=ctx.guild.name)
            await member.send(embed=embed)
            dm=True
        except discord.Forbidden:
            pass
            dm=False
        nreason = f"Kicked by {interaction.user.id}. Reason: {reason}"
        await member.kick(reason=nreason)
        embed=discord.Embed(
            title="✅ User Kicked",
            description=f"Kicked User: `{member}`\nModeration: {interaction.user.mention}\nDM User: {"✅" if dm else "❌"}\nReason: {reason}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed)
    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unexpected Error",
                description="Couldn't kick due to some error.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )

@bot.tree.command(name="timeout", description="Timeout member from this server")
@app_commands.checks.bot_has_permissions(moderate_members=True)
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout_slash(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "No reason provided"):
    if interaction.user == member:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="You cannot timeout yourself.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member.top_role >= interaction.user.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot timeout someone with an equal or higher role than your highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member == bot.user:
        embed=discord.Embed(
            title="❌ Invalid Arguments",
            description="I cannot timeout myself.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member.top_role >= interaction.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot timeout someone with an equal or higher role than me.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    try:
        nreason = f"Timed out by {interaction.user.id}. Reason: {reason}"
        await member.timeout(timedelta(minutes=minutes), reason=nreason)
        embed=discord.Embed(
            title="✅ Timeout Successful",
            description=f"Timed out User: {member.mention}\nModerator: {interaction.user}\nDuration: {minutes} minutes\nReason: {reason}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed)

    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unexpected Error",
                description="Couldn't timeout due to some error",
                color=discord.Color.red()
            ),
            ephemeral=True
        )

@bot.tree.command(name="untimeout", description="Remove timeout from member")
@app_commands.checks.has_permissions(moderate_members=True)
@app_commands.checks.bot_has_permissions(moderate_members=True)
async def untimeout_slash(interaction: discord.Interaction, member: discord.Member):
    
    if member.top_role >= interaction.user.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="You cannot remove timeout of someone with an equal or higher role than your highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    if member.top_role >= interaction.guild.me.top_role:
        embed=discord.Embed(
            title="❌ Missing Permissions",
            description="I cannot remove timeout of someone with an equal or higher role than my highest role.",
            color=discord.Color.red()
        )
        return await interaction.response.send_message(
            embed=embed,
            ephemeral=True
        )

    try:
        await member.timeout(None)
        embed=discord.Embed(
            title="✅ Timeout Removed",
            description=f"User: {member.mention}\nModerator: {interaction.user}",
            color=discord.Color.green(),
            timestamp=discord.utils.utcnow()
        )
        embed.set_footer(
            text=f"Requested by {interaction.user}",
            icon_url=interaction.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed)
    
    except discord.Forbidden:
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Unexpected Error",
                description="Couldn't remove timeout fue to some reason.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )

# -- FUN --

@bot.tree.command(name="coinflip", description="Flip a coin")
async def coinflip_slash(interaction: discord.Interaction, guess: str = "Heads"):
    guess = guess.capitalize()

    if guess not in ["Heads", "Tails"]:
        return await interaction.response.send_message(
            "Invalid Choice!\nChoose `Heads` or `Tails` only.",
            ephemeral=True
        )

    result = random.choice(
        ["Heads", "Tails"]
    )

    won = guess == result

    embed= discord.Embed(
        title="🪙 Coin Flip",
        description=(
            f"Your Guess: **{guess}**\n"
            f"Result: **{result}**\n\n"
            f"{"🎉 You won!" if won else '❌ You lost!'}"
        ),
        color=discord.Color.green() if won else discord.Color.red(),
        timestamp=discord.utils.utcnow()
    )
    embed.set_footer(
        text=f"Flipped by {interaction.user}",
        icon_url=interaction.user.display_avatar.url
    )
    await interaction.response.send(embed=embed)
    

# ----- Error Handling -----
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        perms = ", ".join(
            f"`{perm}`"
            for perm in error.missing_permissions
        )
        await ctx.reply(
            embed=discord.Embed(
                title="❌ Missing Permissions",
                description=f"You need {perms} permission(s) to use this command.",
                color=discord.Color.red()
            )
        )
    
    elif isinstance(error, commands.BotMissingPermissions):
        perms = ", ".join(
            f"`{perm}`"
            for perm in error.missing_permissions
        )
        await ctx.reply(
            embed=discord.Embed(
                title="❌ Missing Permissions",
                description=f"I need {perms} permission(s) to use this command.",
                color=discord.Color.red()
            )
        )

    elif isinstance(error, commands.MemberNotFound):
        await ctx.reply("❌ Member not found.")

    elif isinstance(error, commands.CommandNotFound):
        await ctx.reply("❌ Command not found.")

    else:
        print(error)

@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.MissingPermissions):
        perms = ", ".join(
            f"`{perm}`"
            for perm in error.missing_permissions
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Missing Permissions",
                description=f"You need {perms} permission(s) to use this command.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
    
    elif isinstance(error, app_commands.BotMissingPermissions):
        perms = ", ".join(
            f"`{perm}`"
            for perm in error.missing_permissions
        )
        await interaction.response.send_message(
            embed=discord.Embed(
                title="❌ Missing Permissions",
                description=f"You need {perms} permission(s) to use this command.",
                color=discord.Color.red()
            ),
            ephemeral=True
        )
    
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