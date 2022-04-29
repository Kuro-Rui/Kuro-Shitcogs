from redbot.core.commands import Context, Converter


class StrictString(Converter):
    async def convert(self, ctx, argument: str):
        try:
            int_argument = int(argument)  # Just to see if it's a string integer or not.
            await ctx.send(f"How tf am I supposed to do that??? Imagine `ctx.{argument}`, lol.")
            return
        except:
            argument = argument.replace(" ", "_")
            if hasattr(Context, argument):
                await ctx.send(f"Please don't break me, I already have `ctx.{argument}`.")
                return
            return argument
