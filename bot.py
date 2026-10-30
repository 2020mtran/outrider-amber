import discord
from discord import app_commands
import re
import os
from config import DISCORD_TOKEN, GUILD_ID, STARTUP_CHANNEL_ID, COMMON_ID, UNCOMMON_ID, RARE_ID, EPIC_ID, LEGENDARY_ID
import asyncio

# Discord Client Initialization
intents = discord.Intents.default()
intents.message_content = True

token = DISCORD_TOKEN
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
fuuka_id = 1230570999833952287
ra_id = 184864181663563776

@client.event
async def on_ready():
    print(f'The Shorekeeper, ready.')

    guild = client.get_guild(int(GUILD_ID))
    if guild is None:
        print(f'Guild with ID {GUILD_ID} not found.')
        return
    
    global wuwaDrop, serverDrop, rareDrop
    wuwaDrop = discord.utils.get(guild.roles, id=int(COMMON_ID))
    serverDrop = discord.utils.get(guild.roles, id=int(UNCOMMON_ID))
    rareDrop = discord.utils.get(guild.roles, id=int(RARE_ID))

    startup_channel = guild.get_channel(int(STARTUP_CHANNEL_ID))
    # if startup_channel:
    #     await startup_channel.send('I`ll fulfill it, be it a direct command or any other wish you have.')

    # Sync the command tree with the guild
    await tree.sync(guild=guild)

@tree.command(name="getrole", description="Assign yourself a drop ping role (wuwa | server | rare).", guild=discord.Object(id=GUILD_ID))
async def get_role(interaction: discord.Interaction, role_name: str):
    role = None

    if role_name.lower() == "wuwa":
        role = wuwaDrop
    elif role_name.lower() == "server":
        role = serverDrop
    elif role_name.lower() == "rare":
        role = rareDrop

    if role:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'You have been assigned the role: {role.name}')
    else:
        await interaction.response.send_message('Role not found. Please use one of the following: (wuwa | server | rare)', ephemeral=True)

@tree.command(name="removerole", description="Remove a role from yourself (wuwa | server | rare)", guild=discord.Object(id=GUILD_ID))
async def remove_role(interaction: discord.Interaction, role_name: str):
    role = None

    if role_name.lower() == "wuwa":
        role = wuwaDrop
    elif role_name.lower() == "server":
        role = serverDrop
    elif role_name.lower() == "rare":
        role = rareDrop

    if role and role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f'The role {role.name} has been removed from you.')
    else:
        await interaction.response.send_message('Role not found or you do not have this role. Please use one of the following: (wuwa | server | rare)', ephemeral=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.author.bot and message.author.id != fuuka_id:
        return

    # Handle reminders: "tt 22"
    match = re.fullmatch(r"tt\s+(\d+)", message.content.strip(), re.IGNORECASE)

    if match and not message.author.bot:
        minutes = int(match.group(1))

        if minutes < 1:
            await message.reply("Please enter a reminder time of at least 1 minute.")
            return

        if minutes > 1440:
            await message.reply("The maximum reminder time is 1440 minutes (1 day).")
            return

        # Confirm that the reminder was created
        await message.reply(f"I've marked this moment among the stars. I'll call for you when the time comes ({minutes} minutes)")

        # Schedule the reminder without blocking the bot
        async def send_reminder():
            await asyncio.sleep(minutes * 60)
            await message.channel.send(
                f"The moment has arrived, Rover. It's time to return {message.author.mention}."
            )

        asyncio.create_task(send_reminder())
        return

    if message.author.id != fuuka_id and message.author.id != ra_id:
        return
    
    if "This Discord is linked to a series, so Fuuka" in message.content:
        await message.channel.send(f'{wuwaDrop.mention} Ordained. The Wuwa drop is here.')

    if "Fuuka is dropping cards! Click to claim !" in message.content:
        await message.channel.send(f'{serverDrop.mention} Server drop manifested.')

client.run(DISCORD_TOKEN)