import discord
from discord.ext import commands
import os
from discord.ext.commands import MissingRole
import secrets
import json
import asyncio
from dotenv import load_dotenv

intents = discord.Intents.all()

load_dotenv()

client = commands.Bot(command_prefix="*", intents=intents)

TOKEN = os.getenv("BOT_TOKEN")

@client.event
async def on_ready():
  print("I am alive")

@client.event
async def on_member_join(member):
  if member.guild.id == 945254273640443904:
    channel = client.get_channel(946769906488188928)
    embed = discord.Embed(title="New Member Joined", description="", color=discord.Color.green())
    embed.add_field(name=f"Welcome {member.name} to the server.", value=f"{member.name} thanks for joining {member.guild.name}. Hope you enjoy your stay here.")
    embed.set_thumbnail(url=member.avatar.url)
    await channel.send(embed=embed)
    if member.bot == True:
      role = discord.utils.get(member.guild.roles, name="Waiting")
      await member.add_roles(role)
      print("Added role '" + role.name + "' to " + member.name)
    else:
      role = discord.utils.get(member.guild.roles, name="Members")
      await member.add_roles(role)
      print("Added role '" + role.name + "' to " + member.name)

@client.event
async def on_member_remove(member):
  if member.guild.id == 945254273640443904:
    if member.bot == False:
      channel = client.get_channel(946769906488188928)
      embed = discord.Embed(title="Member Left", description="", color=discord.Color.red())
      embed.add_field(name=f"{member.name} left to the server.", value=f"Sad {member.name} left us. Hope you come back soon.")
      embed.set_thumbnail(url=member.avatar_url)
      await channel.send(embed=embed)
  with open("addbot.json", "r") as addbot_json:
    addbot_file = json.load(addbot_json)
  member_id = member.id
  for mumba_jumba in addbot_file:
    if str(member_id) in mumba_jumba:
      for gulab_jamun in addbot_file[mumba_jumba]:
        try:
          print(gulab_jamun)
          bot = await member.guild.fetch_member(int(gulab_jamun))
          print(bot)
          await bot.kick(reason="Owner left")
          print(f"Chicken roll {bot.name}")
          channel = client.get_channel(946769906488188928)
          emb = discord.Embed(title=f"{bot.name} kicked from the server.", description="Owner left the server.")
          await channel.send(embed=emb)
        except:
          continue

async def get_addbots_file():
  with open("addbot.json", "r") as f:
    addbots = json.load(f)
    return addbots

@client.slash_command()
async def addbot(ctx, botid, *, prefix):
  addbots = await get_addbots_file()
  if ctx.channel.id == 945384612002144377:
    user = await client.fetch_user(botid)
    if user.bot == False:
      await ctx.respond("This isn't a bot")
    else:
      for key, value in addbots.items():
        if str(botid) in value:
          await ctx.respond("This bot is already in the server.")
          break
        else:
          accepted_rejected_json_file = await get_accepted_rejected_file()
          for key, value in list(addbots.items()):
            if str(botid) in key:
              await ctx.respond(f"The bot is already {accepted_rejected_json_file['type']}")
              return
            else:
              if str(ctx.author.id) not in key:
                addbots[str(ctx.author.id)] = []        
                addbots[str(ctx.author.id)].append(botid)
                with open("addbot.json", "w") as f:
                  json.dump(addbots,f)
              else:
                addbots[str(ctx.author.id)].append(botid)
                with open("addbot.json", "w") as f:
                  json.dump(addbots,f)
                break
          with open("addbot.json", "w") as f:
            json.dump(addbots,f)
          embed = discord.Embed(title=f"{ctx.author.name}", description="", color=discord.Color.green())
          embed.add_field(name="Prefix:", value=f"`{prefix}`")
          embed.add_field(name="ID:", value=f"`{botid}`", inline=False)
          embed.add_field(name="Name:", value=f"`{user}`")
          embed.set_footer(text="Note:\nIf you have provided any incorrect information while submitting your bot then your bot will be rejected and kicked from the server.")
          await ctx.respond(embed=embed)
          channel = client.get_channel(945634829217722378)
          emb = discord.Embed(title=f"{ctx.author.name} Submitted a new bot", description="", color=0xf8ff00)
          emb.add_field(name="Name:", value=f"{user}")
          emb.add_field(name="ID:", value=f"{botid}", inline=False)
          emb.add_field(name="Prefix:", value=prefix, inline=False)
          emb.add_field(name="Bot Invite", value=f"[Invite Link](https://discord.com/oauth2/authorize?client_id={botid}&permissions=0&scope=bot%20applications.commands&enable_guild_select=true&guild_id=945254273640443904)", inline=False)
          emb.set_author(name="New Bot", icon_url=ctx.author.avatar.url)
          emb.set_thumbnail(url=user.avatar.url)
          await channel.send("<@946856481087705099>", embed=emb)
          break
  else:
    await ctx.respond("❌ Go to <#945384612002144377> to add your bot")

async def get_accepted_rejected_file():
  with open("accepted_rejected.json", "r") as file:
    accepted_rejected_file = json.load(file)
  return accepted_rejected_file

