from flask import Blueprint, request, jsonify, current_app

find_links = Blueprint('find_links', __name__)


@find_links.route('/', methods=['POST'])
def get_clustered_links():
    data = request.get_json()
    clustered_texts = data.get('texts')
    if not clustered_texts:
        return jsonify({"error": "Texts are required"}), 400

    extracted_data = current_app.config['EXTRACTED_DATA']
    result_links = {}

    for text in clustered_texts:
        found = False
        for site, links in extracted_data.items():
            if text in links:
                result_links[text] = links[text]
                found = True
                break
        if not found:
            result_links[text] = None

    return jsonify(result_links)
