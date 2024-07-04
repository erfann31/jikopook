import logging
import os

from app import create_app
from flask_cors import CORS

from app.config import Config

app = create_app()
CORS(app)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    es_cloud_id = Config.ELASTICSEARCH_CLOUD_ID
    es_api_key = Config.ELASTICSEARCH_API_KEY
    if not es_cloud_id or not es_api_key:
        logging.error("Elasticsearch Cloud ID or API Key environment variables not set.")
        exit(1)
    else:
        logging.info(f"Elasticsearch Cloud ID is set.")
    app.run()
