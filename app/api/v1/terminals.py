"""Terminals API"""

from fastapi import APIRouter, Depends
from app.api.dependencies import get_terminal_service
from app.services.terminal_services import TerminalService
from app.schemas.terminal import TerminalTestRequest, TerminalTestResponse

router = APIRouter(prefix="/terminals", tags=["Terminals"])


@router.post(
    "/test",
    response_model=TerminalTestResponse,
    summary="Test payment terminal",
    description="Simulate testing a payment terminal with robot",
)
async def test_terminal(
    request: TerminalTestRequest,
    terminal_service: TerminalService = Depends(get_terminal_service),
):
    """Test a payment terminal"""
    result = await terminal_service.test_terminal(
        request.terminal_id, request.amount, request.payment_method
    )
    return TerminalTestResponse(**result)


@router.get(
    "/mcdonalds",
    summary="McDonald's terminal test",
    description="Quick test for McDonald's terminals",
)
async def test_mcdonalds(
    terminal_service: TerminalService = Depends(get_terminal_service),
):
    """Test McDonald's terminal configuration"""
    return terminal_service.get_mcdonalds_test()


@router.get(
    "/grocery/regression",
    summary="Grocery store regression",
    description="Full regression test for grocery stores",
)
async def grocery_regression(
    terminal_service: TerminalService = Depends(get_terminal_service),
):
    """Run grocery store regression tests"""
    return terminal_service.get_grocery_regression()
