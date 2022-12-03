from logging import getLogger

import discord
from discord.commands import ApplicationContext
from discord.ext import commands

from config import COLOR
from utils.commands import slash_command

logger = getLogger(__name__)
help_select_raw = {
    "/급식": "급식을 출력합니다.",
    "/등록": "학생 데이터를 등록합니다.",
    "/등록해제": "학생 데이터를 등록 해제합니다.",
    "/봇": "봇의 정보를 출력합니다.",
    "/소스코드": "봇의 소스코드 링크를 출력합니다.",
    "/시간표": "시간표를 출력합니다.",
    "/핑": "봇의 핑을 출력합니다."
}
help_embed_raw = {
    "/급식": "그날의 급식을 출력합니다. 아래에 있는 버튼으로 날짜 조정, 영양소 표시를 할 수 있습니다.",
    "/등록 `[학년]` `[반]`": "학생 데이터를 `[학년]` `[반]`으로 저장합니다.",
    "/등록해제": "학생 데이터를 삭제합니다.",
    "/봇": "봇의 정보를 출력합니다.",
    "/소스코드": "봇 깃허브 레포지토리 링크를 출력합니다.",
    "/시간표 `(학년)` `(반)`": "`(학년)` `(반)`의 그 주 시간표를 출력합니다. /등록 명령어로 학생 데이터를 등록하면 학년과 반을 입력할 필요가 없습니다.",
    "/핑": "봇의 핑을 출력합니다."
}

help_select = []
help_list = []
help_embed = []
for command in help_select_raw:
    help_list.append(command)
    help_select.append(
        discord.SelectOption(
            label=command,
            description=help_select_raw[command]
        )
    )
for command in help_embed_raw:
    help_embed.append(
        discord.Embed(
            title=command,
            description=help_embed_raw[command],
            color=COLOR
        )
    )


class HelpMenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    @discord.ui.select(placeholder="명령어를 선택하세요", options=help_select)
    async def callback(self, select, interaction: discord.Interaction):
        await interaction.response.edit_message(embed=help_embed[help_list.index(select.values[0])], view=self)


class Help(commands.Cog):
    @slash_command(name="도움말", description="도움말을 출력합니다.")
    async def help(self, ctx: ApplicationContext):
        embed = discord.Embed(title="도움말", description="메뉴에서 원하는 명령어를 선택하세요.", color=COLOR)
        embed.add_field(name="참고사항", value="`[입력값]` : 필수 입력값  |  `(입력값)` : 선택 입력값")
        await ctx.respond(embed=embed, view=HelpMenu())


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Help(bot))


def teardown():
    logger.info("Unloaded")
