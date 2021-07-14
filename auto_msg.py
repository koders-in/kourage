import discord
import random
import aiohttp
import json
from discord.ext import commands
import asyncio
import datetime
import random



TOKEN = "SERVER TOKEN"
client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("Bot is ready.")



def __datetime(date_str):
    return datetime.datetime.strptime(date_str, '%H:%M:%S')


async def background_task():
    await client.wait_until_ready()

    channel = client.get_channel(808735710127456310) # Insert channel ID here



    url = 'https://type.fit/api/quotes'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)


    while not client.is_closed():

        embed = discord.Embed(
            description = "Good morning, folks!🔅 Let us get started to grind and shine!✨✨✨\n *P.S. drink water and wear your socks.*",
            timestamp = datetime.datetime.utcnow(),
            color = 0x85e5df
        )
        embed.set_author(name='Message for the Koders')
        embed.add_field(name = "Before we kick off, let's have a thought", value = random.choice(response)['text'], inline = False)
        embed.set_footer(text="Made with ❤️️  by Koders", icon_url="https://cdn.discordapp.com/attachments/810745082537050112/811894457392824331/K_NEW_CIRCLE.png")

        embed2 = discord.Embed(
            description = "Work hard in silence and at your home being socially distant! **But do not forget to log your work** that can make the noise of your work. Log your work, okay?\n *P.S. drink water and wear your socks.*",
            timestamp = datetime.datetime.utcnow(),
            color = 0x85e5df
        )
        embed2.set_author(name='Message for the Koders')
        embed2.set_footer(text="Made with ❤️️  by Koders", icon_url="https://cdn.discordapp.com/attachments/810745082537050112/811894457392824331/K_NEW_CIRCLE.png")

        embed3 = discord.Embed(
            description = "Aye hey, it is your time to take a break 😄. Communication is the key, Remember?\nDo not forget to attend the meeting tonight. Let’s have some fun. You did great this week. We are proud of you. **#ItIsFriyay** 🥳🥳🥳.\n*P.S. drink water and wear your socks.*",
            timestamp = datetime.datetime.utcnow(),
            color = 0x85e5df
        )
        embed3.set_author(name='Message for the Koders')
        embed3.set_footer(text="Made with ❤️️  by Koders", icon_url="https://cdn.discordapp.com/attachments/810745082537050112/811894457392824331/K_NEW_CIRCLE.png")


        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S")
        current_day = now.strftime("%A")
        set_time1 = "11:00:00"
        set_time2 = "20:00:00"
        start1 = __datetime(current_time)
        end1 = __datetime(set_time1)
        end2 = __datetime(set_time2)
        delta1 = end1 - start1
        delta2 = end2 - start1
        delay1 = delta1.total_seconds()
        delay2 = delta2.total_seconds()

        while current_time != set_time1:
            if delay1 > 0:
                await asyncio.sleep(delay1)
                await channel.send(embed=embed)
            break

        while current_time != set_time2:
            if delay2 > 0 and current_day == "Friday":
                await asyncio.sleep(delay2)
                await channel.send(embed=embed3)
            elif delay2 > 0:
                await asyncio.sleep(delay2)
                await channel.send(embed=embed2)
            break


client.loop.create_task(background_task())

client.run(TOKEN)
