from datetime import datetime, timedelta
from json import loads
from logging import getLogger
from os import getenv
from re import findall, sub

import discord
from discord.commands import ApplicationContext, Option
from discord.ext import commands
from requests import get

from config import BAD, COLOR
from utils.commands import slash_command
from utils.gettime import get_time

logger = getLogger(__name__)
key = getenv("NEIS_KEY")


def get_menu(api_key: str, time: datetime, ntr: bool) -> discord.Embed:
    year = time.year
    month = time.month
    day = time.day
    fday = format(day, "02d")
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={api_key}&Type=json&pIndex=1&pSize=10&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7091455&MLSV_YMD={year}{month}{fday}"
    req = get(url)
    try:
        data = loads(req.text)["mealServiceDietInfo"]
    except KeyError:
        data = loads(req.text)["RESULT"]
        if data["CODE"] == "INFO-200":
            embed = discord.Embed(
                title=f"{year}/{month}/{day} 급식 정보",
                description="급식 정보가 없습니다, 날짜를 확인해주세요.",
                color=BAD
            )
            embed.add_field(name="CODE", value=data["CODE"])
            embed.add_field(name="MESSAGE", value=data["MESSAGE"])
            return embed
        embed = discord.Embed(title="오류 발생", description="개발자에게 문의 바랍니다.", color=BAD)
        embed.add_field(name="CODE", value=data["CODE"])
        embed.add_field(name="MESSAGE", value=data["MESSAGE"])
        return embed
    row = data[1]["row"][0]
    if ntr:
        pattern_ntr_amt = r"[0-9]+\.[0-9]+"
        pattern_ntr_name = r"\(.{1,3}\)[^가-힇]+"
        pattern_ntr_unit = r"\(.{1,3}\)"
        cal = row["CAL_INFO"].replace("<br/>", "").split()
        ntr = row["NTR_INFO"].replace("<br/>", "")
        ntr_amt = findall(pattern=pattern_ntr_amt, string=ntr)
        ntr_name = sub(pattern=pattern_ntr_name, repl=" ", string=ntr).split()
        ntr_unit = findall(pattern=pattern_ntr_unit, string=ntr)
        ntr_dict = {"칼로리": (cal[0], f"({cal[1]})")}
        for x in ntr_name:
            ntr_dict[x] = (ntr_amt.pop(0), ntr_unit.pop(0))
        embed = discord.Embed(title=f"{year}/{month}/{day} 급식 영양소 정보", color=COLOR, description="📃 : 급식 보기")
        for x in ntr_dict:
            embed.add_field(name=x, value=f"{ntr_dict[x][0]} {ntr_dict[x][1]}")
    else:
        pattern_allergic = r"[0-9\.]+"
        pattern_menu = r"\s+\([0-9\.]+\)"
        menu_raw = row["DDISH_NM"].replace("<br/>", "")
        menu = sub(pattern=pattern_menu, repl="() ", string=menu_raw).split()
        menu_allergic = findall(pattern=pattern_allergic, string=menu_raw)
        menu_dict = {}
        for x in menu:
            if x.endswith("()"):
                menu_dict[x.replace("()", "")] = menu_allergic.pop(0)
            else:
                menu_dict[x] = "알러지 정보 없음"
        embed = discord.Embed(
            title=f"{year}/{month}/{day} 급식 정보",
            description="작은 글씨는 알러지 정보입니다. 📃 : 영양소 보기",
            color=COLOR
        )
        for x in menu_dict:
            embed.add_field(name=x, value=menu_dict[x])
    return embed


class MenuControl(discord.ui.View):
    def __init__(self, ntr):
        super().__init__(timeout=60)
        self.today = get_time()
        self.ntr = ntr

    @discord.ui.button(label="◀️", style=discord.ButtonStyle.blurple)
    async def yesterday(self, _, interaction: discord.Interaction):
        self.today -= timedelta(days=1)
        await interaction.response.edit_message(embed=get_menu(key, self.today, self.ntr), view=self)

    @discord.ui.button(label="📃", style=discord.ButtonStyle.gray)
    async def toggle_ntr(self, _, interaction: discord.Interaction):
        self.ntr = not self.ntr
        await interaction.response.edit_message(embed=get_menu(key, self.today, self.ntr), view=self)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.blurple)
    async def tomorrow(self, _, interaction: discord.Interaction):
        self.today += timedelta(days=1)
        await interaction.response.edit_message(embed=get_menu(key, self.today, self.ntr), view=self)


class Menu(commands.Cog):
    @slash_command(name="급식", description="급식을 출력합니다.")
    async def menu(
            self,
            ctx: ApplicationContext,
            ntr: Option(bool, name="영양소", desciprion="영양소 정보를 표시합니다", required=False, default=False)
    ):
        today = get_time()
        await ctx.respond(embed=get_menu(key, today, ntr), view=MenuControl(ntr))


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Menu())


def teardown():
    logger.info("Unloaded")
