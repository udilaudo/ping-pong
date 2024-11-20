from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from main import update_data
import json


# Carica il token dal file di configurazione
with open("config.json", "r") as f:
    config = json.load(f)

TOKEN = config["TOKEN"]

if not TOKEN:
    raise ValueError("Il token non è stato trovato nel file di configurazione!")

# carica il json
with open('players.json') as f:
    data = json.load(f)

lista_nomi = [player['name'] for player in data['players']]

# Funzione che gestisce l'invio di un saluto all'avvio del bot
async def start(update: Update, context) -> None:
    await update.message.reply_text("Ciao! Scrivi chi ha giocato.\n il primo nome è il vincitore, il secondo il perdente\n\n I possibili Giocatori sono:\n\n" + "\n".join(lista_nomi))

# Funzione che gestisce il comando /dati
async def dati(update: Update, context) -> None:
    # Qui puoi definire i dati che vuoi inviare
    await update.message.reply_photo(photo=open('plots/rating.png', 'rb'))
    await update.message.reply_document(document=open('results/rating.csv', 'rb'))


# Funzione che risponde ai messaggi
async def process_message(update: Update, context) -> None:
    # Estrai le parole dal messaggio
    words = update.message.text.split()

    # Verifica che ci siano almeno 2 parole
    if len(words) == 2:

        # controlla se i nomi sono presenti nella lista
        if words[0] not in lista_nomi or words[1] not in lista_nomi:
            await update.message.reply_text("Per favore, invia due nomi presenti nella lista")
            return

        # Chiama la funzione update con le 2 parole come argomenti
        update_data(*words)
        await update.message.reply_text(f"{words[0]} vs {words[1]}\nvittoria di {words[0]}\nElo aggiornati:\n{words[0]}: {data['players'][0]['rating']}\n{words[1]}: {data['players'][1]['rating']}")
        # invia una foto
        await update.message.reply_photo(photo=open('plots/rating.png', 'rb'))
        # invia il json con i dati
        await update.message.reply_document(document=open('results/rating.csv', 'rb'))
    else:
        # Risponde se non sono state inviate 3 parole
        await update.message.reply_text("Per favore, invia esattamente 2 parole.")

def main() -> None:
    # Crea l'oggetto Application
    application = Application.builder().token(TOKEN).build()

    # Aggiungi i gestori di comandi e messaggi
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("dati", dati))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_message))

    # Avvia il bot
    application.run_polling()

if __name__ == '__main__':
    main()
