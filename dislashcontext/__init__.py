from dislash.application_commands._modifications.old import send_with_components
from redbot.core import Config, commands
from redbot.core.utils.chat_formatting import box

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
        send_monkeypatch = await self.config.send_monkeypatch()
        if send_monkeypatch and not hasattr(commands.Context, send_monkeypatch):
            setattr(commands.Context, send_monkeypatch, send_with_components)

    def cog_unload(self):
        send_monkeypatch = self.settings["send_monkeypatch"]
        if send_monkeypatch and hasattr(commands.Context, send_monkeypatch):
            delattr(commands.Context, send_monkeypatch)

    @commands.is_owner()
    @commands.group()
    async def dctx(self, ctx: commands.Context):
        """DislashContext base command."""
        pass

    @dctx.command(name="set")
    async def dctx_set(self, ctx: commands.Context, name: StrictString):
        """
        Set the name for the monkeypatched `ctx.send`.

        Example: `[p]dctx set sendi`
        If you want to use dislash components, you can call it with `ctx.sendi`
        > `await ctx.sendi("Content", components=[components])`
        """

        if name:
            send_monkeypatch = await self.config.send_monkeypatch()
            if send_monkeypatch:
                delattr(commands.Context, send_monkeypatch)
            await self.config.send_monkeypatch.set(name)
            setattr(commands.Context, name, send_with_components)
            await ctx.tick()
            code = box(
                (
                    "from dislash.interactions import ActionRow, Button, ButtonStyle\n\n"
                    "link_button = ActionRow(\n"
                    "  Button(\n"
                    "    style=ButtonStyle.link,\n"
                    "    label=\"Google\",\n"
                    "    url=\"https://google.com\"\n"
                    "  )\n"
                    ")\n\n"
                    "await ctx.{send}(\"Test\", components=[link_button])"
                ).format(send=name), lang="py"
            )
            await ctx.send(
                (
                    "The monkeypatched send has been set to `ctx.{send}`. "
                    "To test it, run:\n{prefix}eval {code}"
                ).format(send=name, prefix=ctx.prefix, code=code)
            )

    @dctx.command(name="clear", aliases=["remove", "rem"])
    async def dctx_clear(self, ctx: commands.Context):
        """Removes the current monkeypatched `ctx.send`"""

        send_monkeypatch = await self.config.send_monkeypatch()
        if not send_monkeypatch:
            return await ctx.send("Bruh you didn't even set any before.")
        delattr(commands.Context, send_monkeypatch)
        await ctx.tick()
        await ctx.send(f"The `ctx.{send_monkeypatch}` has been removed.")


async def setup(bot):
    cog = DislashContext(bot)
    await cog.initialize()
    bot.add_cog(cog)
