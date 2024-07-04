import logging

from flask import Blueprint, request, jsonify, current_app

from app.utils.extract import extract_links_and_texts

extract = Blueprint('extract', __name__)


@extract.route('/data', methods=['GET'])
def get_extracted_data():
    return jsonify(current_app.config['EXTRACTED_DATA'])


@extract.route('/', methods=['POST'])
def extract_data():
    data = request.get_json()
    link = data.get('link')
    if not link:
        logging.error("Link is required")
        return jsonify({"error": "Link is required"}), 400

    texts_and_links = extract_links_and_texts(link)
    if texts_and_links is None:
        logging.error("Failed to retrieve the content from the link")
        return jsonify({"error": "Failed to retrieve the content"}), 500

    # Store the extracted data in the EXTRACTED_DATA map
    current_app.config['EXTRACTED_DATA'][link] = texts_and_links

    return jsonify(texts_and_links)
