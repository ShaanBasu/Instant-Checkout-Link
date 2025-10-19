# ============================================
# FILE: backend/routes/pay.py
# ============================================
"""
Route: GET /api/pay/:link_id

Retrieves payment link details and creates transaction
"""

from flask import Blueprint, request, jsonify
from backend.database.links import get_link, update_link_status, increment_click_count
from backend.utils.algorand import is_valid_address
import base64
import json

pay_bp = Blueprint('pay', __name__)


@pay_bp.route('/api/pay/<link_id>', methods=['GET'])
def get_payment_link(link_id):
    """
    Retrieves payment details for a checkout link
    
    Query params:
        ?user_address=SENDERADDRESS
    
    Response:
    {
        "success": true,
        "amount": 1.5,
        "receiver": "5U4DPE...",
        "sender": "user_address",
        "deep_link": "algorand://sign?txn=...",
        "transaction_id": "ABC123"
    }
    """
    try:
        # Get sender address from query params
        sender_address = request.args.get('user_address')
        
        if not sender_address:
            return jsonify({
                'success': False,
                'error': 'user_address query parameter required'
            }), 400
        
        if not is_valid_address(sender_address):
            return jsonify({
                'success': False,
                'error': 'Invalid sender address'
            }), 400
        
        # Look up link from database
        link_data = get_link(link_id)
        
        if not link_data:
            return jsonify({
                'success': False,
                'error': 'Checkout link not found'
            }), 404
        
        if link_data['status'] == 'confirmed':
            return jsonify({
                'success': False,
                'error': 'This link has already been used'
            }), 410
        
        # Track that someone clicked this link
        increment_click_count(link_id)
        
        # For MVP: Return simple transaction details
        # Later: Build unsigned transaction with smart contract
        
        return jsonify({
            'success': True,
            'amount': link_data['amount'],
            'receiver': link_data['receiver'],
            'sender': sender_address,
            'link_id': link_id,
            'description': link_data['description'],
            'deep_link': f"algorand://send?receiver={link_data['receiver']}&amount={int(link_data['amount'] * 1_000_000)}",
            'transaction_id': None
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get payment details: {str(e)}'
        }), 500
