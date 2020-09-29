import discord
import json
import random
import time
import asyncio
import requests
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands.cooldowns import BucketType
from requests.exceptions import HTTPError

TOKEN = 'NzQxNjE5MDA2NjQ1MjA3MDQw.Xy6MhQ.853Js8TYIzx4c1c-Iz5Z4mwWEw4'

def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix, help_command = None)

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '!'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

@client.event
async def on_member_join(member):
    channel = client.get_channel(755769687651909703)
    members = member.guild.member_count
    embed = discord.Embed(title='**Welcome To Signature Doms Community Discord**', description=f'{member.mention} Please read the <#743830128274047057> \nYou are member number {members-1} \n **Time Of Joining** \n {member.joined_at.strftime("%A %d. %B %Y")}', color = discord.Colour.dark_gold()) # or any other color
    role = discord.utils.get(member.guild.roles, name='Unverified')
    await member.add_roles(role)
    await channel.send(embed=embed)

@client.event
async def on_member_remove(member):
    channel = client.get_channel(755430098454446271)
    await channel.send(f'{member.mention} Has left the server.')

async def tez():
    while True:
        print('This is a simple message sent every 15 minutes to keep the bot online.')
        await asyncio.sleep(900)

async def membersyes():
    while True:
        vchannel = client.get_channel(755445385366863962)
        guild = client.get_guild(735050902590849049)
        members = guild.member_count
        await vchannel.edit(name=f'Member Count: {members-1}')
        await asyncio.sleep(15)



@client.event #startup
async def on_ready():
    print('Bot Is Ready')
    await client.change_presence(activity=discord.Streaming(name="Waiting For !Help", url='https://www.twitch.tv/gamergirlbathwater2281'))
    vchannel = client.get_channel(755445385366863962)
    await vchannel.connect(reconnect=True)
    asyncio.create_task(tez())
    asyncio.create_task(avataredit())
    asyncio.create_task(membersyes())

@client.event
async def on_message(message):
    if message.channel.id == 752517536540524554:
        if not message.author.bot:
            a = message.content
            b = message.author
            embed = discord.Embed(title='**Suggestion**', description=a, color = discord.Colour.dark_gold()) # or any other color
            embed.set_footer(text=f"From: {b}.")
            await message.channel.purge(limit=1)
            c = await message.channel.send(embed=embed)
            await c.add_reaction("✅")
            await c.add_reaction("❌")
    if message.channel.id == 737311554571337780:

        if message.content != '!verify':
            await message.delete()

        await message.delete()
        role = discord.utils.get(message.guild.roles, name='Unverified')
        mrole = discord.utils.get(message.guild.roles, name='Member')
        await message.author.add_roles(mrole)
        await message.author.remove_roles(role)
        print('verify yes')
    await client.process_commands(message)

@client.command()
async def membercount(ctx):
    members = ctx.guild.member_count
    embed = discord.Embed(title='Member Count', description=f'There are **{members-1}** members in this guild')
    await ctx.send(embed=embed)

@client.command()
@commands.has_any_role('Moderator','Administrator','Founder')
async def say(ctx, value):
    await ctx.message.delete()
    await ctx.send(value)

@client.command()
@commands.has_any_role('Moderator','Administrator','Founder')
async def shut(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('shut.png'))

@client.command()
@commands.has_any_role('Moderator','Administrator','Founder')
async def nobodyasked(ctx):
    await ctx.message.delete()
    await ctx.send(file=discord.File('nobodyasked.mp4'))

@client.command()
async def gay(ctx, member : discord.Member = None):
    number = random.randint(1, 100)
    if member == None:
        embed = discord.Embed(title=f'**{ctx.author.name} is {number}% gay!**', color = discord.Colour.dark_gold()) # or any other color
    else:
        embed = discord.Embed(title=f'**{member.name} is {number}% gay!**', color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)

