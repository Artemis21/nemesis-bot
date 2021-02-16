"""Discord.py command checks."""
from discord.ext import commands

from . import models


def requires_guild() -> commands.check:
    """Create a check that ensures the command is run in a server.

    This is different from commands.guild_only because it also adds an
    instance of models.Guild to the context object.
    """

    def requires_guild_check(ctx: commands.Context) -> bool:
        """Check that a command is run in a server."""
        if not ctx.guild:
            raise commands.NoPrivateMessage(
                'This command may only be used in a server.'
            )
        ctx.guild_model = models.Guild.get_by_guild(ctx.guild)
        return True

    return commands.check(requires_guild_check)
