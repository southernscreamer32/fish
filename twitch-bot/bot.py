from twitchio.ext import commands
from random import choice

import openai

from config import *

def chatgpt(prompt):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"I am having a conversation and you are a Blue Tilapia in an aquarium. {prompt}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return completion.choices[0].text


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=OAUTH_TOKEN, prefix="fish", initial_channels=CHANNELS)

        self.feeding = True

        self.temp = 0
        self.ph = 0
        self.tds = 0

    async def event_ready(self):
        print(f"Logged in as: {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        print(f'{message.author.name}: {message.content}')

        await self.handle_commands(message)

    @commands.command()
    async def help(self, ctx):
        await ctx.send(f'"{self._prefix} help": shows this • "{self._prefix} stats": current stats from fish tank • "{self._prefix} feed": activate the fish feeder (30-second cooldown)')

    @commands.command()
    async def stats(self, ctx):
        await ctx.send(f"Temp: {self.temp}°C • pH: {self.ph} • TDS: {self.tds} ppm")

    @commands.cooldown(rate=1, per=30, bucket=commands.Bucket.channel)
    @commands.command()
    async def feed(self, ctx):
        if self.feeding:
            await ctx.send(f"/announce The fish feeder has been activated by {ctx.author.name}!")
        else:
            await ctx.send("Feeding command is not active!")

    @commands.command()
    async def fact(self, ctx):
        with open('facts.txt', 'r') as f:
            await ctx.send(choice(f.readlines()))

    @commands.command()
    async def ask(self, ctx):
        response = chatgpt(ctx.message.content)

        await ctx.send(response)


    @commands.command()
    async def toggle(self, ctx):
        if ctx.author.name == "chickwensrule":
            self.feeding = not self.feeding
            await ctx.send(f"/announce Feeding has been {'activated' if self.feeding else 'deactivated'}.")


    async def event_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f'The "{error.command.name}" command is currently on a cooldown for another {round(error.retry_after)} second(s)! {ctx.author.name}')
        elif not isinstance(error, commands.errors.CommandNotFound):
            raise error

if __name__ == "__main__":
    openai.api_key = OPEN_AI_KEY

    bot = Bot()
    bot.run()