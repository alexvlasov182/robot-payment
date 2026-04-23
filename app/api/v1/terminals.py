from fastapi import APIRouter
import asyncio


router = APIRouter(prefix="/terminals", tags=["Terminals"])


@router.post("/test")
async def test_terminal(terminal_id: int, amount: float, payment_method: str = "tap"):
    await asyncio.sleep(0.5)  # simulate robot moving
    return {
        "terminal_id": terminal_id,
        "amount": amount,
        "method": payment_method,
        "status": "approved",
        "response_time_ms": 500,
    }


@router.get("/mcdonalds")
def mcdonalds_test():
    return {"merchant": "McDonald's", "result": "passed"}


@router.get("/grocery/regresssion")
def grocery_regression():
    return {"merchant": "Migros", "tests_run": 50, "passed": 48}
