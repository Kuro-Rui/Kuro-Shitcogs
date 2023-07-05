from discord.gateway import DiscordWebSocket
from redbot.core import Config, commands

from .converters import WSConverter
from .websockets import *


class WebSocket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 91398293891669, True)
        self.config.register_global(websocket="Web")

        self.old_identify = DiscordWebSocket.identify

    async def cog_load(self):
        websocket = await self.config.websocket()
        if websocket == "Web":
            return
        if websocket == "Android":
            DiscordWebSocket.identify = Android.identify
        elif websocket == "iOS":
            DiscordWebSocket.identify = iOS.identify
        elif websocket == "Client":
            DiscordWebSocket.identify = Client.identify
        for shard_id, shard in self.bot.shards.items():
            await bot.shards[shard_id].reconnect()

    async def cog_unload(self):
        DiscordWebSocket.identify = self.old_identify
        for shard_id, shard in self.bot.shards.items():
            await self.bot.shards[shard_id].reconnect()

    @commands.is_owner()
    @commands.command()
    async def websocket(self, ctx, websocket: WSConverter):
        """
        Change websocket ig.

        You can choose from `Android`, `iOS`, `Client`, or `Web`.
        """
        if websocket == "android":
            await self.config.websocket.set("Android")
            DiscordWebSocket.identify = Android.identify
        elif websocket == "ios":
            await self.config.websocket.set("iOS")
            DiscordWebSocket.identify = iOS.identify
        elif websocket == "client":
            await self.config.websocket.set("Client")
            DiscordWebSocket.identify = Client.identify
        elif websocket == "web":
            DiscordWebSocket.identify = self.old_identify
        await ctx.send("Ok, shards will restart for a short time.")
        for shard in self.bot.shards.values():
            await self.bot.shards[shard].reconnect()
        await ctx.tick()


async def setup(bot):
    await bot.add_cog(WebSocket(bot))
