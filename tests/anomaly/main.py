from flask import Flask
from flask_cors import CORS
from routes.anomaly_routes import anomaly_routes

app = Flask(__name__)
CORS(app)

app.register_blueprint(anomaly_routes)

if __name__ == "__main__":
    app.run(debug=True, port=5000)