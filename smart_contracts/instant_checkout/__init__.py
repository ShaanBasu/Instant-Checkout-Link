"""Export contract for deployment"""

from smart_contracts.instant_checkout.contract import app, CheckoutState

__all__ = ["app", "CheckoutState"]