@client.command()
async def horny(ctx, member : discord.Member = None):
    number = random.randint(1, 100)
    if member == None:
        embed = discord.Embed(title=f'💦 **{ctx.author.name} is {number}% horny!**', color = discord.Colour.dark_gold()) # or any other color
    else:
        embed = discord.Embed(title=f'💦 **{member.name} is {number}% horny!**', color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)

@client.command()
async def minecraft(ctx, *, message):

    if len(message) > 36:
        return await bot.say('I can only handle achievements up to 36 letters!')
    img = Image.open("achievement.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("Minecraft.ttf", 14)
    draw.text((60, 32), f"{message}", (255, 255, 255), font=font)
    img.save('achievement2.png')
    await ctx.send(file=discord.File('achievement2.png'))
    if commands.bot_has_permissions(manage_messages=True):
        await client.delete_message(ctx.message)

@client.command()
async def apply(ctx):
    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(
    read_messages=False,
    send_messages=False
    ),
    ctx.author: discord.PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    view_channel=True
    )
  }
    with open("application_log.txt", "a") as f:
        category = client.get_channel(741983757682212914)
        channel = await category.create_text_channel(name=f'Application-{ctx.author.name}', overwrites=overwrites)
        embed = discord.Embed(title='**Application Created**', description=f'Your application has been created at <#{channel.id}>', color = discord.Colour.dark_gold()) # or any other color
        await ctx.send(embed=embed)
        await channel.send('What is your name?')
        name = await client.wait_for('message')
        await channel.send('How old are you?')
        age = await client.wait_for('message')
        await channel.send('In what time zone do you live in?')
        tz = await client.wait_for('message')
        await channel.send('How often will you be online?')
        oa = await client.wait_for('message')
        await channel.send('Why do you want to become a moderator?')
        why = await client.wait_for('message')
        await channel.send('Why do you think you should be picked compared to anyone else?')
        wy = await client.wait_for('message')
        await channel.send('What languages can you speak?')
        lang = await client.wait_for('message')
        f.write(f'What is your name? \n')
        f.write(f'{name.author} : {name.content} \n')
        f.write(f'How old are you \n')
        f.write(f'{age.author} : {age.content} \n')
        f.write(f'In what time zone do you live in? \n')
        f.write(f'{tz.author} : {tz.content} \n')
        f.write(f'How often will you be online? \n')
        f.write(f'{oa.author} : {oa.content} \n')
        f.write(f'Why do you want to become a moderator? \n')
        f.write(f'{why.author} : {why.content} \n')
        f.write(f'Why do you think you should be picked compared to anyone else? \n')
        f.write(f'{wy.author} : {wy.content} \n')
        f.write(f'What languages can you speak? \n')
        f.write(f'{lang.author} : {lang.content} \n')
        transcripts = client.get_channel(755429905713332375)
    await transcripts.send(f'New application by {ctx.author.name}', file=discord.File('application_log.txt'))
    await channel.delete()
    with open("application_log.txt", "w") as f:
        f.write(f'')

@client.command()
async def close(ctx):
    if ctx.channel.name.startswith("ticket-"):
        messages = await ctx.channel.history(limit=None, oldest_first=True).flatten()
        transcripts = client.get_channel(755429905713332375)

        for message in messages:
            with open("ticket_log.txt", "a") as f:
                f.write(f'{message.author} : {message.content} \n')
        await transcripts.send(f'New Transcript closed by {ctx.author.name}', file=discord.File('ticket_log.txt'))
        with open("ticket_log.txt", "w") as f:
            f.write(f'')

        await  ctx.channel.delete()
    else:
        await ctx.send('Please run command in a ticket.')

@client.command()
async def new(ctx):
    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(
    read_messages=False,
    send_messages=False
    ),
    ctx.author: discord.PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    view_channel=True
    )
  }
    category = client.get_channel(741983757682212914)
    channel = await category.create_text_channel(name=f'Ticket-{ctx.author.name}', overwrites=overwrites)
    embed = discord.Embed(title='**Application Created**', description=f'Your ticket has been created at <#{channel.id}>', color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)

