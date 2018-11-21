

from flask import Flask, jsonify

app = Flask(__name__)


app.config.from_object("project.config.DevelopmentConfig")


@app.route("/users/ping", methods=['GET'])
def ping_pong():
    return jsonify({
        'estado': 'satisfactorio',
        'mensaje': 'pong!!!'
    })
