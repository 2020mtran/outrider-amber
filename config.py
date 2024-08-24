from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access environment variables
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
STARTUP_CHANNEL_ID = os.getenv('STARTUP_CHANNEL_ID')
COMMON_ID = os.getenv('COMMON_ID')
UNCOMMON_ID = os.getenv('UNCOMMON_ID')
RARE_ID = os.getenv('RARE_ID')
EPIC_ID = os.getenv('EPIC_ID')
LEGENDARY_ID = os.getenv('LEGENDARY_ID')