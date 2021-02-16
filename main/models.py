"""Peewee ORM models."""
from __future__ import annotations

import discord

import peewee

from . import config


db = peewee.SqliteDatabase(str(config.BASE_PATH / 'db.sqlite3'))


class BaseModel(peewee.Model):
    """Base model to set default settings."""

    class Meta:
        """Peewee settings."""

        database = db
        use_legacy_table_names = False


class Guild(BaseModel):
    """A model containing data relating to a single server the bot is in."""

    discord_id = peewee.BigIntegerField(primary_key=True)
    prefix = peewee.CharField(max_length=16, default=config.DEFAULT_PREFIX)

    @classmethod
    def get_guild(cls, guild_id: int) -> Guild:
        """Get an instance of the model by Discord guild ID."""
        if guild := cls.get_or_none(cls.discord_id == guild_id):
            return guild
        return cls.create(discord_id=guild_id)

    @classmethod
    def get_by_guild(cls, guild: discord.Guild) -> Guild:
        """Get an instance of the model by Discord.py guild object."""
        return cls.get_guild(guild.id)


MODELS = [Guild]

db.create_tables(MODELS)
