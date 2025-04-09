
# Pronote Discord Bot (avec ENT monlycée.net)

Ce projet utilise `headless-ent` pour se connecter à Pronote via l'ENT monlycée.net.
Une fois connecté, il envoie des notifications sur Discord (notes, devoirs, absences, emploi du temps).

## 📦 Contenu :
- `bot.py` : le bot Discord
- `config.env` : ton fichier de configuration (à compléter)
- `headless_login.py` : récupère un token Pronote via headless-ent

## 🚀 Instructions :
1. Installe les dépendances :
   pip install -r requirements.txt

2. Complète le fichier `config.env` avec :
   - ton identifiant monlycée.net
   - ton mot de passe
   - ton URL Pronote
   - ton token Discord

3. Lance le script de connexion :
   python headless_login.py

4. Lance le bot :
   python bot.py

⚠️ Ne partage jamais ton fichier `.env` ou tes identifiants.
