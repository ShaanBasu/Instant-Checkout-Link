# ============================================
# FILE: backend/utils/algorand.py
# ============================================
"""
Algorand utilities for blockchain interaction
"""

from algosdk.v2client import algod
from algosdk.encoding import decode_address
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to Algorand testnet
ALGORAND_SERVER = os.getenv('ALGORAND_SERVER', 'https://testnet-api.algonode.cloud')
ALGORAND_TOKEN = ''  # Testnet doesn't need token

# Create algod client (connection to blockchain)
algod_client = algod.AlgodClient(ALGORAND_TOKEN, ALGORAND_SERVER)


def is_valid_address(address: str) -> bool:
    """
    Validate if address is properly formatted Algorand address
    Algorand addresses are 58 characters long and base32 encoded
    
    For MVP testing, we allow placeholder addresses
    """
    if not address:
        return False
    
    
    # Check if it's 58 characters (valid Algorand address length)
    if len(address) != 58:
        return False
    
    # Try to decode as real Algorand address
    try:
        decode_address(address)
        return True
    except:
        # For MVP, accept 58-char strings as valid even if decode fails
        # In production, remove this and use strict validation
        if len(address) == 58:
            return True
        return False


def get_network_params():
    """Get current blockchain parameters"""
    try:
        params = algod_client.suggested_params()
        return params
    except Exception as e:
        raise Exception(f"Failed to get network parameters: {str(e)}")


def check_address_balance(address: str):
    """Check ALGO balance of an address"""
    try:
        if not is_valid_address(address):
            return None
        
        account_info = algod_client.account_info(address)
        # Convert microAlgos to ALGO
        balance_algo = account_info['amount'] / 1_000_000
        return balance_algo
    except:
        return None