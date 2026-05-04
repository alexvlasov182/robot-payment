"""Terminal service"""

import asyncio
from typing import Dict


class TerminalService:
    """Service for terminal testing simulation"""

    async def test_terminal(self, terminal_id: int, amount: float, method: str) -> Dict:
        """Simulate testing a payment terminal"""
        # Simulate robot movement and payment processing
        await asyncio.sleep(0.5)

        return {
            "terminal_id": terminal_id,
            "amount": amount,
            "method": method,
            "status": "approved",
            "response_time_ms": 500,
            "message": f"Payment of ${amount} via {method} approved",
        }

    def get_mcdonalds_test(self) -> Dict:
        """Mock McDonalds's terminal test"""
        return {
            "merchant": "McDonald's",
            "terminal_model": "Verifone V200c",
            "test_results": {
                "tap_payment": "passed",
                "chip_payment": "passed",
                "pin_entry": "passed",
            },
            "success_rate": "100%",
        }

    def get_grocery_regression(self) -> Dict:
        """Mock grocery store regression test"""
        return {
            "merchant": "Migros",
            "test_run": 50,
            "passed": 48,
            "failed": 2,
            "success_rate": "96%",
        }
