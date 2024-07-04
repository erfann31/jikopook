import logging

from elasticsearch import Elasticsearch
from flask import Blueprint, request, jsonify, current_app

search = Blueprint('search', __name__)


def get_es_client():
    es_cloud_id = current_app.config['ELASTICSEARCH_CLOUD_ID']
    es_api_key = current_app.config['ELASTICSEARCH_API_KEY']
    return Elasticsearch(
        cloud_id=es_cloud_id,
        api_key=es_api_key,
    )


@search.route('/query', methods=['POST'])
def search_query():
    data = request.get_json()
    query_text = data.get('query')
    if not query_text:
        logging.error("Query text is required")
        return jsonify({"error": "Query text is required"}), 400

    es = get_es_client()
    index_name = current_app.config['ELASTICSEARCH_INDEX']

    query = {
        "query": {
            "multi_match": {
                "query": query_text,
                "fields": ["cluster", "data"]
            }
        }
    }

    try:
        response = es.search(index=index_name, body=query)
        return jsonify(response['hits']['hits']), 200
    except Exception as e:
        logging.error(f"Error executing search query: {str(e)}")
        return jsonify({"error": str(e)}), 500
