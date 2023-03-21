import PyPDF2
import pytesseract
from PIL import Image

# apri il file PDF e crea un oggetto pdfReader
pdfFileObj = open('target.pdf', 'rb')
pdfReader = PyPDF2.PdfReader(pdfFileObj)

# estrai il testo dal PDF
text = ''
for pageNum in range(len(pdfReader.pages)):
    pageObj = pdfReader.pages[pageNum]
    text += pageObj.extract_text()

# leggi la domanda dall'utente
domanda = input("Inserisci la domanda: ")

# cerca la risposta nel testo del PDF
risposta = ''
if domanda in text:
    risposta = text.split(domanda)[1].split('\n')[0]

# stampa la risposta
print("Risposta:", risposta)