@client.command()
@commands.has_any_role('Administrator','Founder')
async def lock(ctx):
    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(
    read_messages=False,
    send_messages=False
    ),
    ctx.guild.get_role(735413955865870346): discord.PermissionOverwrite(
    read_messages=True,
    send_messages=False,
    ),
    ctx.guild.get_role(743846545451122788): discord.PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    ),
    ctx.guild.get_role(748476765718184009): discord.PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    ),
    ctx.guild.get_role(735413844511424573): discord.PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    ),
  }
    await ctx.channel.edit(overwrites=overwrites)
    embed = discord.Embed(title='🔒 **Channel Locked**', description=f"*Members can no longer talk in this channel.*", color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)

@client.command()
@commands.has_any_role('Administrator','Founder')
async def unlock(ctx):
    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(
    read_messages=False,
    send_messages=False
    ),
    ctx.guild.get_role(735413955865870346): discord.PermissionOverwrite(
    read_messages=True,
    send_messages=True,
    )
    }
    await ctx.channel.edit(overwrites=overwrites)
    embed = discord.Embed(title='🔓 **Channel Unlocked**', description=f"*Members can now talk in this channel.*", color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    embed = discord.Embed(title='⬆ **Ping**', description=f"Ping = **{round(client.latency * 1000)}ms**", color = discord.Colour.dark_gold()) # or any other color
    embed.set_footer(text=f"{ctx.author.name} ran this command.")
    await ctx.send(embed=embed)
    print(f'{ctx.author} Used Ping')

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responces = ['It is certain.',
                 'As I see it, yes.',
                 'It is decidedly so.',
                 'Most likely.',
                 'Outlook good.',
                 'Without a doubt.',
                 'Yes – definitely.',
                 'You may rely on it.',
                 'Signs point to yes.',
                 'Yes.',
                 'Reply hazy, try again.',
                 'Ask again later.',
                 'Better not tell you now.',
                 'Cannot predict now.',
                 'Concentrate and ask again',
                 "Don't count on it.",
                 'My reply is no.',
                 'My sources say no.',
                 'Outlook not so good.',
                 'Very doubtful.']
    embed = discord.Embed(title='🎱 8ball', description=f"Question: {question}. \n Responce: {random.choice(responces)}", color = discord.Colour.dark_gold()) # or any other color
    embed.set_footer(text=f"{ctx.author.name} ran this command.")
    await ctx.send(embed=embed)

@client.command()
@commands.is_owner()
async def setstatus(ctx, a=None):
    if a == None:
        embed = discord.Embed(title='👀 Status', description=f"Invalid status, Please use **\n online🟢, \n green🟢, \n idle🟠, \n yellow🟠, \n dnd🔴, \n red🔴, \n offline⚫, \n invisible⚫, \n grey⚫.**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'online':
        await client.change_presence(status=discord.Status.online)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to **🟢 : Online**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'idle':
        await client.change_presence(status=discord.Status.idle)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to **🟠 : Idle**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'dnd':
        await client.change_presence(status=discord.Status.dnd)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to **🔴 : Do Not Disturb**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'offline':
        await client.change_presence(status=discord.Status.invisible)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to **⚫ : Invisible**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'invisible':
        await client.change_presence(status=discord.Status.invisible)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to ⚫ : Invisible**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'grey':
        await client.change_presence(status=discord.Status.invisible)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to ⚫ : Invisible**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'green':
        await client.change_presence(status=discord.Status.online)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to **🟢 : Online**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'red':
        await client.change_presence(status=discord.Status.dnd)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to **🔴 : Do Not Disturb**", color = discord.Colour.dark_gold()) # or any other color
    elif a == 'yellow':
        await client.change_presence(status=discord.Status.idle)
        embed = discord.Embed(title='👀 Status', description=f"Changed bots status to **🟠 : Idle**", color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)

@client.command() #purge
@commands.has_any_role('Moderator','Administrator','Founder','Owner','Admin','Mod')
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    embed = discord.Embed(title='⚡ Purge', description=f"Purged **{amount}** messages", color = discord.Colour.dark_gold()) # or any other color
    print(f'{ctx.author} Used Purge')
    embed.set_footer(text=f"{ctx.author.name} ran this command.")
    await ctx.send(embed=embed)

@client.command() #purge
@commands.has_any_role('Moderator','Administrator','Founder')
async def nuke(ctx):
    await ctx.channel.purge(limit=10000000)
    embed = discord.Embed(title='<a:nuke:748531712497025055> **Nuke**', description=f"**Nuked The Channel**", color = discord.Colour.dark_gold()) # or any other color
    print(f'{ctx.author} Used Nuke')
    embed.set_footer(text=f"{ctx.author.name} ran this command.")
    await ctx.send(embed=embed)

@client.command()
async def coinflip(ctx):
    responses = ['Heads.',
                 'Tails.']
    embed = discord.Embed(title='🔁 Coin Flipped', description=f"The Coin Was Flipped, It Landed On **{random.choice(responses)}**", color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)
    embed.set_footer(text=f"{ctx.author.name} ran this command.")
    print(f'{ctx.author} Used Coin Flip')

@client.command()
async def rolldice(ctx):
    responces = ['1','2','3','4','5','6']
    embed = discord.Embed(title='🎲 Dice Rolled', description=f"The dice was rolled, it landed on **{random.choice(responces)}**", color = discord.Colour.dark_gold()) # or any other color
    embed.set_footer(text=f"{ctx.author.name} ran this command.")
    await ctx.send(embed=embed)



@client.command()#help
async def help(ctx):
    embed = discord.Embed(title='📢 HELP MENU', description=f"🙂 **General** \n **!help** - View the command help menu\n 🎟 **Tickets**\n **!apply** - Create an application\n **!close** - Close the ticket you are typing in \n **!new** - Create a ticket\n🎮 **Fun** \n **!kiss** - Give someone a kiss\n**!8ball** - Ask the magical 8 ball a question and get an answer\n**!coinflip** - Flip a coin \n**!rockpaperscissors** - Rock paper scissors game\n**!rolldice** - Roll a dice \n**!gay** - Measure how gay someone is \n**!horny** - Measure how horny someone is\n🎨 **Other**\n**!avatar** - check someones avatar\n**!info** - View a user info \n **!ping** - Check bots latency\n <:blobhyperthink:743833140451082372> **NSFW** \n **!sauce** - generate some nhentai sauce \n **!hentai** - send some hentai", color = discord.Colour.dark_gold()) # or any other
    embed.set_footer(text=f"The Default Server Prefix Is !, and {ctx.author.name} ran this command.")
    await ctx.send(embed=embed)
    print(f'{ctx.author} Used Help')

@client.command()
@commands.has_any_role('Junior Mod','Moderator','Administrator','Founder')
async def shelp(ctx):
    embed = discord.Embed(title='Staff Help Menu', description=f"👮‍♂️ **Moderation** \n **!ban** - Ban a member of the server. \n **!purge** - Clear a certain amount of messages \n **!kick** - Kick a user in the Discord server \n **!lock** - Lock the channel so users cannot send messages \n **!mute** - Mute a user in the Discord server \n **!tempban** - Temporarily ban a user on the Discord server \n  **!tempmute** - Temporarily mute a user on the Discord server \n **!unban** - Unban a user on the Discord server \n **!unlock** - Unlock the channel you are typing in \n **!unmute** - Unmute a user on the Discord server \n 🖥 **Management** \n **!setprefix** - Set the bot's prefix \n **!setstatus** - Set the bot's status \n👀 **Trolling** \n **!shut** - Shut someone up \n **!nobodyasked** - Nobody asked\n **!say** - Make bot say something", color = discord.Colour.dark_gold()) # or any other
    await ctx.send(embed=embed)

@client.command()
@commands.has_any_role('Administrator')
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    embed = discord.Embed(title='🛠PREFIX CHANGE', description=f'The Prefix is now **{prefix}**', color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)

@client.command()
async def kiss(ctx, x : discord.Member=None):
    if x == None:
        f = f"{ctx.author.mention} Kisses himself."
    else:
        f = f"{ctx.author.mention} Kisses {x.mention}."
    response = requests.get(f'https://nekos.life/api/kiss')
    embed = discord.Embed(description=f)
    embed.set_image(url=response.json()["url"])
    await ctx.send(embed=embed)

@client.command()
async def hentai(ctx, type=None):
    if ctx.channel.nsfw == True:
        if type == None:
            emb = discord.Embed(title='<a:verify_white:746008789895086123> Incorrect Formating', description=f"Please use a proper type, our current types are **pussy**, **neko**, **lesbian**, **cumsluts**, **classic**, **boobs**, **anal**, **yuri**, **trap**, **tits**, **hentai**, **futanari**, **femdom**, **feet**, **ero**, **cumArts**, **blowJob**, **spank**, And **gasm**", color = discord.Colour.dark_gold()) # or any other color
            await ctx.send(embed=emb)
        elif type == 'pussy':
            ep = "/img/pussy"
        elif type == 'neko':
            ep = "/img/lewd"
        elif type == 'lesbian':
            ep = "/img/les"
        elif type == 'cumsluts':
            ep = "/img/cum"
        elif type == 'classic':
            ep = "/img/classic"
        elif type == 'boobs':
            ep = "/img/boobs"
        elif type == 'anal':
            ep = "/img/anal"
        elif type == 'yuri':
            ep = "/img/yuri"
        elif type == 'trap':
            ep = "/img/trap"
        elif type == 'tits':
            ep = "/img/tits"
        elif type == 'futanari':
            ep = "/img/futanari"
        elif type == 'femdom':
            ep = "/img/femdom"
        elif type == 'feet':
            ep = "/img/feet"
        elif type == 'ero':
            ep = "/img/ero"
        elif type == 'cumarts':
            ep = "/img/cum_jpg"
        elif type == 'blowjob':
            ep = "/img/blowjob"
        elif type == 'spank':
            ep = "/img/spank"
        elif type == 'gasm':
            ep = "/img/gasm"
        else:
            ep = "img/hentai"

        response = requests.get(f'https://nekos.life/api/v2{ep}')
        embed = discord.Embed()
        embed.set_image(url=response.json()["url"])
        await ctx.send(embed=embed)


    else:
        ebed = discord.Embed(title='<a:Eor:744501627901181982> Wrong Channel', description=f"Please do command in a **NSFW** channel", color = discord.Colour.dark_gold()) # or any other color
        await ctx.send(embed=ebed)

@client.command()
async def avatar(ctx, member : discord.Member=None):
    embed = discord.Embed()
    if member == None:
        embed.set_image(url=f'')
    else:
        embed.set_image(url=f'{member.avatar_url}')
    await ctx.send(embed=embed)

@client.command()
async def sauce(ctx, type=None, *, g=None):
    if ctx.channel.nsfw == True:

        number = random.randint(1, 327013)
        sauce = ['218734','201583','295362','191039','144393','313044','153006','260606','184654','161400','105279','253846','255622','94864','326785','272422','275098','100713','132339']
        top = ['98150']
        saucenum = random.choice(sauce)
        topnum = random.choice(top)
        amount = len(sauce)
        emount = len(top)
        if type == None:
            embed = discord.Embed(title='<a:verify_white:746008789895086123> Sauce', description=f"Incorrect format, please use **!sauce working** , **!sauce approved** or **!sauce top**", color = discord.Colour.dark_gold()) # or any other color
            await ctx.send(embed=embed)
        elif type == 'tag':
            bigbreasts = ["None"]
            stockings = ["None"]
            anal = ["None"]
            incest = ["None"]
            bigass = ["None"]
            loli = ["None"]
            tenticles = ["None"]
            blowjob = ["None"]
            milf = ["None"]
            if g == None:
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Incorrect Formating', description=f"Please use a proper tag, our current tags are **oppai**, **stockings**, **anal**, **incest**, **big ass**, **loli**, **tenticles**, **blowjob**, And **milf**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'oppai':
                yes = random.choice(bigbreasts)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Oppai', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'stockings':
                yes = random.choice(stockings)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Stockings', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'anal':
                yes = random.choice(anal)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Anal', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'incest':
                yes = random.choice(incest)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Incest', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'big ass':
                yes = random.choice(bigass)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Big ass', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'loli':
                yes = random.choice(loli)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Loli', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'tenticles':
                yes = random.choice(tenticles)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Tenticles', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'blowjob':
                yes = random.choice(blowjob)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Blowjob', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            elif g == 'milf':
                yes = random.choice(milf)
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Milf', description=f"Found some sauce in our list : **[{yes}](https://nhentai.net/g/{yes})**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title='<a:verify_white:746008789895086123> Incorrect Formating', description=f"Please use a proper tag, our current tags are **oppai**, **stockings**,**anal**, **incest**,**big ass**, **loli**,**tenticles**, **blowjob**, And **milf**", color = discord.Colour.dark_gold()) # or any other color
                await ctx.send(embed=embed)


        elif type == 'random':
            embed = discord.Embed(title='<a:verify_white:746008789895086123> Sauce Generated', description=f"Some sauce was generated : **[{number}](https://nhentai.net/g/{number}/)**", color = discord.Colour.dark_gold()) # or any other color
            embed.set_footer(text=f"{ctx.author.name} Requested this, Some numbers will not work. If you find a working one, please send to owner.")
            await ctx.send(embed=embed)
        elif type == 'approved':
            embed = discord.Embed(title='<a:verify_white:746008789895086123> Sasha Approved Sauce', description=f"Found some sauce in our list : **[{saucenum}](https://nhentai.net/g/{saucenum})**", color = discord.Colour.dark_gold()) # or any other color
            embed.set_footer(text=f"{ctx.author.name} Requested this, {amount} in stock.")
            await ctx.send(embed=embed)
        elif type == 'top':
            embed = discord.Embed(title='<a:verify_white:746008789895086123> Friend Favourites', description=f"Found some sauce in our list : **[{topnum}](https://nhentai.net/g/{topnum})**", color = discord.Colour.dark_gold()) # or any other color
            embed.set_footer(text=f"{ctx.author.name} Requested this, {emount} in stock.")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title='<a:verify_white:746008789895086123> Sauce', description=f"Incorrect format, please use **!sauce working** , **!sauce approved** or **!sauce top**", color = discord.Colour.dark_gold()) # or any other color
            await ctx.send(embed=embed)
    else:
        ebed = discord.Embed(title='<a:Eor:744501627901181982> Wrong Channel', description=f"Please do command in a **NSFW** channel", color = discord.Colour.dark_gold()) # or any other color
        await ctx.send(embed=ebed)

@client.command()
@commands.has_any_role('Administrator','Founder')
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)
    embed = discord.Embed(title='🛠 **Kick**', description=f"Successfully kicked {member} for {reason}", color = discord.Colour.dark_gold()) # or any other color
    logs = discord.Embed(title='🛠 **Kick**', description=f"{ctx.author} has kicked {member} for {reason}", color = discord.Colour.dark_gold()) # or any other color
    channel = client.get_channel(755430148102422710)
    await ctx.send(embed=embed)
    await channel.send(embed=logs)

