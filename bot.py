"""The main bot."""
import logging

import discord
from discord.ext import commands

from main import config, helpcmd, models


logging.basicConfig(level=logging.INFO)


def get_prefix(bot: commands.Bot, message: discord.Message) -> str:
    """Get the prefix for a server (or DMs)."""
    if not message.guild:
        return config.DEFAULT_PREFIX
    return models.Guild.get_by_guild(message.guild).prefix


bot = commands.Bot(command_prefix=get_prefix, help_command=helpcmd.Help())
bot.load_extension('cogs')

bot.run(config.TOKEN)
