from discord.gateway import DiscordWebSocket
from redbot.core import Config, commands

from .converters import WSConverter
from .websockets import *


class WebSocket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, 91398293891669, True)
        self.config.register_global(websocket="Web")

    @commands.is_owner()
    @commands.command()
    async def websocket(self, ctx, websocket: WSConverter):
        """
        Bot websocket monkeypatch? (No irdumb)

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
            await self.config.websocket.set("Web")
            DiscordWebSocket.identify = Web.identify
        for shard in self.bot.shards.items():
            shard_id = shard[0]
            await self.bot.shards[shard_id].reconnect()
        await ctx.tick()


async def setup(bot):
    bot.add_cog(WebSocket(bot))

    websocket = await bot.get_cog("WebSocket").config.websocket()
    if websocket != "Web":
        if websocket == "Android":
            DiscordWebSocket.identify = Android.identify
        elif websocket == "iOS":
            DiscordWebSocket.identify = iOS.identify
        elif websocket == "Client":
            DiscordWebSocket.identify = Client.identify
        for shard_id, shard in bot.shards.items():
            await bot.shards[shard_id].reconnect()
