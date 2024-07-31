import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup

def get_price_from_url(url):
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    response = requests.get(url, headers=custom_headers)
    soup = BeautifulSoup(response.text, 'lxml')

    product_name = soup.select_one('#productTitle').text.strip()
    product_price = soup.select_one('span.a-offscreen').text

    return (product_name, product_price)

    
    

load_dotenv()
discord_api_key = os.getenv('DISCORD_API_KEY')

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("$hello"):
        url = 'https://www.amazon.com/Sony-WH-1000XM4-Canceling-Headphones-phone-call/dp/B0863TXGM3'
        name, price = get_price_from_url(url)

        await message.channel.send(f"{name}: {price}")

client.run(discord_api_key)