import discord
from discord import app_commands
import re
import os
from config import DISCORD_TOKEN, GUILD_ID, STARTUP_CHANNEL_ID, COMMON_ID, UNCOMMON_ID, RARE_ID, EPIC_ID, LEGENDARY_ID

# Discord Client Initialization
intents = discord.Intents.default()
intents.message_content = True

token = DISCORD_TOKEN
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
fuuka_id = 1230570999833952287
ra_id = 184864181663563776

# Initialize global variables
wuwaDropRole = None
serverDropRole = None
rareRole = None
epicRole = None
legendaryRole = None

@client.event
async def on_ready():
    print(f'The Shorekeeper, ready.')

    guild = client.get_guild(int(os.getenv('GUILD_ID')))
    if guild is None:
        print(f'Guild with ID {os.getenv("GUILD_ID")} not found.')
        return
    
    global wuwaDrop, serverDrop
    wuwaDrop = discord.utils.get(guild.roles, id=int(os.getenv('COMMON_ID')))
    serverDrop = discord.utils.get(guild.roles, id=int(os.getenv('UNCOMMON_ID')))

    startup_channel = guild.get_channel(int(os.getenv('STARTUP_CHANNEL_ID')))
    if startup_channel:
        await startup_channel.send('I`ll fulfill it, be it a direct command or any other wish you have.')

    # Sync the command tree with the guild
    await tree.sync(guild=guild)

@tree.command(name="getrole", description="Assign yourself a drop ping role (wuwa | server).", guild=discord.Object(id=GUILD_ID))
async def get_role(interaction: discord.Interaction, role_name: str):
    role = None

    if role_name.lower() == "wuwa":
        role = wuwaDrop
    elif role_name.lower() == "server":
        role = serverDrop

    if role:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'You have been assigned the role: {role.name}')
    else:
        await interaction.response.send_message('Role not found. Please use one of the following: (wuwa | server)', ephemeral=True)

@tree.command(name="removerole", description="Remove a role from yourself (wuwa | server)", guild=discord.Object(id=GUILD_ID))
async def remove_role(interaction: discord.Interaction, role_name: str):
    role = None

    if role_name.lower() == "wuwa":
        role = wuwaDrop
    elif role_name.lower() == "uncommon":
        role = serverDrop

    if role and role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f'The role {role.name} has been removed from you.')
    else:
        await interaction.response.send_message('Role not found or you do not have this role. Please use one of the following: wuwa | server.', ephemeral=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.author.id != fuuka_id and message.author.id != ra_id:
        return
    
    if "This Discord is linked to a series, so Fuuka" in message.content:
        await message.channel.send(f'{wuwaDropRole.mention} Ordained. The Wuwa drop is here.')

    if "Fuuka is dropping cards! Click to claim !" in message.content:
        await message.channel.send(f'{serverDropRole.mention} Server drop manifested.')

client.run(DISCORD_TOKEN)