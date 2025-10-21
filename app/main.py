from flask import Flask
from app.cliente_routes import cliente_bp

app = Flask(__name__)

app.register_blueprint(cliente_bp)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)