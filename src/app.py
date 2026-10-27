from flask import Flask, jsonify, request
from flask_cors import CORS
from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp
from blueprints.administrativos.routes import administrativos_bp
from config import config
from database import mysql 

app = Flask(__name__)

app.config.from_object(config['development'])

mysql.init_app(app)

app.register_blueprint(alumnos_bp)
app.register_blueprint(maestros_bp)
app.register_blueprint(administrativos_bp)

CORS(app)

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>"

app.register_error_handler(404, pagina_no_encontrada)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)