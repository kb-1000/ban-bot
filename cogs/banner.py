# -*- coding: utf-8 -*-

from discord.ext import commands
import discord
import asyncio
import itertools


class Banner(commands.Cog, name="Main"):
    """The description for Banner goes here."""

    def __init__(self, bot):
        self.bot = bot
        self._reload()

    async def cog_check(self, ctx):
        # checks that apply to every command in here
        return True

    @commands.Cog.listener()
    async def on_message(self, message):
        for url in self.urls:
            if url in message.content and message.guild is not None:
                await asyncio.sleep(0.1)
                await message.guild.ban(message.author, reason="nude sending selfbot")
                return

    # XXX(kb1000): Add fs lock

    @commands.is_owner()
    @commands.command()
    async def addBannedHost(self, ctx, host: str):
        with open("list.txt", "r", encoding="utf-8") as fp:
            banned = set(map(str.strip, fp))
        banned.add(host)
        banned = sorted(banned)
        self.banned = banned
        with open("list.txt", "w", encoding="utf-8") as fp:
            fp.write("\n".join(banned))
        self.urls = list(itertools.chain(*[(f"https://{host}", f"http://{host}") for host in banned]))

    @commands.is_owner()
    @commands.command()
    async def reload(self, ctx):
        return self._reload()

    def _reload(self):
        with open("list.txt", "r", encoding="utf-8") as fp:
            banned = set(map(str.strip, fp))
        banned = sorted(banned)
        self.banned = banned
        with open("list.txt", "w", encoding="utf-8") as fp:
            fp.write("\n".join(banned))
        self.urls = list(itertools.chain(*[(f"https://{host}", f"http://{host}") for host in banned]))


def setup(bot):
    bot.add_cog(Banner(bot))
