"""Load the cogs."""
from cogs.meta import Meta
from cogs.moderation import Moderation

import discord


COGS = [Moderation, Meta]


def setup(bot: discord.Client):
    """Load the cogs and perform other setup tasks."""
    for cog in COGS:
        cog = cog(bot)
        bot.add_cog(cog)
