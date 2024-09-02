from flask import Flask, render_template, jsonify, request
from elasticsearch import Elasticsearch

app = Flask(__name__)
es = Elasticsearch("http://localhost:9200")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard.html')
def dashboard():
    return render_template('dashboard.html')


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q')
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["Brand", "Description"]
            }
        }
    }
    
    res = es.search(index="products", body=body)
    return jsonify(res['hits']['hits'])

if __name__ == '__main__':
    app.run(debug=True)
