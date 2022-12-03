from logging import getLogger
from time import time

from discord import Embed
from discord.commands import ApplicationContext, Option
from discord.ext import commands

from config import COLOR
from utils.commands import slash_command
from utils.bot import Bot

logger = getLogger(__name__)


class Default(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @slash_command(name="핑", description="봇의 핑을 전송합니다.")
    async def ping(self, ctx: ApplicationContext):
        embed = Embed(title=":ping_pong: 퐁!", color=COLOR)
        embed.add_field(
            name="discord API Ping: ", value=f"{round(self.bot.latency * 1000)} ms"
        )
        await ctx.respond(embed=embed)

    @slash_command(name="봇", description="봇의 정보를 전송합니다.")
    async def botinfo(self, ctx: ApplicationContext):
        nowtime = time()
        s = round(nowtime - self.bot.start_time)
        d = 0
        h = 0
        m = 0
        while s >= 86400:
            s = s - 86400
            d += 1
        while s >= 3600:
            s = s - 3600
            h += 1
        while s >= 60:
            s = s - 60
            m += 1
        embed = Embed(title="봇 정보", color=COLOR)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name="봇 이름", value=f"**{self.bot.user.name}** ({str(self.bot.user)})", inline=False)
        embed.add_field(
            name="업타임", value=f"{d} 일 {h} 시간 {m} 분 {s} 초",
            inline=False
        )
        embed.add_field(name="봇 ID", value=str(self.bot.user.id), inline=False)
        await ctx.respond(embed=embed)

    @slash_command()
    async def stop(self, ctx: ApplicationContext):
        if await self.bot.is_owner(ctx.user):
            await ctx.respond("stopping..")
            await self.bot.close()

    @slash_command()
    async def reload_ext(self, ctx: ApplicationContext, ext_name: Option(str)):
        if await self.bot.is_owner(ctx.user):
            self.bot.unload_extension(f"functions.{ext_name}")
            self.bot.load_extension(f"functions.{ext_name}")
            await ctx.respond(f"{ext_name}.py reloaded")

    @slash_command()
    async def send_here(self, ctx: ApplicationContext, content: Option(str)):
        await ctx.send(content)
        delete_this = await ctx.respond("random respond")
        await delete_this.delete_original_response()


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Default(bot))


def teardown():
    logger.info("Unloaded")
