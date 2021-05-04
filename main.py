from keep_alive import keep_alive
import os
import discord
import asyncio
import random
import functions

from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

bot = commands.Bot(command_prefix="$")

nav = DefaultMenu("◀️", "▶️")
bot.help_command = PrettyHelp(navigation=nav, color=discord.Colour.green())

# print(len(bot.guilds), bot.guilds)
  
@bot.event
async def on_ready():
  print("I'm in")

class Quiz(commands.Cog):
  """ Use "$quiz <time for each question>" to start the quiz. The deafault time is 30 seconds for each question. Use the "skip" command to skip the question. Use the "quit" command to quit the quiz. DM Light_Yagami#6883 or RishiNandha Vanchi#3379 if you need any help or you have any quesries regarding the bot"""
  @commands.command(
    name="quiz",
    brief="Answer some questions",
    help='Use "$quiz" command to start the quiz'
  )
  
  async def _work(self, message, timeout_=30):
    channel=message.channel

    questions=functions.questions("reactions")
    order=list(range(1,len(questions)))
    #order=[55,56]
    random.shuffle(order)

    correct, wrong, skipped = 0, 0, 0

    for i in order:
      embed=discord.Embed(title=questions[i][0], color=discord.Color.blue(),url="",description=questions[i][3])
      await channel.send(embed=embed)
          
      def funcc(x):

        return ((functions.format(x.content) == functions.format(questions[i][1])) or (x.content == "quit") or (x.content == "skip")) and x.channel==channel

      try:
        global msg
        msg = await bot.wait_for('message', check=funcc,timeout=float(timeout_))


      except asyncio.TimeoutError:
        wrong += 1
        await channel.send("Timeout!, The Answer was:")
        embed2 = discord.Embed(title="", color=discord.Color.red(),url="",description=questions[i][1])
        await channel.send(embed=embed2)
        if len(questions[i][2])>0:
          await channel.send(questions[i][2])
        order.append(i)
        pass

      else:
        if msg.content == "quit":
          await channel.send('{.author} has stopped the quiz'.format(msg))
          await channel.send("Correct: "+str(correct)+"\nSkipped: "+str(skipped)+"\nWrong: "+str(wrong))
          break


        if msg.content == "skip":
          skipped += 1
          await channel.send("Skipped!, The Answer was:")
          embed2 = discord.Embed(title="", color=discord.Color.red(),url="",description=questions[i][1])
          await channel.send(embed=embed2)
          if len(questions[i][2])>0:
            await channel.send(questions[i][2])
          order.append(i)
          continue
        
        else: 
          correct += 1
          s = '{.author} got the correct answer! \n' + questions[i][2]
          await msg.channel.send(s.format(msg))
          if i==order[-1]:
            embed4=discord.Embed(title="Conquered!",color=discord.Color.gold(),url="https://www.youtube.com/watch?v=Utgrbq_CFt4",description="GGs!, You are dang OP")
            await channel.send(embed=embed4)


bot.add_cog(Quiz(bot))
keep_alive()
bot.run(os.getenv("TOKEN"))