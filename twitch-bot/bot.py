from twitchio.ext import commands

from config import *

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=OAUTH_TOKEN, prefix="fish", initial_channels=CHANNELS)

        self.temp = 0
        self.ph = 0
        self.tds = 0

    async def event_ready(self):
        print(f"Logged in  as {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        print(f'{message.author.name}: {message.content}')

        await self.handle_commands(message)

    @commands.command()
    async def stats(self, ctx):
        await ctx.send(f"Temp: {self.temp}°C • pH: {self.ph} • TDS: {self.tds} ppm")

    @commands.cooldown(rate=1, per=30, bucket=commands.Bucket.channel)
    @commands.command()
    async def feed(self, ctx):
        await ctx.send(f"/announce The fish feeder has been activated by {ctx.author.name}!")

    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f'The "{error.command.name}" command is currently on a cooldown for another {round(error.retry_after)} second(s)! {ctx.author.name}')

if __name__ == "__main__":
    bot = Bot()
    bot.run()