@client.command()
@commands.has_any_role('Administrator','Founder')
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason=reason)
    embed = discord.Embed(title='🛠 **Ban**', description=f"Successfully banned {member} for {reason}", color = discord.Colour.dark_gold()) # or any other color
    logs = discord.Embed(title='🛠 **Ban**', description=f"{ctx.author} has banned {member} for {reason}", color = discord.Colour.dark_gold()) # or any other color
    channel = client.get_channel(755430148102422710)
    await ctx.send(embed=embed)
    await channel.send(embed=logs)

@client.command()
@commands.has_any_role('Administrator','Founder')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned ')
            embed = discord.Embed(title='🛠 **Unban**', description=f"Successfully unbanned {user.name}#{user.discriminator}", color = discord.Colour.dark_gold()) # or any other color
            logs = discord.Embed(title='🛠 **Unban**', description=f"{ctx.author} has unbanned {user.name}#{user.discriminator}", color = discord.Colour.dark_gold()) # or any other color
            channel = client.get_channel(755430148102422710)
            await ctx.send(embed=embed)
            await channel.send(embed=logs)
            return

@client.command()
@commands.has_any_role('Moderator','Administrator','Founder')
async def mute(ctx, member : discord.Member, *, reason = None ):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    mrole = discord.utils.get(ctx.guild.roles, name='Member')
    await member.add_roles(role)
    await member.remove_roles(mrole)
    embed = discord.Embed(title='🛠 **Mute**', description=f"Successfully muted {member} for {reason}", color = discord.Colour.dark_gold()) # or any other color
    logs = discord.Embed(title='🛠 **Mute**', description=f"{ctx.author} has Muted {member} for {reason}", color = discord.Colour.dark_gold()) # or any other color
    channel = client.get_channel(755430148102422710)
    await ctx.send(embed=embed)
    await channel.send(embed=logs)

