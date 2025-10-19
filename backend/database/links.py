# ============================================
# FILE: backend/database/links.py
# ============================================
"""
Database for storing checkout links
Uses JSON file for MVP (can upgrade to MongoDB/PostgreSQL later)
"""

import json
import os
from datetime import datetime
import uuid

DATABASE_FILE = 'links_database.json'


def _load_database():
    """Load all links from JSON file"""
    if not os.path.exists(DATABASE_FILE):
        return {}
    
    try:
        with open(DATABASE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}


def _save_database(data):
    """Save all links to JSON file"""
    with open(DATABASE_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def create_link(amount: float, receiver_address: str, description: str = ""):
    """
    Create a new checkout link
    
    Args:
        amount: Amount in ALGO
        receiver_address: Where the payment goes
        description: Optional description
    
    Returns:
        Dictionary with link_id and details
    """
    db = _load_database()
    
    # Generate unique ID
    link_id = str(uuid.uuid4())[:8]
    
    # Store link with metadata
    db[link_id] = {
        'amount': amount,
        'receiver': receiver_address,
        'description': description,
        'created': datetime.now().isoformat(),
        'status': 'unused',  # unused, used, confirmed
        'txid': None,
        'txn_timestamp': None,
        'click_count': 0
    }
    
    _save_database(db)
    
    return {
        'link_id': link_id,
        'amount': amount,
        'receiver': receiver_address,
        'created': db[link_id]['created']
    }


def get_link(link_id: str):
    """Get link details by ID"""
    db = _load_database()
    
    if link_id not in db:
        return None
    
    return db[link_id]


def update_link_status(link_id: str, status: str, txid: str = None):
    """Update link status after transaction"""
    db = _load_database()
    
    if link_id in db:
        db[link_id]['status'] = status
        if txid:
            db[link_id]['txid'] = txid
            db[link_id]['txn_timestamp'] = datetime.now().isoformat()
    
    _save_database(db)


def increment_click_count(link_id: str):
    """Track how many times a link was clicked"""
    db = _load_database()
    
    if link_id in db:
        db[link_id]['click_count'] = db[link_id].get('click_count', 0) + 1
    
    _save_database(db)


def list_links():
    """Get all links (for debugging)"""
    return _load_database()


def delete_link(link_id: str):
    """Delete a link"""
    db = _load_database()
    
    if link_id in db:
        del db[link_id]
        _save_database(db)
        return True
    
    return False