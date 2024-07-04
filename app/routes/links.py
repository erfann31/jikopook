from flask import Blueprint, jsonify, request, current_app

links = Blueprint('links', __name__)


@links.route('/', methods=['GET'])
def get_links():
    links = current_app.config['LINKS']
    return jsonify(links)


@links.route('/', methods=['POST'])
def add_link():
    data = request.get_json()
    new_link = data.get('link')
    if new_link:
        current_app.config['LINKS'].append(new_link)
        return jsonify({"message": "Link added successfully!"}), 201
    else:
        return jsonify({"error": "Invalid input"}), 400


@links.route('/', methods=['DELETE'])
def delete_link():
    data = request.get_json()
    link_to_delete = data.get('link')
    if link_to_delete in current_app.config['LINKS']:
        current_app.config['LINKS'].remove(link_to_delete)
        return jsonify({"message": "Link deleted successfully!"}), 200
    else:
        return jsonify({"error": "Link not found"}), 404
