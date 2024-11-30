import csv

# Zwiększenie limitu rozmiaru pola
csv.field_size_limit(1000000)  # Zwiększenie limitu do 1MB

# Pliki wejściowe i wyjściowe
csv_file = "produkty.csv"  # Plik CSV z danymi
ndjson_file = "produkty.ndjson"  # Plik wyjściowy w formacie NDJSON

# Konwersja CSV na NDJSON z nagłówkami "index"
with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    with open(ndjson_file, "w", encoding="utf-8") as nf:
        for row in reader:
            # Dodaj nagłówek "index" z unikalnym ID
            index_header = { "index": { "_id": row["ITEM_ID"] } }
            nf.write(f"{index_header}\n".replace("'", '"'))  # Zamiana ' na "
            # Dodaj właściwe dane
            nf.write(f"{row}\n".replace("'", '"'))  # Zamiana ' na "
