"""Moderation-related commands."""
from datetime import datetime, timedelta

import discord
from discord.ext import commands


class Moderation(commands.Cog):
    """Moderation-related commands."""

    def __init__(self, bot: commands.Bot):
        """Save a reference to the bot."""
        self.bot = bot

    @commands.command(
        brief='Delete up to a message.', name='clear-until', aliases=['clear']
    )
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    async def clear_until(
            self, ctx: commands.Context, *, message: discord.Message):
        """Delete all messages up to (not including) a specified message.

        Example: `{{pre}}clear-until 12345678912345`
        """
        if message.created_at + timedelta(days=14) < datetime.now():
            await ctx.send('Cannot delete messages over 14 days old.')
            return
        messages = await ctx.channel.purge(after=message, limit=1000)
        await ctx.send(f'Deleted {len(messages)} messages.', delete_after=2)
