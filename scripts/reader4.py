import PyPDF2
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
nltk.download('punkt')
# apri il file PDF
with open('target.pdf', 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    # ottieni il testo del documento
    text = ''
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        text += page.extract_text()

# elabora il testo per la ricerca
sentences = sent_tokenize(text)
words = [word_tokenize(sentence.lower()) for sentence in sentences]

# esegui la ricerca
question = input("Inserisci la domanda: ")
for i, sentence in enumerate(words):
    if set(word_tokenize(question.lower())).issubset(set(sentence)):
        # la domanda è contenuta in questa frase
        # ritorna il titolo del paragrafo
        print("Titolo del paragrafo: ", sentences[i-1])
        break