@client.command()
@commands.has_any_role('Moderator','Administrator','Founder')
async def unmute(ctx, member : discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    mrole = discord.utils.get(ctx.guild.roles, name='Member')
    await member.add_roles(mrole)
    await member.remove_roles(role)
    embed = discord.Embed(title='🛠 **Unmute**', description=f"Successfully unmuted {member}", color = discord.Colour.dark_gold()) # or any other color
    logs = discord.Embed(title='🛠 **Unmute**', description=f"{ctx.author} has unmuted {member}", color = discord.Colour.dark_gold()) # or any other color
    channel = client.get_channel(755430148102422710)
    await ctx.send(embed=embed)
    await channel.send(embed=logs)

@client.command(aliases=['rps'])
async def rockpaperscissors(ctx, choice = None):
    responces = ['Rock','Paper','Scissors']
    botchoice = random.choice(responces)
    a = None
    b = None
    if choice == None:
        b == 'Error Please use Rock Paper or Scissors'
    if choice == 'rock':
        if botchoice == 'Rock':
            a = 'Draw'
            b = f'You Chose {choice} 🗻, Bot chose {botchoice} 🗻\n It Resulted In a {a}'
        if botchoice == 'Paper':
            a = 'Loss'
            b = f'You Chose {choice} 🗻, Bot chose {botchoice} 📄\n It Resulted In a {a}'
        if botchoice == 'Scissors':
            a = 'Win'
            b = f'You Chose {choice} 🗻, Bot chose {botchoice} ✂️\n It Resulted In a {a}'
    if choice == 'paper':
        if botchoice == 'Rock':
            a = 'Win'
            b = f'You Chose {choice} 📄, Bot chose {botchoice} 🗻\n It Resulted In a {a}'
        if botchoice == 'Paper':
            a = 'Draw'
            b = f'You Chose {choice} 📄, Bot chose {botchoice} 📄 \n It Resulted In a {a}'
        if botchoice == 'Scissors':
            a = 'Loss'
            b = f'You Chose {choice} 📄, Bot chose {botchoice} ✂️\n It Resulted In a {a}'
    if choice == 'scissors':
        if botchoice == 'Rock':
            a = 'Loss'
            b = f'You Chose {choice} ✂️, Bot chose {botchoice} 🗻\n It Resulted In a {a}'
        if botchoice == 'Paper':
            a = 'Win'
            b = f'You Chose {choice} ✂️, Bot chose {botchoice} 📄\n It Resulted In a {a}'
        if botchoice == 'Scissors':
            a = 'Draw'
            b = f'You Chose {choice} ✂️, Bot chose {botchoice} ✂️\n It Resulted In a {a}'

    embed = discord.Embed(title='🗻 **Rock Paper Scissors**', description=f"{b}", color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=embed)

@client.command()
async def info(ctx, member : discord.Member = None):
    embed = discord.Embed(title='❓ **Info**', color = discord.Colour.dark_gold())
    if member == None:
        embed.set_thumbnail(url = f'{ctx.author.avatar_url}')
        embed.add_field(name='ID', value=f'{ctx.author.id}', inline = True)
        embed.add_field(name='Creation Date', value=f'{ctx.author.created_at.strftime("%A %d. %B %Y")}', inline = True)
        embed.add_field(name='Server Join Date', value=f'{ctx.author.joined_at.strftime("%A %d. %B %Y")}', inline = True)
        arole = ""
        a = ""
        for role in ctx.author.roles:
            arole += "\n" + role.mention

        toprole = ""
        for role in ctx.author.roles:
            toprole = "\n" + role.mention

        role = discord.utils.get(ctx.guild.roles, name='Payed Member')
        if role in ctx.author.roles:
            a = "True"
        else:
            a = "False"


        embed.add_field(name='Roles', value=arole, inline = True)
        embed.add_field(name='Top Role', value=toprole, inline = True)
        embed.add_field(name='Payed Member?', value=f"{a}", inline = True)
    else:
        embed.set_thumbnail(url = f'{member.avatar_url}')
        embed.add_field(name='ID', value=f'{member.id}', inline = True)
        embed.add_field(name='Creation Date', value=f'{member.created_at.strftime("%A %d. %B %Y")}', inline = True)
        embed.add_field(name='Server Join Date', value=f'{member.joined_at.strftime("%A %d. %B %Y")}', inline = True)
        mrole = ""
        a = ""
        for role in member.roles:
            mrole += "\n" + role.mention
        toprole = ""
        for role in member.roles:
            toprole = "\n" + role.mention
        role = discord.utils.get(ctx.guild.roles, name='Payed Member')
        if role in member.roles:
            a = "True"
        else:
            a = "False"

        embed.add_field(name='Roles', value=mrole, inline = True)
        embed.add_field(name='Top Role', value=toprole, inline = True)
        embed.add_field(name='Payed Member?', value=f"{a}", inline = True)
    await ctx.send(embed=embed)

@client.command()
async def tempmute(ctx, member : discord.Member, x, *, reason = None ):
    channel = client.get_channel(755430148102422710)
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    mrole = discord.utils.get(ctx.guild.roles, name='Member')
    membed = discord.Embed(title='🛠 **Temporary Mute**', description=f"Successfully muted {member} for {x} minutes", color = discord.Colour.dark_gold()) # or any other color
    mlogs = discord.Embed(title='🛠 **Temporary Mute**', description=f"{ctx.author} has Temp Muted {member} for {x} minutes", color = discord.Colour.dark_gold()) # or any other color
    await member.add_roles(role)
    await member.remove_roles(mrole)
    await ctx.send(embed=membed)
    await channel.send(embed=mlogs)
    time.sleep(int(x) * 60)
    await member.add_roles(mrole)
    await member.remove_roles(role)
    uembed = discord.Embed(title='🛠 **Unmute**', description=f"{member} has been unmuted after being temp muted for {x} minutes", color = discord.Colour.dark_gold()) # or any other color
    ulogs = discord.Embed(title='🛠 **Unmute**', description=f"{member} has been unmuted after being temp muted for {x} minutes", color = discord.Colour.dark_gold()) # or any other color
    await ctx.send(embed=uembed)
    await channel.send(embed=ulogs)

@client.command()
@commands.has_any_role('Moderator','Administrator','Founder')
async def add(ctx, a):
    list = []
    list.append(a)
    print("Yes")

@client.command()
async def serverinfo(ctx):
    embed = discord.Embed()
    mrole = ""
    for role in ctx.guild.roles:
        mrole += "\n" + role.mention
    embed.add_field(name='Roles', value=mrole, inline = True)
    await ctx.send(embed=embed)

client.run(TOKEN)
