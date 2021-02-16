"""The meta cog."""
import discord
from discord.ext import commands

from main import checks, config, errors, models


ABOUT = (
    'A moderation/general purpose bot by Artemis ([artemisdev.xyz]'
    '(https://artemisdev.xyz)). I only add to this when I need a feature, so '
    'please don\'t send me feature requests unless there is a feature no '
    'other bot implements.'
)


class Meta(commands.Cog):
    """Commands relating to the bot itself."""

    def __init__(self, bot: commands.Bot):
        """Set the help command cog to this one."""
        self.bot = bot
        self.bot.help_command.cog = self

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Send prefix if bot is mentioned."""
        prefix = None
        if message.guild:
            if message.guild.me in message.mentions:
                prefix = models.Guild.get_by_guild(message.guild).prefix
        else:
            if self.bot.user in message.mentions:
                prefix = config.DEFAULT_PREFIX
        if prefix is not None:
            await message.channel.send(f'My prefix is `{prefix}`.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: Exception):
        """Handle an error."""
        await errors.on_command_error(ctx, error)

    @commands.command(brief='About the bot.')
    async def about(self, ctx: commands.Context):
        """Get some information about the bot."""
        embed = discord.Embed(
            title='About',
            description=ABOUT,
            colour=0x45b3e0
        )
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(brief='Change the prefix.')
    @commands.has_guild_permissions(manage_guild=True)
    @checks.requires_guild()
    async def prefix(self, ctx: commands.Context, *, prefix: str):
        """Change the bot prefix.

        Example: `{{pre}}prefix m!`
        You can always find out the bot's prefix by mentioning it.
        """
        ctx.guild_model.prefix = prefix
        ctx.guild_model.save()
        await ctx.send(f'Updated server prefix to `{prefix}`.')
