
# ============================================
# FILE: backend/utils/contract_client.py
# ============================================
"""
Client for interacting with the smart contract on blockchain
"""

from algosdk.v2client import algod
from algosdk.account import Account
from algosdk.mnemonic import to_private_key
from algosdk import transaction
import os
from dotenv import load_dotenv

load_dotenv()


class CheckoutContractClient:
    """Wrapper for smart contract interactions"""
    
    def __init__(self, app_id: int = None):
        """Initialize contract client"""
        
        # Connect to Algorand testnet
        self.algod_client = algod.AlgodClient(
            token='',
            address='https://testnet-api.algonode.cloud'
        )
        
        self.app_id = app_id or int(os.getenv('APP_ID', 0))
        
        if not self.app_id:
            print("⚠️  Warning: APP_ID not set. Contract calls will fail.")
            print("Please deploy contract first and set APP_ID in .env")
    
    
    def call_process_payment(
        self,
        payment_amount: int,
        receiver_address: str,
        link_id: str,
        sender_address: str,
        sender_mnemonic: str
    ):
        """
        Call smart contract to process payment
        
        Args:
            payment_amount: Amount in microAlgos
            receiver_address: Who receives payment
            link_id: Donation link ID
            sender_address: Who sends payment
            sender_mnemonic: Sender's mnemonic for signing
        """
        try:
            if not self.app_id:
                return {
                    'success': False,
                    'error': 'Contract not deployed. Set APP_ID in .env'
                }
            
            # Get sender's private key
            sender_private_key = to_private_key(sender_mnemonic)
            
            # Get current params
            params = self.algod_client.suggested_params()
            
            # Create transaction
            # This would call process_payment method
            # For MVP, you can use a simple payment transaction
            
            # Simple payment (for MVP without full contract integration)
            txn = transaction.PaymentTxn(
                sender=sender_address,
                index=0,
                sp=params,
                receiver=receiver_address,
                amt=payment_amount
            )
            
            # Sign transaction
            signed_txn = txn.sign(sender_private_key)
            
            # Send to blockchain
            txid = self.algod_client.send_transaction(signed_txn)
            
            return {
                'success': True,
                'transaction_id': txid,
                'amount': payment_amount / 1_000_000,
                'receiver': receiver_address
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    
    def get_contract_stats(self):
        """Get contract statistics from blockchain"""
        try:
            if not self.app_id:
                return {
                    'total_algo_received': 0,
                    'total_payments_processed': 0,
                    'contract_version': '1.0'
                }
            
            # Get application info
            app_info = self.algod_client.application_info(self.app_id)
            
            # Extract global state
            global_state = app_info['params']['global-state']
            
            total_received = 0
            total_payments = 0
            
            for state in global_state:
                key = state['key']
                value = state['value']['uint']
                
                # Parse state keys
                if key == 'dHJzZQ==':  # "trse" in base64
                    total_received = value
                elif key == 'cGNudA==':  # "pcnt" in base64
                    total_payments = value
            
            return {
                'total_algo_received': total_received / 1_000_000,
                'total_payments_processed': total_payments,
                'contract_version': '1.0'
            }
        
        except Exception as e:
            return {
                'total_algo_received': 0,
                'total_payments_processed': 0,
                'contract_version': '1.0',
                'error': str(e)
            }
    
    
    def check_transaction_status(self, txid: str):
        """Check if transaction was confirmed"""
        try:
            txn_info = self.algod_client.pending_transaction_info(txid)
            
            if txn_info['confirmed-round'] is not None:
                return {
                    'status': 'confirmed',
                    'confirmed_round': txn_info['confirmed-round'],
                    'transaction_id': txid
                }
            else:
                return {
                    'status': 'pending',
                    'transaction_id': txid
                }
        
        except Exception as e:
            return {
                'status': 'not_found',
                'error': str(e)
            }