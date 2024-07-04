from flask import Blueprint

init = Blueprint('init', __name__)


@init.route('/')
def initialize():
    return "Welcome To Jikopook!"
