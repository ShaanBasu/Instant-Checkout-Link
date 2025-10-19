# ============================================
# FILE: backend/routes/create_link.py
# ============================================
"""
Route: POST /api/create-link

Creates a new checkout link that users can share
"""

from flask import Blueprint, request, jsonify
from backend.database.links import create_link
from backend.utils.algorand import is_valid_address
import os

create_link_bp = Blueprint('create_link', __name__)


@create_link_bp.route('/api/create-link', methods=['POST'])
def create_checkout_link():
    """
    Creates a new payment link
    
    Request body:
    {
        "amount": 1.5,
        "receiver_address": "5U4DPE4D5SRTBR36SV2L3MAFZM7VFGN6KQPHKGK4JM7BVGJKMHIKK65I3Y",
        "description": "optional description"
    }
    
    Response:
    {
        "success": true,
        "link_id": "abc123xy",
        "amount": 1.5,
        "checkout_url": "http://localhost:8000?link=abc123xy"
    }
    """
    try:
        # Get data from request
        data = request.get_json()
        
        # Validate data exists
        if not data:
            return jsonify({
                'success': False,
                'error': 'No JSON data provided'
            }), 400
        
        # Extract fields
        amount = data.get('amount')
        receiver_address = data.get('receiver_address')
        description = data.get('description', '')
        
        # Validate amount
        if amount is None or amount <= 0:
            return jsonify({
                'success': False,
                'error': 'Amount must be positive'
            }), 400
        
        # Validate receiver address
        if not receiver_address:
            return jsonify({
                'success': False,
                'error': 'Receiver address required'
            }), 400
        
        if not is_valid_address(receiver_address):
            return jsonify({
                'success': False,
                'error': 'Invalid Algorand address format'
            }), 400
        
        # Create the link in database
        link_data = create_link(amount, receiver_address, description)
        
        # Build checkout URL
        base_url = os.getenv('BASE_URL', 'http://localhost:8000')
        checkout_url = f"{base_url}?link={link_data['link_id']}"
        
        return jsonify({
            'success': True,
            'link_id': link_data['link_id'],
            'amount': amount,
            'receiver_address': receiver_address,
            'checkout_url': checkout_url,
            'created': link_data['created']
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500