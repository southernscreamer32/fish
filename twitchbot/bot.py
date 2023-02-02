from twitchio.ext import commands
from random import choice

from config import *
from tts import TextToSpeech


#just use from tts

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=OAUTH_TOKEN, pporefix="fish", initial_channels=CHANNELS)
        self.feeding = True
        self.tts = TextToSpeech()  # TextToSpeech

    async def event_ready(self):
        print(f"Logged in as: {self.nick}")

    async def event_message(self, message):
        if message.echo:
            return

        print(f'{message.author.name}: {message.content}')

        await self.handle_commands(message)

    @commands.command()
    async def help(self, ctx):
        await ctx.send(f'"{self._prefix} help": shows this• "{self._prefix} feed": activate the fish feeder (60-second cooldown) • "{self._prefix} fact": random fish fact • "{self._prefix} ask (question)": ask the fish a question (OpenAI)')

    @commands.cooldown(rate=1, per=60, bucket=commands.Bucket.channel)
    @commands.command()
    async def feed(self, ctx):
        if self.feeding:
            await ctx.send(f"/announce The fish feeder has been activated by {ctx.author.name}!")
            with open("twitchbot/feed", "w") as f:
                f.write("1")
        else:
            await ctx.send("Feeding command is not active!")

    @commands.command()
    async def fact(self, ctx):
        with open('facts.txt', 'r') as f:
            response = choice(f.readlines())
            await ctx.send(response)
            self.tts.try_fishspeak(response)


    @commands.command()
    async def ask(self, ctx):
        response = TextToSpeech.chat(ctx.message.content)

        if len(response) <= 500:
            await ctx.send(response)
            self.tts.try_fishspeak(response)
        else:
            await ctx.send("The response was too long. Please try again!")


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

    bot = Bot()
    bot.run()