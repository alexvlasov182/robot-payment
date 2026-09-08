"""Robots Endpoints"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user, get_robot_service
from app.models.user import User
from app.schemas.robot import RobotCreate, RobotResponse, RobotUpdate
from app.services.robot_service import RobotService

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
    current_user: User = Depends(get_current_user),
):
    """Create a new robot (authentication required)"""
    try:
        return robot_service.create_robot(robot_data, current_user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.get(
    "/",
    response_model=list[RobotResponse],
    summary="List robots",
    description="Get all registered robots",
)
async def list_robots(
    robot_service: RobotService = Depends(get_robot_service),
    current_user: User = Depends(get_current_user),
):
    """List all robots owned by current user (authentication required)"""
    return robot_service.get_all_robots(current_user)


@router.get(
    "/{robot_id}",
    response_model=RobotResponse,
    summary="Get robot by ID",
    description="Get specific robot details",
)
async def get_robot(
    robot_id: int,
    robot_service: RobotService = Depends(get_robot_service),
    current_user: User = Depends(get_current_user),
):
    """Get robot by ID (authentication required, must be owner)"""
    robot = robot_service.get_robot(robot_id, current_user)
    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found"
        )
    return robot


@router.put(
    "/{robot_id}",
    response_model=RobotResponse,
    summary="Update robot",
    description="Update robot information",
)
async def update_robot(
    robot_id: int,
    robot_data: RobotUpdate,
    robot_service: RobotService = Depends(get_robot_service),
    current_user: User = Depends(get_current_user),
):
    """Update robot (authentication required, must be owner)"""

    robot = robot_service.update_robot(robot_id, robot_data, current_user)

    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )

    return robot


@router.patch(
    "/{robot_id}/status",
    response_model=RobotResponse,
    summary="Update robot status",
)
async def update_robot_status(
    robot_id: int,
    robot_data: RobotUpdate,
    robot_service: RobotService = Depends(get_robot_service),
    current_user: User = Depends(get_current_user),
):
    robot = robot_service.update_robot_status(robot_id, robot_data, current_user)

    if not robot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Robot not found",
        )

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
    current_user: User = Depends(get_current_user),
):
    """Delete robot (authentication required, must be owner)"""
    if not robot_service.delete_robot(robot_id, current_user):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Robot not found"
        )
