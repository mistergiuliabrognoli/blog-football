import os
import json
import re
from datetime import datetime

# Traduzione dei mesi per data in italiano
MESI = {
    1: "Gennaio", 2: "Febbraio", 3: "Marzo", 4: "Aprile",
    5: "Maggio", 6: "Giugno", 7: "Luglio", 8: "Agosto",
    9: "Settembre", 10: "Ottobre", 11: "Novembre", 12: "Dicembre"
}

def extract_metadata(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    title = filename.replace('.md', '').replace('.txt', '').replace('-', ' ').title()
    
    # Data formattata in italiano
    mod_time = datetime.fromtimestamp(os.path.getmtime(filepath))
    date_str = f"{mod_time.day} {MESI[mod_time.month]} {mod_time.year}"
    
    # Immagine di default
    image = 'https://images.unsplash.com/photo-1579952363873-27f3bade9f55?q=80&w=800'
    excerpt = ""
    tags = ["Nuovo"]

    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line: continue
        
        # Trova il primo titolo (# Titolo)
        if line.startswith('# ') and title == filename.replace('.md', '').replace('.txt', '').replace('-', ' ').title():
            title = line[2:].strip()
        
        # Trova la prima immagine nel markdown ![alt](url)
        img_match = re.search(r'!\[.*?\]\((.*?)\)', line)
        if img_match and 'unsplash.com' not in image: # Sostituisci solo se è l'immagine di default
            image = img_match.group(1)
            
        # Estrai la prima frase per l'anteprima (ignora titoli e immagini)
        if not line.startswith('#') and not line.startswith('!') and len(line) > 30 and not excerpt:
            # Rimuovi eventuali formattazioni markdown base
            clean_line = line.replace('*', '').replace('_', '')
            excerpt = clean_line[:130] + "..." if len(clean_line) > 130 else clean_line

    return {
        "id": filename,
        "title": title,
        "date": date_str,
        "image": image,
        "excerpt": excerpt,
        "tags": tags,
        "timestamp": os.path.getmtime(filepath)
    }

def scan_directory(directory):
    db = []
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith(".md") or filename.endswith(".txt"):
                filepath = os.path.join(directory, filename)
                metadata = extract_metadata(filepath)
                db.append(metadata)
    
    # Ordina i post dal più recente al più vecchio
    db.sort(key=lambda x: x['timestamp'], reverse=True)
    return db

print("Generazione database.json in corso...")

database = {
    "blog": scan_directory("content/blog"),
    "allenamenti": scan_directory("content/allenamenti")
}

with open('database.json', 'w', encoding='utf-8') as f:
    json.dump(database, f, indent=4, ensure_ascii=False)

print("✅ database.json generato con successo!")
print(f"Trovati {len(database['blog'])} articoli e {len(database['allenamenti'])} allenamenti.")
