"""Schema for the terminal"""

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt


class TerminalTestRequest(BaseModel):
    """Request schema for terminal test"""

    terminal_id: PositiveInt = Field(..., description="Terminal identifier")
    amount: PositiveFloat = Field(..., description="Payment amount")
    payment_method: str = Field(default="tap", pattern="^(tap|chip|swipe)$")


class TerminalTestResponse(BaseModel):
    """Response schema for terminal test"""

    terminal_id: int
    amount: float
    method: str
    status: str
    response_time_ms: int
    message: str
