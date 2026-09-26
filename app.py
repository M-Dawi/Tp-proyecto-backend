from flask import Flask
from src.routes.reservas_routes import reservas_bp
from src.routes.socios_routes import socios_bp
from src.routes.deportes_routes import deportes_bp
app = Flask(__name__)

app.register_blueprint(reservas_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(deportes_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