@client.slash_command()
@commands.has_any_role("Staff")
async def accept(ctx, botid):
  channel = client.get_channel(945384634060001320)
  users = await ctx.guild.fetch_member(botid)
  with open('addbot.json', 'r') as r:
    addbote = json.load(r)
  for key, value in addbote.items():
    if str(botid) in value:
      embed = discord.Embed(title="Bot Reviewed", description="", color=discord.Color.green())
      embed.add_field(name="Your bot was reviewed by:", value=f"{ctx.author.mention} `[{ctx.author.name}#{ctx.author.discriminator}]`")
      embed.add_field(name="Bot Information:", value="Bot information are as follows", inline=False)
      embed.add_field(name="Tag:", value=users)
      embed.add_field(name="ID:", value=botid, inline=False)
      embed.add_field(name="Username:", value=users.name, inline=False)
      embed.add_field(name="Results:", value="The bot is accepted", inline=False)
      accepted_rejected_file = await get_accepted_rejected_file()
      print("Above for loop")
      for bot_ids, types in accepted_rejected_file.items():
        print("Entered for loop")
        if str(botid) in bot_ids:
          await ctx.respond(f"This bot is already {accepted_rejected_file[str(botid)]['type']}")
          return
        else:
          print("in else")
          continue
      print(types)
      accepted_rejected_file[str(botid)] = {}
      accepted_rejected_file[str(botid)]["type"] = "accepted"
      with open("accepted_rejected.json", "w") as accepted_rejeceted_json:
        json.dump(accepted_rejected_file, accepted_rejeceted_json)
      await channel.send(f"<@{key}>", embed=embed)
      await ctx.respond(f"Bot `{users}` accepted by {ctx.author.name}")
      botlar_role = discord.utils.get(ctx.guild.roles, name="BOTLAR")
      waiting_role = discord.utils.get(ctx.guild.roles, name="Waiting")
      developer_role = discord.utils.get(ctx.guild.roles, name="Bot Developers")
      print(developer_role.id)
      await users.add_roles(botlar_role)
      await users.remove_roles(waiting_role)
      member_to_send = await ctx.guild.fetch_member(int(key))
      await member_to_send.add_roles(developer_role)
      try:
        await member_to_send.send(f"Your bot, {users} has been accepted in {ctx.guild.name}")
      except:
        await ctx.respond("Couldn't dm {}".format(member_to_send))
      return      
  await ctx.respond("This bot ID is not stored in the database. Ask the botowner to add the bot first then try to use this command.")
  return
      
@accept.error
async def accept_error(ctx, error):
  if isinstance(error, MissingRole):
    await ctx.reply("You cannot execute this command. You need Bot reviewers role to execute this command.")

@client.slash_command()
@commands.has_any_role("Staff")
async def reject(ctx, botid, *, reason):
  channel = client.get_channel(945384634060001320)
  userss = await client.fetch_user(int(botid))
  with open('addbot.json', 'r') as r:
    addbotee = json.load(r)
  for key, value in addbotee.items():
    if str(botid) in value:
      addbotee[key].remove(str(botid))
      with open("addbot.json", "w") as addbot_file:
        json.dump(addbotee, addbot_file)
      embed = discord.Embed(title="Bot Reviewed", description="", color=discord.Color.red())
      embed.add_field(name="Your bot was reviewed by:", value=f"{ctx.author.mention} `[{ctx.author.name}#{ctx.author.discriminator}]`")
      embed.add_field(name="Bot Information:", value="Bot information are as follows", inline=False)
      embed.add_field(name="Tag:", value=userss)
      embed.add_field(name="ID:", value=botid, inline=False)
      embed.add_field(name="Username:", value=userss.name, inline=False)
      embed.add_field(name="Results:", value="The bot is rejected", inline=False)
      embed.add_field(name="Reason:", value=reason)
      accepted_rejected_file = await get_accepted_rejected_file()
      print("Above for loop")
      for bot_ids, types in accepted_rejected_file.items():
        print("Entered for loop")
        if str(botid) in bot_ids:
          await ctx.respond(f"This bot is already {accepted_rejected_file[str(botid)]['type']}")
          return
        else:
          print("in else")
          continue
      # for author_id, bot_id in addbotee.items():
      #   for peg in bot_id:
      #     if peg == str(botid):
      #       addbo
      print(types)
      accepted_rejected_file[str(botid)] = {}
      accepted_rejected_file[str(botid)]["type"] = "rejected"
      with open("accepted_rejected.json", "w") as accepted_rejeceted_json:
        json.dump(accepted_rejected_file, accepted_rejeceted_json)
      await channel.send(f"<@{key}>", embed=embed)
      await ctx.respond(f"Bot `{userss}` rejected by {ctx.author.name}")
      Bot = await ctx.guild.fetch_member(botid)
      await Bot.kick(reason="Bot rejected")
      member_to_send = await client.fetch_user(int(key))
      try:
        await member_to_send.send(f"Your bot, {userss} has been declined. Reason: {reason}")
      except:
          await ctx.respond("Couldn't dm {}".format(member_to_send))
          return      
  await ctx.respond("This bot ID is not stored in the database. Ask the botowner to add the bot first then try to use this command.")
  return

@client.event
async def on_message(message):
  if message.guild.id == 945254273640443904:
    if message.channel.id == 961253252748431430:
      return
    if message.channel.id == 961253409770602506:
      return
    if message.author.bot == False:  
      channel = client.get_channel(1010900884596740176)
      await channel.send(f"{message.author.name} ({message.author.id}) has sent in {message.channel.name} ({message.channel.id})")
      embed = discord.Embed(title=message.content, description="", color=discord.Color.blue())
      await channel.send(embed=embed)
    if message.author.id == 939739460407558215:
      return
    if message.channel.id == 1010900884596740176:
      return
  await client.process_commands(message)
  
client.run(TOKEN)