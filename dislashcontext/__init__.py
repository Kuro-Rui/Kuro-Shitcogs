import discord
from dislash.interactions import ActionRow, Button, ButtonStyle
from dislash.application_commands._modifications.old import send_with_components
from redbot.core import Config, commands
from typing import Optional

from .converters import StrictString


class DislashContext(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 9937656857, True)
        default_global = {"send_monkeypatch": None}
        self.config.register_global(**default_global)
        self.settings = {}

    async def initialize(self):
        self.settings = await self.config.all()
        if self.settings["send_monkeypatch"] and not hasattr(commands.Context, self.settings["send_monkeypatch"]):
            setattr(commands.Context, self.settings["send_monkeypatch"], send_with_components)

    def cog_unload(self):
        if self.settings["send_monkeypatch"] and hasattr(commands.Context, self.settings["send_monkeypatch"]):
                delattr(commands.Context, self.settings["send_monkeypatch"])

    @commands.is_owner()
    @commands.group()
    async def dctx(self, ctx: commands.Context, name: Optional[StrictString]):
        """
        Set the name for the monkeypatched `ctx.send`.

        Example: `[p]dctx sendi`
        If you want to use dislash components, you can call it with `ctx.sendi`
        > `await ctx.sendi("Content", components=[components])`
        """

        if not name:
            if self.settings["send_monkeypatch"]:
                delattr(commands.Context, self.settings["send_monkeypatch"])
                self.settings["send_monkeypatch"] = None
                return await ctx.send("The monkeypatched `ctx.send` has been removed.")
        self.settings["send_monkeypatch"] = name
        setattr(commands.Context, self.settings["send_monkeypatch"], send_with_components)
        await ctx.tick()
        await ctx.send(
            "The monkeypatched send has been set to `ctx.{send}`.\n"
            "If you want to test it, run:\n"
            "{prefix}eval ```py\n"
            "from dislash.interactions import ActionRow, Button, ButtonStyle\n\n"
            "link_button = ActionRow(\n"
            "  Button(\n"
            "    style=ButtonStyle.link,\n"
            "    label=\"Google\",\n"
            "    url=\"https://google.com\"\n"
            "  )\n"
            ")\n\n"
            "await ctx.{send}(\"Test\", components=[link_button])\n"
            "```"
        ).format(send=self.settings["send_monkeypatch"], prefix=ctx.prefix)


async def setup(bot):
    cog = DislashContext(bot)
    await cog.initialize()
    bot.add_cog(cog)
