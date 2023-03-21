import pypdf
import pandas as pd
from prettytable import PrettyTable
from pdf2image import convert_from_path
import random
import os, shutil
        
table = PrettyTable()
table.field_names = ["Indice","Titolo", "Pagina"]

def _setup_page_id_to_num(pdf, pages=None, _result=None, _num_pages=None):
    if _result is None:
        _result = {}
    if pages is None:
        _num_pages = []
        pages = pdf.trailer["/Root"].get_object()["/Pages"].get_object()
    t = pages["/Type"]
    if t == "/Pages":
        for page in pages["/Kids"]:
            _result[page.idnum] = len(_num_pages)
            _setup_page_id_to_num(pdf, page.get_object(), _result, _num_pages)
    elif t == "/Page":
        _num_pages.append(1)
    return _result

def setup_outlines_table(outlines,pg_id_num_map):
    for outline in outlines:
        if isinstance(outline, list):
            # se l'oggetto è una lista, cicla ricorsivamente
            setup_outlines_table(outline,pg_id_num_map)
        else:
            # se l'oggetto è valido, aggiungi una riga alla tabella
            # uso il try in caso alcuni indici senza riferimenti vengano prelevati involontariamente
            try:
                index = outline.title.split(' ', 1)[0]
                title = outline.title.split(' ', 1)[1]
                page = pg_id_num_map[outline.page.idnum] + 1
                table.add_row([index,title,page])
            except IndexError:
                continue

def extract_outlines(pdf_path):
    # Apre il file PDF in modalità di lettura binaria
    with open(pdf_path, 'rb') as f:
        # Crea un oggetto PdfFileReader per leggere il contenuto del PDF
        pdf_reader = pypdf.PdfReader(f)
        
        if pdf_reader.outline:
            # map page ids to page numbers
            pg_id_num_map = _setup_page_id_to_num(pdf_reader)
            # Estrae i segnalibri dal PDF
            outlines = pdf_reader.outline
            # Stampa i segnalibri
            setup_outlines_table(outlines,pg_id_num_map)
        
def search_pdf(file_path, query):
    # Apriamo il file PDF in modalità lettura binaria
    with open(file_path, 'rb') as pdf_file:
        # Crea un oggetto PDFReader dal file PDF
        pdf_reader = pypdf.PdfReader(pdf_file)
        # Carica le pagine per salvarle come immagini
        pages = convert_from_path(file_path,500)
        # Rimuovo le immagini presenti nella cartella di output
        remove_last_images('./img')
        # Iteriamo attraverso le pagine del PDF
        for page in pdf_reader.pages:
            # Estraiamo il testo dalla pagina corrente
            text = page.extract_text().lower()

            # Cerchiamo la query all'interno del testo
            if query in text:
                # Stampa la pagina e la posizione della query all'interno del testo
                print(f"Trovato '{query}' alla pagina {pdf_reader.get_page_number(page) + 1}")
                # Salvo la pagina come JPEG nel formato page_{numero della pagina}_{Hash random per evitare doppioni}
                pages[pdf_reader.get_page_number(page)].save(f"img/page_{pdf_reader.get_page_number(page) + 1}_{random.getrandbits(128)}",'JPEG')
                
def remove_last_images(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
           
            
#extract_outlines('./target.pdf')
#print(table)
try:
    while True:
        query = input('Inserisci un campo di ricerca (digita "exit" o premi CTRL+C per uscire): ')
        if query == 'exit':
            print('Bye!')
            break
        else:
            search_pdf('./target.pdf', query.lower())
except KeyboardInterrupt:
    print('\nBye!')


