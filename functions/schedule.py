from logging import getLogger
from sqlite3 import connect

from comcigan import AsyncSchool
from discord import Embed
from discord.commands import ApplicationContext, Option
from discord.ext import commands

from config import BAD, COLOR
from utils.commands import slash_command
from constants import DAYS

logger = getLogger(__name__)


class Schedule(commands.Cog):
    def __init__(self):
        self.conn = connect("database.db", isolation_level=None)
        self.conn.set_trace_callback(logger.debug)
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS UserData(Id int, Grade int, Class int)")

    @slash_command(name="등록", description="학생 데이터를 등록합니다.")
    async def register(
            self,
            ctx: ApplicationContext,
            grade_num: Option(int, name="학년", description="학년을 입력하세요", choices=[1, 2, 3]),
            class_num: Option(int, name="반", description="반을 입력하세요", choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
    ):
        self.cursor.execute(f"SELECT * FROM UserData WHERE Id={ctx.user.id}")
        if self.cursor.fetchone():
            self.cursor.execute(f"UPDATE UserData SET Grade={grade_num}, Class={class_num} WHERE Id={ctx.user.id}")
            embed = Embed(title="학생 데이터 수정 완료", description=f"`{grade_num}`학년 `{class_num}`반으로 수정되었습니다.", color=COLOR)
        else:
            self.cursor.execute(f"INSERT INTO UserData VALUES({ctx.user.id}, {grade_num}, {class_num})")
            embed = Embed(title="학생 데이터 등록 완료", description=f"`{grade_num}`학년 `{class_num}`반으로 등록되었습니다.", color=COLOR)
        await ctx.respond(embed=embed)

    @slash_command(name="등록해제", description="학생 데이터를 등록 해제합니다.")
    async def deregister(self, ctx: ApplicationContext):
        self.cursor.execute(f"DELETE FROM UserData WHERE Id={ctx.user.id}")
        embed = Embed(title="학생 데이터 등록 해제 완료", description="등록이 해제되었습니다.", color=COLOR)
        await ctx.respond(embed=embed)

    @slash_command(name="시간표", description="시간표를 출력합니다.")
    async def schedule(
            self,
            ctx: ApplicationContext,
            grade_num: Option(int, name="학년", description="학년을 입력하세요", required=False, choices=[1, 2, 3]),
            class_num: Option(
                int,
                name="반",
                description="반을 입력하세요",
                required=False,
                choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            ),
    ):
        self.cursor.execute(f"SELECT * FROM UserData WHERE Id={ctx.user.id}")
        data = self.cursor.fetchone()
        if data:
            grade_num = data[1]
            class_num = data[2]
        elif not (grade_num and class_num):
            embed = Embed(title="오류 발생", description="학년과 반을 입력하시거나, /등록 명령어를 통해 학년과 반을 등록해주세요.", color=BAD)
            await ctx.respond(embed=embed)
            return
        jd = await AsyncSchool.init("중동중학교")
        embed = Embed(title=f"{grade_num}학년 {class_num}반 시간표", color=COLOR)
        try:
            jd[grade_num][class_num]
        except IndexError:
            embed = Embed(title="오류 발생", description="학년, 반을 다시 한번 확인해주세요", color=BAD)
            return await ctx.respond(embed=embed)
        for day in range(6):
            try:
                temp = ""
                for classes in jd[grade_num][class_num][day]:
                    temp += classes[0] + " "
                if temp == "":
                    embed.add_field(name=f"{DAYS[day]}요일", value="정보 없음", inline=False)
                else:
                    embed.add_field(name=f"{DAYS[day]}요일", value=temp, inline=False)
            except IndexError:
                continue
        await ctx.respond(embed=embed)
        if not data:
            await ctx.send("/등록 명령어로 학년과 반을 등록해 /시간표 만으로 시간표를 확인할 수 있어요!")


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Schedule())


def teardown():
    logger.info("Unloaded")
