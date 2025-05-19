import discord
import os
import json

TOKEN = os.getenv("TOKEN")
ID_SALON_CIBLE = int(os.getenv("SALON_ID"))

FICHIER_IDENTITES = "identites.json"
PREFIX_ANONYME = "Anonyme"

intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.guilds = True

client = discord.Client(intents=intents)

if os.path.exists(FICHIER_IDENTITES):
    with open(FICHIER_IDENTITES, "r") as f:
        identites = json.load(f)
else:
    identites = {}

def sauvegarder_identites():
    with open(FICHIER_IDENTITES, "w") as f:
        json.dump(identites, f)

def obtenir_identite_anon(user_id):
    if str(user_id) not in identites:
        nouveau_num = len(identites) + 1
        identites[str(user_id)] = f"{PREFIX_ANONYME} {str(nouveau_num).zfill(2)}"
        sauvegarder_identites()
    return identites[str(user_id)]

@client.event
async def on_ready():
    print(f"Connecté en tant que {client.user.name}")

@client.event
async def on_message(message):
    if message.guild or message.author == client.user:
        return

    salon = client.get_channel(ID_SALON_CIBLE)
    if not salon:
        print("Salon introuvable.")
        return

    pseudo = obtenir_identite_anon(message.author.id)
    embed = discord.Embed(title=pseudo, description=message.content, color=0x2f3136)
    await salon.send(embed=embed)
    await message.channel.send("Message transmis anonymement au Bureau 9.")

client.run(TOKEN)