#!/bin/bash

# Spostati nella cartella dello script (la cartella del sito)
cd "$(dirname "$0")"

echo "========================================="
echo "  Aggiornamento Sito M.G. Brognoli"
echo "========================================="
echo ""
echo "Leggendo i file nelle cartelle content/blog e content/allenamenti..."

# Esegui lo script Python per leggere i markdown e creare database.json
python3 generate_db.py

echo ""
echo "Apro Google Chrome all'indirizzo del test locale..."

# Apri Chrome a localhost:8000. Il server Python ci mette un istante ad avviarsi.
(sleep 1 && open -a "Google Chrome" http://localhost:8000) &

echo "Avvio il server locale..."
echo "✅ IL SITO È ORA ATTIVO."
echo "Per spegnere il server chiudi questa finestra del terminale."
echo "========================================="

# Avvia il server http python
python3 -m http.server 8000
