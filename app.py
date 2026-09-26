from flask import Flask
from src.routes.reservas_routes import reservas_bp
from src.routes.socios_routes import socios_bp
from src.routes.deportes_routes import deportes_bp
from src.routes.canchas_routes import canchas_bp
from src.routes.bloqueos_routes import bloqueos_bp
app = Flask(__name__)

app.register_blueprint(reservas_bp)
app.register_blueprint(socios_bp)
app.register_blueprint(deportes_bp)
app.register_blueprint(canchas_bp)
app.register_blueprint(bloqueos_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
