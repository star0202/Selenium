from logging import getLogger
from os import getenv, listdir
from time import time
from traceback import format_exception
from sys import exc_info
from uuid import uuid4

import discord
from discord.ext import commands

from config import BAD, STATUS
from utils.logger import setup_logging


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.all(), help_command=None)
        setup_logging()
        self.logger = getLogger(__name__)
        self.start_time = time()
        self.session = uuid4()
        for filename in listdir("functions"):
            if filename.endswith(".py"):
                self.load_cog(f"functions.{filename[:-3]}")
        self.logger.info(f"{len(self.extensions)} extensions are completely loaded")
        self.load_extension("jishaku")

    def load_cog(self, cog: str):
        try:
            if type(self.load_extension(cog, store=True)[cog]) == discord.ExtensionFailed:
                self.logger.error(self.load_extension(cog)[cog])
        except Exception as e:
            self.logger.error(e)

    def run(self):
        super().run(getenv("TOKEN"))

    async def on_ready(self):
        self.logger.info(f"Logged in as {self.user.name}")
        self.logger.info(f"Session ID: {self.session}")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Game(STATUS),
        )
        await self.wait_until_ready()

    async def on_command_error(self, ctx: discord.ApplicationContext, error: discord.ApplicationCommandError):
        text = "".join(format_exception(type(error), error, error.__traceback__))
        self.logger.error(text)
        await ctx.send(
            embed=discord.Embed(
                title="오류 발생",
                description="개발자에게 문의 바랍니다.",
                color=BAD
            )
        )

    async def on_error(self, event, *args, **kwargs):
        error = exc_info()
        text = f"{error[0].__name__}: {error[1]}"
        await args[0].channel.send(
            embed=discord.Embed(
                title="오류 발생",
                description="개발자에게 문의 바랍니다.",
                color=BAD
            )
        ) if not args[0] is None else None
        self.logger.error(text)

    async def on_application_command(self, ctx: discord.ApplicationContext):
        self.logger.info(f"{ctx.user}({ctx.user.id}): /{ctx.command.name}"
                         f"{' ' + str(ctx.selected_options) if ctx.selected_options else ''}")
