import logging

from elasticsearch import Elasticsearch
from flask import Blueprint, jsonify, current_app

from app.utils.cluster import cluster_extracted_data

cluster = Blueprint('cluster', __name__)


def get_es_client():
    es_cloud_id = current_app.config['ELASTICSEARCH_CLOUD_ID']
    es_api_key = current_app.config['ELASTICSEARCH_API_KEY']
    return Elasticsearch(
        cloud_id=es_cloud_id,
        api_key=es_api_key,
    )


@cluster.route('/', methods=['GET'])
def cluster_data():
    extracted_data = current_app.config['EXTRACTED_DATA']
    if not extracted_data:
        return jsonify({"error": "No data to cluster"}), 400

    try:
        cluster_map = cluster_extracted_data(extracted_data)
        current_app.config['CLUSTERED_DATA'] = cluster_map

        # ایندکس کردن داده‌های کلاستر شده
        es = get_es_client()
        index_name = current_app.config['ELASTICSEARCH_INDEX']

        # حذف ایندکس موجود
        try:
            es.indices.delete(index=index_name)
        except Exception as e:
            logging.error(f"Error deleting index: {str(e)}")

        # ایجاد ایندکس جدید و وارد کردن داده‌ها
        try:
            es.indices.create(index=index_name)
            for key, value in cluster_map.items():
                document = {"cluster": key, "data": value}
                es.index(index=index_name, body=document)
        except Exception as e:
            logging.error(f"Error indexing data: {str(e)}")
            return jsonify({"error": str(e)}), 500

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify(cluster_map)


@cluster.route('/data', methods=['GET'])
def get_clustered_data():
    es = get_es_client()
    index_name = current_app.config['ELASTICSEARCH_INDEX']

    try:
        response = es.search(index=index_name, body={"query": {"match_all": {}}})
        return jsonify(response['hits']['hits']), 200
    except Exception as e:
        logging.error(f"Error retrieving data: {str(e)}")
        return jsonify({"error": str(e)}), 500
