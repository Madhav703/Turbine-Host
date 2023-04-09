from multiprocessing import context
import discord
from datetime import datetime
import json
import aiohttp
import asyncio
from discord.ext import commands
from asyncio import sleep
import os
import typing
from discord.ext.commands import Cog, BucketType
from cogs.help import HelpCommand

with open('config.json') as f:
    data = json.load(f)
    token = data["TOKEN"]

__all__ = ("Turbine", "bot")
on_startup: typing.List[typing.Callable[["Turbine"], typing.Coroutine]] = []

owners = [995000644660383764,939887303403405402,650336213219278849] 

intents = discord.Intents.all()

initial_extensions = ['cogs.utility',
                      'cogs.mod',
                      'cogs.owner',
                      'cogs.games',
                      'cogs.events'
         
                      ] 

class Turbine(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(
            activity=discord.Activity(type=discord.ActivityType.watching, name="Turbine Host"),
            command_prefix=self.get_prefix,
            case_insensitive=True,
            strip_after_prefix=True,
            owner_ids=set(owners),
            help_command=HelpCommand(),
            intents=intents,
            allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, replied_user=False),
            **kwargs,
        )

        self.loop = asyncio.get_event_loop()
        self.session = aiohttp.ClientSession()
        self.seen_messages = 0
        self.color = 0x00ffb3
        self.owner = "<:owner:1015528945338294364>"
        self.yes = "<:tick_yes:1015298407843246160>"
        self.no = "<:xxcross:1038116049159213138>"
        self.ban = "<a:banned:1015602109384765533>"
        self.dot = "<:turbine_dot:1089880285086228612>"
        self.text = "<:champ_text:1032282847618269285>"
        self.voice = "<:champ_vc:1032282961468469309>"
        self.stage = "<:champ_stage:1032283082348302406>"
        self.me = "<:Champ:1032283338976800818>"
        self.python = "<:Python:1032283430970458122>"
        self.dpy = "<:dpy:1032283514458079313>"
        self.emoji = "<:bots:1041267739437826099>"
        self.human = "<:members:1014897190411436175>"
        self.admin = "<:Admin:1018824842843267112>"
        self.boosts = "<a:Nitroboostyy:1015326687430455347>"

    async def setup_hook(self) -> None:
        for coro_func in on_startup:
            await (coro_func(self))

    @on_startup.append
    async def __load_extensions(self):
        for _ in initial_extensions:
            await self.load_extension(_)
            print(f"Loaded extension: {_}")
           

        await self.load_extension("jishaku")
        print(f"Loaded extension: jishaku")

    @on_startup.append
    async def __set_env(self):
        os.environ["JISHAKU_HIDE"] = "True"
        os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
        os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
        os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

    async def on_ready(self):
        print("Logged in as {0} ({0.id})".format(self.user))

    

    async def on_message(self, message: discord.Message):

        if not message.guild or message.author.bot:
            return

        await self.process_commands(message)
        
    async def on_message_edit(self, before: discord.Message,after: discord.Message):
        if after.guild is None or after.author.bot:
            return
        if before.content != after.content and before.author.id in self.owner_ids:
            await self.process_commands(after)

    
    async def get_prefix(bot, message):
        if message.author.id in bot.owner_ids:
            return commands.when_mentioned_or("$", "")(bot, message)
        else:
            return commands.when_mentioned_or("?")(bot, message)

    
bot = Turbine()
bot.run(token)
