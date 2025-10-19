# ============================================
# FILE: backend/app.py
# ============================================
"""
Main Flask backend application
Connects frontend to smart contract
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Enable CORS - allow frontend to make requests
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "http://localhost:8000",
            "http://localhost:5000",
            "http://localhost:3000"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Import routes
from backend.routes.create_link import create_link_bp
from backend.routes.pay import pay_bp
from backend.routes.verify import verify_bp

# Register blueprints
app.register_blueprint(create_link_bp)
app.register_blueprint(pay_bp)
app.register_blueprint(verify_bp)


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Instant Checkout Link Backend',
        'version': '1.0'
    }), 200


@app.route('/api/contract-stats', methods=['GET'])
def get_contract_stats():
    """Get contract statistics from blockchain"""
    try:
        # For now, return mock data
        # Later: Connect to smart contract client
        return jsonify({
            'success': True,
            'total_algo_received': 0,
            'total_payments_processed': 0,
            'contract_version': '1.0'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', True)
    app.run(host='0.0.0.0', port=port, debug=debug)