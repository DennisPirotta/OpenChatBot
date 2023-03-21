import pypdf
import pandas as pd

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

def extract_bookmarks(pdf_path):
    # Apre il file PDF in modalità di lettura binaria
    with open(pdf_path, 'rb') as f:
        # Crea un oggetto PdfFileReader per leggere il contenuto del PDF
        pdf_reader = pypdf.PdfReader(f)
        
        if pdf_reader.outline:
            # map page ids to page numbers
            pg_id_num_map = _setup_page_id_to_num(pdf_reader)
            # Estrae i segnalibri dal PDF
            outlines = pdf_reader.outline
            # Crea una lista vuota per contenere i dati dei segnalibri
            data = []
        
            #print(bookmarks)
        
            for outline in outlines:
                if isinstance(outline, list):
                    # se l'oggetto è una lista, cicla ricorsivamente
                    for sublist in outline:
                        if isinstance(sublist, pypdf.generic.Destination):
                            title = sublist['/Title']
                            if title is not None:
                                print(title)
                                print(pg_id_num_map[sublist.page.idnum] + 1)
                            else:
                                print("Segnalibro senza titolo")
                elif isinstance(outline, tuple):
                    # se l'oggetto è una tupla, cicla ricorsivamente
                    for subtuple in outline:
                        if isinstance(subtuple, pypdf.generic.Destination):
                            title = subtuple['/Title']
                            if title is not None:
                                print(title)
                            else:
                                print("Segnalibro senza titolo")
                elif isinstance(outline, pypdf.generic.Destination):
                    # se l'oggetto è una destinazione, stampa il titolo
                    title = outline['/Title']
                    if title is not None:
                        print(title)
                    else:
                        print("Segnalibro senza titolo")
                else:
                    print(f"Tipo di segnalibro non supportato: {type(outline)}")
        
            # Cicla sui segnalibri estratti
            #for bookmark in bookmarks:
                #if isinstance(bookmark, list)
                #print(bookmark['/Title'])
                #print('\n')
                # Estrae il titolo del segnalibro e la pagina a cui si riferisce
                #title = bookmark['/Title']
                #page_num = pg_id_num_map[bookmark.page.idnum] + 1
                # Aggiunge i dati del segnalibro alla lista
                #data.append({'Titolo': title, 'Pagina': page_num})
            #Crea una tabella Pandas con i dati dei segnalibri
            df = pd.DataFrame(data)
            return df
        
pdf_path = './target.pdf'
bookmarks_table = extract_bookmarks(pdf_path)
print(bookmarks_table)
