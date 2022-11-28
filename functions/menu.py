from datetime import datetime
from json import loads
from logging import getLogger
from os import getenv
from re import findall, sub

from discord import Embed
from discord.commands import ApplicationContext, Option
from discord.ext import commands
from pytz import timezone
from requests import get

from config import BAD, COLOR
from utils.commands import slash_command

logger = getLogger(__name__)


class Menu(commands.Cog):
    @slash_command(name="급식", description="급식을 출력합니다.")
    async def menu(
            self,
            ctx: ApplicationContext,
            year: Option(int, name="연도", description="연도를 입력하세요", required=False),
            month: Option(int, name="월", description="월을 입력하세요", required=False),
            day: Option(int, name="일", description="일을 입력하세요", required=False)
    ):
        pattern_allergic = r"[0-9\.]+"
        pattern_menu = r"\s+\([0-9\.]+\)"
        today = datetime.now(tz=timezone("Asia/Seoul"))
        if not year:
            year = today.year
        if not month:
            month = today.month
        if not day:
            day = today.day
        key = getenv("NEIS_KEY")
        url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}&Type=json&pIndex=1&pSize=10&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7091455&MLSV_YMD={year}{month}{day}"
        req = get(url)
        data = loads(req.text)["mealServiceDietInfo"]
        head = data[0]["head"][1]
        row = data[1]["row"][0]
        if head["RESULT"]["CODE"] != "INFO-000":
            embed = Embed(title="오류 발생", description="개발자에게 문의 바랍니다.", color=BAD)
            embed.add_field(name="CODE", value=head["RESULT"]["CODE"])
            embed.add_field(name="MESSAGE", value=head["RESULT"]["MESSAGE"])
            await ctx.respond(embed=embed)
            return
        menu_raw = row["DDISH_NM"].replace("<br/>", "")
        menu = sub(pattern=pattern_menu, repl="() ", string=menu_raw).split()
        menu_allergic = findall(pattern=pattern_allergic, string=menu_raw)
        menu_dict = {}
        for x in menu:
            if x.endswith("()"):
                menu_dict[x.replace("()", "")] = menu_allergic.pop(0)
            else:
                menu_dict[x] = "알러지 정보 없음"
        embed = Embed(title=f"{year}/{month}/{day} 급식 정보", description="작은 글씨는 알러지 정보입니다.", color=COLOR)
        for x in menu_dict.keys():
            embed.add_field(name=x, value=menu_dict[x])
        await ctx.respond(embed=embed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Menu())


def teardown():
    logger.info("Unloaded")
