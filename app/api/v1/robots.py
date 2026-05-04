"""Robots Endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_robot_service, get_current_user
from app.services.robot_service import RobotService
from app.schemas.robot import RobotCreate, RobotResponse

router = APIRouter(prefix="/robots", tags=["Robots"])


@router.post(
    "/",
    response_model=RobotResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create robot",
    description="Register a new robot for testing",
)
async def create_robot(
    robot_data: RobotCreate,
    robot_service: RobotService = Depends(get_robot_service),
    _current_user: dict = Depends(get_current_user),
):
    """Create a new robot (authentication required)"""
    try:
        return robot_service.create_robot(robot_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/",
    response_model=List[RobotResponse],
    summary="List robots",
    description="Get all registered robots",
)
async def list_robots(
    robot_service: RobotService = Depends(get_robot_service),
    _current_user: dict = Depends(get_current_user),
):
    """List all robots (authentication required)"""
    return robot_service.get_all_robots()


@router.get(
    "/{robot_id}",
    response_model=RobotResponse,
    summary="Get robot by ID",
    description="Get sepcific robot details",
)
async def get_robot(
    robot_id: int,
    robot_service: RobotService = Depends(get_robot_service),
    _current_user: dict = Depends(get_current_user),
):
    """Get robot by ID (authentication required)"""
    robot = robot_service.get_robot(robot_id)
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found"
        )
    return robot


@router.patch(
    "/{robot_id}/status",
    response_model=RobotResponse,
    summary="Update robot status",
    description="Update robot status (online/offline/busy)",
)
async def update_robot_status(
    robot_id: int,
    status: str,
    robot_service: RobotService = Depends(get_robot_service),
    _current_user: dict = Depends(get_current_user),
):
    """Update robot status (authentication required)"""
    robot = robot_service.update_robot_status(robot_id, status)
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot


@router.delete(
    "/{robot_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete robot",
    description="Remove a robot from the system",
)
async def delete_robot(
    robot_id: int,
    robot_service: RobotService = Depends(get_robot_service),
    _current_user: dict = Depends(get_current_user),
):
    """Delete robot (authentication required)"""
    if not robot_service.delete_robot(robot_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found"
        )
