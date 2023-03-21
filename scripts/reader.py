import PyPDF2
import spacy

# Caricamento del modello NLP per la lingua italiana
nlp = spacy.load('en_core_web_sm')

# Funzione per estrarre l'indice dal file PDF
def extract_index(filename):
    # Aprire il file PDF
    pdf_file = open(filename, 'rb')
    # Creare un oggetto PDFReader con PyPDF2
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # Verificare se il file ha un indice
    if '/Index' not in pdf_reader.trailer['/Root']:
        print('Il file PDF non ha un indice.')
        return None
    # Estrarre il contenuto del PDF
    text = ''
    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    # Usare spaCy per elaborare il testo del PDF
    doc = nlp(text)
    # Trovare l'oggetto "Index" nel testo del PDF
    for token in doc:
        if token.text.lower() == 'indice':
            index_start = token.idx
            break
    # Trovare la fine dell'indice
    index_end = text.find('Capitolo', index_start)
    # Estrarre l'indice
    index_text = text[index_start:index_end]
    return index_text

# Funzione per trovare la pagina corrispondente all'elemento dell'indice
def find_page(filename, index_item):
    # Aprire il file PDF
    pdf_file = open(filename, 'rb')
    # Creare un oggetto PDFReader con PyPDF2
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    # Trovare il numero di pagina corrispondente all'elemento dell'indice
    for page_num in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(page_num)
        text = page.extractText()
        if index_item in text:
            return page_num + 1
    return None

# Funzione per cercare l'elemento dell'indice in base a una domanda
def find_index_item(filename, query):
    # Estrarre l'indice dal file PDF
    index_text = extract_index(filename)
    if index_text is None:
        return None
    # Usare spaCy per elaborare il testo dell'indice
    doc = nlp(index_text)
    # Trovare l'elemento dell'indice corrispondente alla domanda
    for token in doc:
        if token.text.lower() == query.lower():
            index_item = token.head.text
            return index_item
    return None

# Esempio di utilizzo
filename = 'target.pdf'
query = 'Ethernet LAN?'
# Trovare l'elemento dell'indice corrispondente alla domanda
index_item = find_index_item(filename, query)
if index_item is None:
    print('L\'elemento dell\'indice corrispondente alla domanda non è stato trovato.')
else:
    # Trovare la pagina corrispondente all'elemento dell'indice
    page_num = find_page(filename, index_item)
    if page_num is None:
        print('La pagina corrispondente all\'elemento dell\'indice non è stata trovata.')
    else:
        print(f'L\'elemento dell\'indice "{index_item}" si trova alla pagina {page_num}.')
        
