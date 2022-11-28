from discord.ext import commands
import discord
from discord.commands import ApplicationContext, Option
from utils.commands import slash_command
import logging
from comcigan import AsyncSchool
from config import COLOR, BAD
import sqlite3
import requests
from pytz import timezone
from datetime import datetime
from os import getenv
import json
from re import findall, sub

logger = logging.getLogger(__name__)
days = ["월", "화", "수", "목", "금", "토"]


class School(commands.Cog):
    def __init__(self):
        self.conn = sqlite3.connect("database.db", isolation_level=None)
        self.cursor = self.conn.cursor()

    @slash_command(name="등록", description="학생 데이터를 등록합니다.")
    async def register(
            self,
            ctx: ApplicationContext,
            grade_num: Option(int, name="학년", description="학년을 입력하세요"),
            class_num: Option(int, name="반", description="반을 입력하세요")
    ):
        self.cursor.execute(f"SELECT * FROM UserData WHERE Id={ctx.author.id}")
        if self.cursor.fetchone():
            self.cursor.execute(f"UPDATE UserData SET Grade={grade_num}, Class={class_num} WHERE Id={ctx.user.id}")
            embed = discord.Embed(title="학생 데이터 수정 완료", description=f"`{grade_num}`학년 `{class_num}`반으로 수정되었습니다.", color=COLOR)
        else:
            self.cursor.execute(f"INSERT INTO UserData VALUES({ctx.user.id}, {grade_num}, {class_num})")
            embed = discord.Embed(title="학생 데이터 등록 완료", description=f"`{grade_num}`학년 `{class_num}`반으로 등록되었습니다.", color=COLOR)
        await ctx.respond(embed=embed)

    @slash_command(name="등록해제", description="학생 데이터를 등록 해제합니다.")
    async def deregister(self, ctx: ApplicationContext):
        self.cursor.execute(f"DELETE FROM UserData WHERE Id={ctx.author.id}")
        embed = discord.Embed(title="학생 데이터 등록 해제 완료", description="등록이 해제되었습니다.", color=COLOR)
        await ctx.respond(embed=embed)

    @slash_command(name="시간표", description="오늘 시간표를 출력합니다.")
    async def schedule(
            self,
            ctx: ApplicationContext,
            grade_num: Option(int, name="학년", description="학년을 입력하세요", required=False),
            class_num: Option(int, name="반", description="반을 입력하세요", required=False)
    ):
        registered = False
        self.cursor.execute(f"SELECT * FROM UserData WHERE Id={ctx.user.id}")
        data = self.cursor.fetchone()
        if data:
            grade_num = data[1]
            class_num = data[2]
            registered = True
        elif not (grade_num and class_num):
            embed = discord.Embed(title="오류 발생", description="학년과 반을 입력하시거나, /등록 명령어를 통해 학년과 반을 등록해주세요.", color=BAD)
            await ctx.respond(embed=embed)
            return
        jd = await AsyncSchool.init("중동중학교")
        embed = discord.Embed(title=f"{grade_num}학년 {class_num}반 시간표", color=COLOR)
        try:
            jd[grade_num][class_num]
        except IndexError:
            embed = discord.Embed(title="오류 발생", description="학년, 반을 다시 한번 확인해주세요", color=BAD)
            return await ctx.respond(embed=embed)
        for day in range(6):
            try:
                temp = ""
                for classes in jd[grade_num][class_num][day]:
                    temp += classes[0] + " "
                if temp == "":
                    embed.add_field(name=f"{days[day]}요일", value="정보 없음", inline=False)
                else:
                    embed.add_field(name=f"{days[day]}요일", value=temp, inline=False)
            except IndexError:
                continue
        await ctx.respond(embed=embed)
        if not registered:
            await ctx.send("/등록 명령어로 학년과 반을 등록해 /시간표 만으로 시간표를 확인할 수 있어요!")

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
        req = requests.get(url)
        data = json.loads(req.text)["mealServiceDietInfo"]
        head = data[0]["head"][1]
        row = data[1]["row"][0]
        if head["RESULT"]["CODE"] != "INFO-000":
            embed = discord.Embed(title="오류 발생", description="개발자에게 문의 바랍니다.", color=BAD)
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
        embed = discord.Embed(title=f"{year}/{month}/{day} 급식 정보", description="작은 글씨는 알러지 정보입니다.", color=COLOR)
        for x in menu_dict.keys():
            embed.add_field(name=x, value=menu_dict[x])
        await ctx.respond(embed=embed)


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(School())


def teardown():
    logger.info("Unloaded")
