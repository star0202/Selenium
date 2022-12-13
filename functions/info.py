from logging import getLogger

from discord import Embed, Colour, Member, guild_only
from discord.commands import ApplicationContext, Option
from discord.ext import commands

from config import COLOR
from utils.commands import slash_command
from utils.utils import datetime_to_unix

logger = getLogger(__name__)


class Info(commands.Cog):
    @slash_command(name="유저정보", description="유저의 정보를 전송합니다.")
    async def user_info(
            self,
            ctx: ApplicationContext,
            user: Option(
                Member, required=False, name="유저", description="정보를 출력할 유저를 입력하세요, 자신을 원한다면 비워두세요."
            )
    ):
        if user is None:
            user = ctx.author
        embed = Embed(colour=COLOR if user.color == Colour.default() else user.color, title=str(user))
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="계정명", value=str(user))
        embed.add_field(name="닉네임", value=user.display_name)
        embed.add_field(name="ID", value=str(user.id))
        embed.add_field(name="최상위 역할", value=str(user.top_role))
        embed.add_field(name="유형", value="봇" if user.bot else "일반 유저")
        embed.add_field(
            name="계정 생성 날짜",
            value=f"<t:{datetime_to_unix(user.created_at)}:R> ({user.created_at.strftime('%Y/%m/%d %H:%M:%S')})"
        )
        await ctx.respond(embed=embed)

    @slash_command(name="서버정보", description="현재 서버의 정보를 전송합니다.")
    @guild_only()
    async def server_info(self, ctx: ApplicationContext):
        server = ctx.guild
        embed = Embed(colour=COLOR, title=server.name)
        embed.set_thumbnail(url=server.icon.url if server.icon else Embed.Empty)
        embed.add_field(name="소유자", value=server.owner.mention)
        user = 0
        bot = 0
        async for x in server.fetch_members():
            if x.bot:
                bot += 1
            else:
                user += 1
        embed.add_field(name="멤버 수", value=f"유저 {user}명, 봇 {bot}개", inline=False)
        embed.add_field(name="ID", value=str(server.id), inline=False)
        embed.add_field(name="역할 개수", value=f"{len(server.roles)}개", inline=False)
        embed.add_field(
            name="서버 생성 날짜",
            value=f"<t:{datetime_to_unix(server.created_at)}:R> ({server.created_at.strftime('%Y/%m/%d %H:%M:%S')})",
            inline=False
        )
        await ctx.respond(embed=embed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Info())


def teardown():
    logger.info("Unloaded")
