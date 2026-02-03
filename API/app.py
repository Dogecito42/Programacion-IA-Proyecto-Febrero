from flask import Flask
from controllers.db_controller import db_bp

app = Flask(__name__)
app.register_blueprint(db_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
