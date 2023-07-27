"""
discord_bot.py

sends notifications to discord. sends all new descriptions and titles to one channel.
sends a status update to another channel
"""


from os import getenv 
import discord
import asyncio
from .utils import * 
from .upwork import * 


TOKEN = getenv("DISCORD_TOKEN")
CLIENT = discord.Client(intents=discord.Intents.default())


async def update_db(_, configs):
    """updates the job database and sends an update""" 
    await notify_user(configs, "upwork", update_upwork())
    # TODO: update linkedin jobs
    # discord send linkedin stats
    # TODO: update indeed jobs
    # discord send indeed stats
    # TODO: update glassdoor jobs
    # discord send glassdoor stats


def help(_conf, _message) -> str:
    return "`send \"!update-db\" to update the internal database and get stats.`"


async def _send_gigs(configs, source, gigs):
    """sends the first 10 gigs as one message"""
    await send_stats(configs, source, len(gigs))
    # sep = "---" 
    # msg = f"\n{sep}\n".join([str(gig) for gig in gigs[:10]])
    loc_gigs = [str(gig).replace("\n\n", "\n")[:1750] for gig in gigs]

    channel = CLIENT.get_channel(int(configs.get("discord").get("gigs-channel")))

    for gig in loc_gigs:
        # await channel.send(sep)
        await channel.send(str(gig))


def send_gigs(configs, source, gigs):
    @CLIENT.event
    async def on_ready():
        try:
            await _send_gigs(configs, source, gigs)
        except:
            await CLIENT.close()
        finally:
            await CLIENT.close()
    
    CLIENT.run(TOKEN)
    

async def send_stats(configs, source: str, jobs_found: int):
    """sends a message to the status channel"""
    msg = f"found {jobs_found} {source} gigs"

    channel = CLIENT.get_channel(int(configs.get("discord").get("stats-channel")))
    print("channel", channel)
    await channel.send(msg)


def handle_message(configs, message, user_message) -> [str]:
    """handles incoming messages"""
    p_message = user_message.lower()

    switch = {"!help": help, "!update-db": update_db}
    
    case = switch.get(p_message)

    if case:
        return case(configs, message)


async def send_message(configs, message, user_message):
    try:
        res = handle_response(configs, message, user_message)
        if res:
            await message.channel.send(response)

    except Exception as e:
        print(e)


def entry_point(args, configs): 
    @CLIENT.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @CLIENT.event
    async def on_message(message):
        # Make sure bot doesn't get stuck in an infinite loop
        if message.author != client.user:
            await send_message(configs, message, str(message.content))        

    # Remember to run your bot with your personal TOKEN
    CLIENT.run(TOKEN)
        
