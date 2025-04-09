import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from pronote_api import get_notes, get_edt, get_devoirs, get_absents, get_polling, get_all

load_dotenv("config.env")

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
PRONOTE_URL = os.getenv("PRONOTE_URL")

# ⚠️ Remplace par tes cookies PRONOTE actualisés
COOKIES = {
    "AUTH_SESSION_ID": "fdac6a37-3b68-4b21-a28e-d6ddc827e1fa",
    "AUTH_SESSION_ID_LEGACY": "fdac6a37-3b68-4b21-a28e-d6ddc827e1fa",
    "TS01e4588a": "01b0b9bf5c22ba14057cce7cc7af2dd4bad1ac993de11876356ebcf5f3bd7e98f8aa62fbfd454e5345a767ed4b150b14588104a8d4",
    "KEYCLOAK_IDENTITY": "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJjMTFhNjkyMy1mMmViLTQ1OTEtOTIyNC04MDI1ZDY3OTRiZWUifQ.eyJleHAiOjE3NDQyNjYzMjUsImlhdCI6MTc0NDIzMDMyNSwianRpIjoiYWIyNjFlMjQtNzdhOC00ZmQ0LWI3M2YtN2NmZDdlMzNlZTc1IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLm1vbmx5Y2VlLm5ldC9yZWFsbXMvSURGIiwic3ViIjoiZTE4OGMzZWYtNTUxZi00NDVmLThjZmMtZjFjMzRhOThkMjcxIiwidHlwIjoiU2VyaWFsaXplZC1JRCIsInNlc3Npb25fc3RhdGUiOiJmZGFjNmEzNy0zYjY4LTRiMjEtYTI4ZS1kNmRkYzgyN2UxZmEiLCJzaWQiOiJmZGFjNmEzNy0zYjY4LTRiMjEtYTI4ZS1kNmRkYzgyN2UxZmEiLCJzdGF0ZV9jaGVja2VyIjoiamVBbFA2NEdLc1ZYcTE4aFpuZ05uemRZVUpiOGNXU0JGd3hhVUV6bGg4VSJ9.b8NkeAcbMLrepgJOlbrJ_7J3CgD3ffk-HkfQddThq5jBjJOBZphGwIKu8uHCCfd_LBR5z5_EwjGqDjAt996snw",
    "KEYCLOAK_IDENTITY_LEGACY": "eyJhbGciOiJIUzUxMiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJjMTFhNjkyMy1mMmViLTQ1OTEtOTIyNC04MDI1ZDY3OTRiZWUifQ.eyJleHAiOjE3NDQyNjYzMjUsImlhdCI6MTc0NDIzMDMyNSwianRpIjoiYWIyNjFlMjQtNzdhOC00ZmQ0LWI3M2YtN2NmZDdlMzNlZTc1IiwiaXNzIjoiaHR0cHM6Ly9hdXRoLm1vbmx5Y2VlLm5ldC9yZWFsbXMvSURGIiwic3ViIjoiZTE4OGMzZWYtNTUxZi00NDVmLThjZmMtZjFjMzRhOThkMjcxIiwidHlwIjoiU2VyaWFsaXplZC1JRCIsInNlc3Npb25fc3RhdGUiOiJmZGFjNmEzNy0zYjY4LTRiMjEtYTI4ZS1kNmRkYzgyN2UxZmEiLCJzaWQiOiJmZGFjNmEzNy0zYjY4LTRiMjEtYTI4ZS1kNmRkYzgyN2UxZmEiLCJzdGF0ZV9jaGVja2VyIjoiamVBbFA2NEdLc1ZYcTE4aFpuZ05uemRZVUpiOGNXU0JGd3hhVUV6bGg4VSJ9.b8NkeAcbMLrepgJOlbrJ_7J3CgD3ffk-HkfQddThq5jBjJOBZphGwIKu8uHCCfd_LBR5z5_EwjGqDjAt996snw",
    "KEYCLOAK_SESSION": "IDF/e188c3ef-551f-445f-8cfc-f1c34a98d271/fdac6a37-3b68-4b21-a28e-d6ddc827e1fa",
    "KEYCLOAK_SESSION_LEGACY": "IDF/e188c3ef-551f-445f-8cfc-f1c34a98d271/fdac6a37-3b68-4b21-a28e-d6ddc827e1fa",
    "CASTJU_356A192B7913B04C54574D18C28D46E6395428AB": "CAqV8YtUeC7we2XZ",
    "DISSESSIONAuthnDelegation": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImU2NDU0ZmY1LWJlMmYtNGU3YS05NGRlLWJiMmUyM2Y3MDBhNiJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0...",
    "TS01e2022e": "01b0b9bf5c22ba14057cce7cc7af2dd4bad1ac993de11876356ebcf5f3bd7e98f8aa62fbfd454e5345a767ed4b150b14588104a8d4",
    "TGC": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6ImY4NTY5M2E5LTQ3YTEtNGYwNS1hOWVlLWM1MmI4YWEwYjEwNSJ9.ZXlKNmFYQWlPaUpFUlVZaUxDSmhiR2NpT2lKa2FYSWlMQ0psYm1NaU9pSkJNVEk0...",
    "org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE": "fr-FR",
    "TS01ac4393": "01b0b9bf5c22ba14057cce7cc7af2dd4bad1ac993de11876356ebcf5f3bd7e98f8aa62fbfd454e5345a767ed4b150b14588104a8d4",
    "KC_ROUTE": "kc007"
}


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.command()
async def notes(ctx):
    data = get_notes(PRONOTE_URL, COOKIES)
    await ctx.send(f"📝 Voici les notes :\n```{data}```")

@bot.command()
async def edt(ctx):
    data = get_edt(PRONOTE_URL, COOKIES)
    await ctx.send(f"📅 Emploi du temps :\n```{data}```")

@bot.command()
async def devoirs(ctx):
    data = get_devoirs(PRONOTE_URL, COOKIES)
    await ctx.send(f"📚 Devoirs à faire :\n```{data}```")

@bot.command()
async def absences(ctx):
    data = get_absents(PRONOTE_URL, COOKIES)
    await ctx.send(f"🚫 Absences :\n```{data}```")

@bot.command()
async def test(ctx):
    await ctx.send("✅ Bot opérationnel.")

@bot.command()
async def polling(ctx):
    data = get_polling(PRONOTE_URL, COOKIES)
    await ctx.send(f"📡 Résultat polling :\n```{data}```")
@bot.command()
async def tout(ctx):
    data = get_all(PRONOTE_URL, COOKIES)
    message = "🧠 Données complètes récupérées :\n"
    for key, value in data.items():
        message += f"\n📂 {key.capitalize()}:\n```{value[:500]}```\n"
    await ctx.send(message)


bot.run(TOKEN)
