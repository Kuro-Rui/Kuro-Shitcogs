from redbot.core.commands import BadArgument, Context, Converter


class StrictString(Converter):
    async def convert(self, ctx, argument: str):
        try:
            int_argument = int(argument)  # Just to see if it's a string integer or not.
            raise BadArgument(f"How tf am I supposed to do that??? Imagine `ctx.{argument}`, lol.")
        except:
            argument = argument.replace(" ", "_")
            if hasattr(Context, argument):
                raise BadArgument(f"Please don't break me, I already have `ctx.{argument}`.")
            else:
                return argument
