from logging import getLogger

from discord import Embed
from discord.commands import ApplicationContext
from discord.ext import commands

from config import COLOR
from utils.commands import slash_command

logger = getLogger(__name__)


helpembed = Embed(title="도움말", description="`[값]`: 필수 입력 `(값)`: 선택 입력", color=COLOR)
helpembed.add_field(name="/급식 `(영양소)`", value="급식을 출력합니다. 만약 영양소를 체크했다면 영양소를 출력합니다.", inline=False)
helpembed.add_field(name="/등록 `[학년]` `[반]`", value="유저의 반을 등록합니다. 등록한 이후엔 /시간표 만으로 시간표를 확인할 수 있습니다.", inline=False)
helpembed.add_field(name="/등록해제", value="유저의 반 데이터를 삭제합니다.", inline=False)
helpembed.add_field(name="/봇", value="봇에 대한 정보를 출력합니다.", inline=False)
helpembed.add_field(name="/소스코드", value="봇 소스코드 링크를 출력합니다.", inline=False)
helpembed.add_field(name="/시간표 `(학년)` `(반)`", value="`학년` `반`의 시간표를 출력합니다.", inline=False)
helpembed.add_field(name="/핑", value="퐁!", inline=False)


class Help(commands.Cog):
    @slash_command(name="도움말", description="도움말을 출력합니다.")
    async def help(self, ctx: ApplicationContext):
        await ctx.respond(embed=helpembed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Help(bot))


def teardown():
    logger.info("Unloaded")
