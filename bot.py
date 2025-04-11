
import discord
from discord.ext import commands
import requests  # Correction ici

from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")



intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user.name}")

@bot.command()
async def hello(ctx):
    await ctx.send("Salut ! Je suis ton bot Python prêt à te servir 🤖")

@bot.command()
async def meteo(ctx, *, ville: str = "Paris"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ville}&appid={API_KEY}&units=metric&lang=fr"
        response = requests.get(url)
        print("URL utilisée :", url)
        print("Code HTTP :", response.status_code)
        print("Réponse brute :", response.text)

        data = response.json()

        if str(data.get("cod")) != "200":
            await ctx.send(f"❌ Ville introuvable : {ville}")
            return

        nom_ville = data["name"]
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        humid = data["main"]["humidity"]
        vent = data["wind"]["speed"]

        await ctx.send(
            f"🌍 **{nom_ville}**\n🌡️ Température : {temp}°C\n☁️ Ciel : {desc.capitalize()}\n💧 Humidité : {humid}%\n💨 Vent : {vent} km/h"
        )

    except Exception as e:
        await ctx.send("⚠️ Une erreur est survenue.")
        print(f"Erreur API météo : {e}")


bot.run(DISCORD_TOKEN)
