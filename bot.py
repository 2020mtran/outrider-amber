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

# Initialize global variables
commonRole = None
uncommonRole = None
rareRole = None
epicRole = None
legendaryRole = None

@client.event
async def on_ready():
    print(f'Outrider Amber, reporting!')

    guild = client.get_guild(int(os.getenv('GUILD_ID')))
    if guild is None:
        print(f'Guild with ID {os.getenv("GUILD_ID")} not found.')
        return
    
    global commonRole, uncommonRole, rareRole, epicRole, legendaryRole
    commonRole = discord.utils.get(guild.roles, id=int(os.getenv('COMMON_ID')))
    uncommonRole = discord.utils.get(guild.roles, id=int(os.getenv('UNCOMMON_ID')))
    rareRole = discord.utils.get(guild.roles, id=int(os.getenv('RARE_ID')))
    epicRole = discord.utils.get(guild.roles, id=int(os.getenv('EPIC_ID')))
    legendaryRole = discord.utils.get(guild.roles, id=int(os.getenv('LEGENDARY_ID')))

    startup_channel = guild.get_channel(int(os.getenv('STARTUP_CHANNEL_ID')))
    if startup_channel:
        await startup_channel.send('Outrider Amber, reporting for duty!')

    # Sync the command tree with the guild
    await tree.sync(guild=guild)

@tree.command(name="getrole", description="Assign yourself a role (common, uncommon, rare, epic, legendary)", guild=discord.Object(id=GUILD_ID))
async def get_role(interaction: discord.Interaction, role_name: str):
    role = None

    if role_name.lower() == "common":
        role = commonRole
    elif role_name.lower() == "uncommon":
        role = uncommonRole
    elif role_name.lower() == "rare":
        role = rareRole
    elif role_name.lower() == "epic":
        role = epicRole
    elif role_name.lower() == "legendary":
        role = legendaryRole

    if role:
        await interaction.user.add_roles(role)
        await interaction.response.send_message(f'You have been assigned the role: {role.name}')
    else:
        await interaction.response.send_message('Role not found. Please use one of the following: common, uncommon, rare, epic, legendary.', ephemeral=True)

@tree.command(name="removerole", description="Remove a role from yourself", guild=discord.Object(id=GUILD_ID))
async def remove_role(interaction: discord.Interaction, role_name: str):
    role = None

    if role_name.lower() == "common":
        role = commonRole
    elif role_name.lower() == "uncommon":
        role = uncommonRole
    elif role_name.lower() == "rare":
        role = rareRole
    elif role_name.lower() == "epic":
        role = epicRole
    elif role_name.lower() == "legendary":
        role = legendaryRole

    if role and role in interaction.user.roles:
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f'The role {role.name} has been removed from you.')
    else:
        await interaction.response.send_message('Role not found or you do not have this role. Please use one of the following: common, uncommon, rare, epic, legendary.', ephemeral=True)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('Edition seven'):
        pattern = r'\((\d+)\s*wl\)'
        match = re.search(pattern, message.content)
        # await message.channel.send(f'Found an edition, now determining its worth...')
        # await message.channel.send(f'Matching: {match}')

        if match:
            target_str = match.group(1) # this gets whatever is in the parentheses
            target = int(target_str)
            # await message.channel.send(f'Wishlist is: {target_str}')

            if target >= 100 and target < 200:
                role = commonRole
            elif target >= 200 and target < 500:
                role = uncommonRole
            elif target >= 500 and target < 1000:
                role = rareRole
            elif target >= 1000 and target < 2000:
                role = epicRole
            elif target >= 2000:
                role = legendaryRole
            else:
                role = None
            
            if role: 
                await message.channel.send(f'{role.mention} A new edition has dropped!')

client.run(DISCORD_TOKEN)