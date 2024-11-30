import os
import json
import math
import xml.etree.ElementTree as ET
import requests

def parse_xml_to_ndjson(xml_file, ndjson_file):
    """
    Funkcja do konwersji XML na NDJSON.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()

    with open(ndjson_file, "w", encoding="utf-8") as nf:
        for item in root.findall("SHOPITEM"):
            record = {
                "ITEM_ID": item.find("ITEM_ID").text if item.find("ITEM_ID") is not None else None,
                "PRODUCTNO": item.find("PRODUCTNO").text if item.find("PRODUCTNO") is not None else None,
                "PRODUCTNAME": item.find("PRODUCTNAME").text if item.find("PRODUCTNAME") is not None else None,
                "EAN": item.find("EAN").text if item.find("EAN") is not None else None,
                "DESCRIPTION": item.find("DESCRIPTION").text if item.find("DESCRIPTION") is not None else None,
                "URL": item.find("URL").text if item.find("URL") is not None else None,
                "IMGURL": item.find("IMGURL").text if item.find("IMGURL") is not None else None,
                "PRICE_VAT": item.find("PRICE_VAT").text if item.find("PRICE_VAT") is not None else None,
                "MANUFACTURER": item.find("MANUFACTURER").text if item.find("MANUFACTURER") is not None else None,
                "CATEGORYTEXT": item.find("CATEGORYTEXT").text if item.find("CATEGORYTEXT") is not None else None,
                "DELIVERY_DATE": item.find("DELIVERY_DATE").text if item.find("DELIVERY_DATE") is not None else None,
                "NX_SystemName": item.find("NX_SystemName").text if item.find("NX_SystemName") is not None else None,
                "NX_StockCategory": item.find("NX_StockCategory").text if item.find("NX_StockCategory") is not None else None,
            }
            index_header = {"index": {"_id": record["ITEM_ID"]}}
            nf.write(json.dumps(index_header) + "\n")
            nf.write(json.dumps(record) + "\n")

def split_ndjson(ndjson_file, output_dir, parts=10):
    """
    Funkcja do podziału NDJSON na mniejsze pliki.
    """
    with open(ndjson_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    chunk_size = math.ceil(len(lines) / parts)
    os.makedirs(output_dir, exist_ok=True)

    for i in range(parts):
        chunk_file = os.path.join(output_dir, f"chunk_{i + 1}.ndjson")
        with open(chunk_file, "w", encoding="utf-8") as cf:
            cf.writelines(lines[i * chunk_size:(i + 1) * chunk_size])
        print(f"Stworzono plik: {chunk_file}")

def upload_to_elasticsearch(files, es_url, index_name):
    """
    Funkcja do wgrywania plików NDJSON na Elasticsearch.
    """
    headers = {"Content-Type": "application/x-ndjson"}
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            data = f.read()
        response = requests.post(f"{es_url}/{index_name}/_bulk", headers=headers, data=data)
        if response.status_code == 200:
            print(f"Pomyślnie wgrano plik: {file}")
        else:
            print(f"Błąd przy wgrywaniu pliku {file}: {response.text}")

# Ścieżki plików i konfiguracja
xml_file = "data.xml"
ndjson_file = "produkty.ndjson"
output_dir = "chunks"
es_url = "http://localhost:9200"  # URL Elasticsearch
index_name = "produkty"  # Nazwa indeksu w Elasticsearch

# Wykonanie procesów
parse_xml_to_ndjson(xml_file, ndjson_file)
split_ndjson(ndjson_file, output_dir)
chunk_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".ndjson")]
upload_to_elasticsearch(chunk_files, es_url, index_name)
