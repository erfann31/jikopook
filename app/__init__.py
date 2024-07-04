import os

from flask import Flask

from app.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    app.config['EXTRACTED_DATA'] = {}
    app.config['ELASTICSEARCH_CLOUD_ID'] = Config.ELASTICSEARCH_CLOUD_ID
    app.config['ELASTICSEARCH_API_KEY'] = Config.ELASTICSEARCH_API_KEY
    app.config['ELASTICSEARCH_INDEX'] = 'extracted_data'

    from .routes.init import init as init_blueprint
    app.register_blueprint(init_blueprint, url_prefix='')

    from .routes.links import links as links_blueprint
    app.register_blueprint(links_blueprint, url_prefix='/api/links')

    from .routes.extract import extract as extract_blueprint
    app.register_blueprint(extract_blueprint, url_prefix='/api/extract')

    from .routes.cluster import cluster as cluster_blueprint
    app.register_blueprint(cluster_blueprint, url_prefix='/api/cluster')

    from .routes.find_links import find_links as find_links_blueprint
    app.register_blueprint(find_links_blueprint, url_prefix='/api/find-links')

    from .routes.search import search as search_blueprint
    app.register_blueprint(search_blueprint, url_prefix='/api/search')

    return app
