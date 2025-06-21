
from flask import Flask
from flask_jwt_extended import JWTManager
from routes import bp
from auth import login
import logging

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)

app.register_blueprint(bp, url_prefix='/api')

@app.route('/login', methods=['POST'])
def login_route():
    return login()

@app.errorhandler(404)
def not_found(e):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def server_error(e):
    return {'error': 'Server error'}, 500

logging.basicConfig(level=logging.INFO, filename='app.log',
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
