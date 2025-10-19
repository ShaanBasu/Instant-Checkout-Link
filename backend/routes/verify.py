# ============================================
# FILE: backend/routes/verify.py
# ============================================
"""
Route: GET /api/verify

Verifies if a transaction was confirmed on blockchain
"""

from flask import Blueprint, request, jsonify
from backend.database.links import get_link, update_link_status
from backend.utils.algorand import algod_client

verify_bp = Blueprint('verify', __name__)


@verify_bp.route('/api/verify', methods=['GET'])
def verify_payment():
    """
    Verifies transaction was confirmed on blockchain
    
    Query params:
        ?txid=ABC123TRANSACTION
        ?link_id=abc123xy (optional, to update database)
    
    Response:
    {
        "success": true,
        "status": "confirmed",
        "amount": 1.5,
        "sender": "5U4D...",
        "receiver": "RECV...",
        "confirmed_round": 12345678
    }
    """
    try:
        # Get transaction ID
        txid = request.args.get('txid')
        link_id = request.args.get('link_id')
        
        if not txid:
            return jsonify({
                'success': False,
                'error': 'txid query parameter required'
            }), 400
        
        # Query blockchain for transaction
        try:
            pending_txn = algod_client.pending_transaction_info(txid)
            
            if pending_txn['confirmed-round'] is not None:
                # Transaction was confirmed!
                tx_details = pending_txn['txn']['txn']
                
                result = {
                    'success': True,
                    'status': 'confirmed',
                    'confirmed_round': pending_txn['confirmed-round'],
                    'amount': tx_details.get('amt', 0) / 1_000_000,  # Convert to ALGO
                    'sender': tx_details.get('snd', 'unknown'),
                    'receiver': tx_details.get('rcv', 'unknown'),
                    'fee': tx_details.get('fee', 1000) / 1_000_000,  # Convert to ALGO
                    'transaction_id': txid
                }
                
                # Update database if link_id provided
                if link_id:
                    update_link_status(link_id, 'confirmed', txid)
                
                return jsonify(result), 200
            else:
                # Transaction still pending
                return jsonify({
                    'success': True,
                    'status': 'pending',
                    'message': 'Transaction submitted, waiting for confirmation',
                    'transaction_id': txid
                }), 200
        
        except Exception as e:
            # Transaction not found
            return jsonify({
                'success': False,
                'status': 'not_found',
                'error': 'Transaction not found on blockchain',
                'details': str(e)
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500