from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Połączenie z Elasticsearch
es = Elasticsearch(["http://localhost:9200"])

@app.route('/')
def index():
    return "API działa"

# Endpoint wyszukiwania
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')  # Pobierz zapytanie z URL

    if not query:
        return jsonify({"error": "Brak zapytania"})

    # Zapytanie do Elasticsearch
    response = es.search(
        index="produkty",
        body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["PRODUCTNAME", "DESCRIPTION"]
                }
            },
            "size": 10  # Liczba wyników
        }
    )

    # Przetwórz wyniki
    results = []
    for hit in response['hits']['hits']:
        results.append({
            "ITEM_ID": hit['_source'].get('ITEM_ID'),
            "PRODUCTNO": hit['_source'].get('PRODUCTNO'),
            "PRODUCTNAME": hit['_source'].get('PRODUCTNAME'),
            "PRICE_VAT": hit['_source'].get('PRICE_VAT'),
            "IMGURL": hit['_source'].get('IMGURL'),  # Przekazujemy URL obrazu
            "URL": hit['_source'].get('URL')  # Przekazujemy URL produktu
        })

    return jsonify({"results": results})


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
