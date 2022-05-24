from redbot.core.commands import BadArgument, Converter


class WSConverter(Converter):
    async def convert(self, ctx, argument):
        if argument.lower() not in ["android", "ios", "client", "web"]:
            raise BadArgument("Must be either `Android`, `iOS`, `Client`, or `Web`.")
        return argument.lower()
