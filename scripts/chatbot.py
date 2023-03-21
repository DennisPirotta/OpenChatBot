from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import PyPDF2
import pytesseract
from PIL import Image

# crea il chatbot
bot = ChatBot('Il mio bot di risposte PDF')

# crea un trainer per il bot e addestra il bot sul corpus di domande e risposte in inglese predefinito
trainer = ChatterBotCorpusTrainer(bot)
trainer.train('chatterbot.corpus.italian')

# apri il file PDF e crea un oggetto pdfReader
pdfFileObj = open('nome_del_file.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# estrai il testo dal PDF
text = ''
for pageNum in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(pageNum)
    text += pageObj.extractText()

# definisci una funzione che cerchi la risposta alla domanda nel testo del PDF
def cerca_risposta(domanda):
    risposta = ''
    if domanda in text:
        risposta = text.split(domanda)[1].split('\n')[0]
    return risposta

# esegui il ciclo di conversazione con l'utente
while True:
    try:
        # chiedi all'utente di inserire la domanda
        domanda = input("Tu: ")

        # cerca la risposta nel testo del PDF
        risposta = cerca_risposta(domanda)

        # se la risposta è stata trovata, stampala
        if risposta:
            print("Bot: ", risposta)
        # altrimenti, fai rispondere il bot utilizzando ChatterBot
        else:
            risposta_bot = bot.get_response(domanda)
            print("Bot: ", risposta_bot)

    # gestisci eventuali eccezioni
    except(KeyboardInterrupt, EOFError, SystemExit):
        break
