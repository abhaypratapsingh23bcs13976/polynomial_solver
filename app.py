from flask import Flask, jsonify, redirect
from flask_cors import CORS
from flasgger import Swagger
from routes.solver import solver_bp
from utils.logger import logger

def create_app():
    app = Flask(__name__)
    CORS(app) # Enable CORS for frontend interaction

    # Swagger configuration
    app.config['SWAGGER'] = {
        'title': 'Polynomial Equation Solver API',
        'uiversion': 3,
        'description': 'A production-ready API to solve polynomial equations and visualize results.',
    }
    Swagger(app)

    # Register Blueprints
    app.register_blueprint(solver_bp, url_prefix='/api')

    @app.route('/')
    def index():
        return redirect('/static/index.html')

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal Server Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("Starting Polynomial Solver API...")
    app.run(host='0.0.0.0', port=5000, debug=True)
