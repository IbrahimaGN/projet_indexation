from flask import Flask, jsonify, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["Brand", "Description"]
            }
        }
    }

    try:
        res = es.search(index="products", body=body)
        return jsonify(res['hits']['hits'])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


