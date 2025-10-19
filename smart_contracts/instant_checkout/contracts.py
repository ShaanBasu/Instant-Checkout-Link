# ============================================
# FILE: smart_contracts/instant_checkout/contract.py
# ============================================
"""
Instant Checkout Link Smart Contract
Runs on Algorand blockchain
Handles payments, tracking, and verification
"""

from beaker import Application, GlobalState, LocalState, external, internal
from pyteal import *

# Create the application
app = Application(name="InstantCheckoutLink")
