import requests
import discord
from dotenv import load_dotenv
import os
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.app_commands import Choice
import openai
from PIL import Image
import csv
import aiohttp
import numpy as np
from transformers import BlipProcessor, BlipForConditionalGeneration
import base64
load_dotenv()


intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)



@client.tree.command(name='resume_score', description='See how well your resume matches with different job positions')
@app_commands.describe(resume_link = "Google Drive Link to your Resume")
@app_commands.checks.cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
async def resume_score(interaction: discord.Interaction, resume_link: str):
    
    return 

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')



# Create a coroutine that handles image messages.
@client.event
async def on_message(message):
  
  global headers
  
  if message.author == client.user:
        return
  
  if message.attachments and message.content.startswith('memeify') or message.content.startswith('Memeify'):
    # Get the image from the message.
    image_url = message.attachments[0].url
    
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                

                payload = {
                    "model": "gpt-4-vision-preview",
                    "messages": [
                    {
                        "role": "user",
                        "content": [
                        {
                            "type": "text",
                            "text": "Act as a professional at generating funny meme captions given images. Generate 1 meme caption for the image attached. Make the caption extremely specific to what's in the image. Output only the meme caption and nothing else."
                        },
                        {
                            "type": "image_url",
                            "image_url": image_url
                        }
                        ]
                    }
                    ],
                    "max_tokens": 300
                }
                try: 
                    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

                    meme_caption = response.json()['choices'][0]['message']['content']

                    print("MEME CAPTION:", meme_caption)
                    
                    await message.channel.send(meme_caption)

                except Exception as e:

                    return 



@client.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f"Please wait for {round(error.retry_after, 0)} seconds before running the command again!", ephemeral=True)
    else:
        await interaction.response.send_message(f"Please wait for {round(error.retry_after, 0)} seconds before running the command again!", ephemeral=True)


client.run(os.environ.get('DISCORD_TOKEN'))