import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

# Charger les variables d’environnement
load_dotenv("config.env")

ENT_USERNAME = os.getenv("ENT_USERNAME")
ENT_PASSWORD = os.getenv("ENT_PASSWORD")
PRONOTE_URL = os.getenv("PRONOTE_URL")

async def run():
    async with async_playwright() as p:
        # Lancer le navigateur avec affichage
        browser = await p.chromium.launch(headless=False, slow_mo=100)
        context = await browser.new_context()
        page = await context.new_page()

        print("🔗 Connexion à l'ENT Monlycée.net...")

        # Étape 1 : Accès à Pronote
        await page.goto(PRONOTE_URL)
        await page.wait_for_timeout(3000)

        # Étape 2 : Remplir les identifiants
        try:
            await page.fill("#username", ENT_USERNAME)
            await page.fill("#password", ENT_PASSWORD)
        except Exception as e:
            print("❌ Erreur lors du remplissage des champs :", e)
            await page.screenshot(path="erreur_remplissage.png")
            await browser.close()
            return

        # Étape 3 : Cliquer sur "Se connecter"
        try:
            await page.locator("button:has-text('Se connecter')").click()
        except Exception as e:
            print("❌ Bouton de connexion introuvable :", e)
            await page.screenshot(path="erreur_bouton.png")
            await browser.close()
            return

        # Étape 4 : Attendre la redirection vers Pronote
        await page.wait_for_url("**/pronote/**", timeout=20000)
        print("✅ Redirigé vers Pronote")

        # Étape 5 : Forcer l’accès à l’espace élève
        if "/eleve.html" not in page.url:
            await page.goto(f"{PRONOTE_URL}/eleve.html")
            await page.wait_for_timeout(5000)

        await page.screenshot(path="eleve_ok.png")

        # Étape 6 : Extraction des cookies
        cookies = await context.cookies()
        print("\n🍪 Cookies PRONOTE récupérés :\n")

        if not cookies:
            print("❌ Aucun cookie trouvé. Peut-être un problème de redirection.")
        else:
            for c in cookies:
                print(f"{c['name']} = {c['value']}")

        await page.screenshot(path="session_ok.png")
        print("✅ Connexion réussie !")
        await browser.close()

asyncio.run(run())
