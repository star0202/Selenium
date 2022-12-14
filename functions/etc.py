from logging import getLogger

from discord.commands import ApplicationContext
from discord.ext import commands
from discord.ui import Button, View

from utils.commands import slash_command

logger = getLogger(__name__)


class GithubLink(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="🛠️", url="https://github.com/star0202/Selenium"))


class Etc(commands.Cog):
    @slash_command(name="소스코드", description="봇 소스코드 링크를 출력합니다.")
    async def github_repo(self, ctx: ApplicationContext):
        await ctx.respond("깃허브 바로가기!", view=GithubLink())


def setup(bot):
    logger.info("Loaded")
    bot.add_cog(Etc(bot))


def teardown():
    logger.info("Unloaded")
