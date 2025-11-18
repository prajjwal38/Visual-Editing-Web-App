"""Project API routes."""
from fastapi import APIRouter, HTTPException, Depends
from typing import List

from presentation.schemas.project_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProjectResponse,
    ResolutionSchema,
    TimelineSchema,
    DurationSchema
)
from presentation.api.dependencies import (
    get_create_project_use_case,
    get_get_project_use_case,
    get_project_repository
)
from application.dtos.project_dto import CreateProjectDTO, UpdateProjectDTO

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    request: ProjectCreateRequest,
    use_case=Depends(get_create_project_use_case)
):
    """Create a new project.

    Creates a new video editing project with specified settings.
    """
    try:
        dto = CreateProjectDTO(
            name=request.name,
            description=request.description,
            resolution_width=request.resolution.width,
            resolution_height=request.resolution.height,
            fps=request.fps
        )

        result = await use_case.execute(dto)

        return ProjectResponse(
            id=result.id,
            name=result.name,
            description=result.description,
            status=result.status,
            resolution=ResolutionSchema(
                width=result.resolution_width,
                height=result.resolution_height
            ),
            fps=result.fps,
            created_at=result.created_at,
            updated_at=result.updated_at,
            timeline=TimelineSchema(
                layers=[],
                total_duration=DurationSchema(seconds=result.total_duration)
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    use_case=Depends(get_get_project_use_case)
):
    """Get a project by ID.

    Retrieves project details including timeline information.
    """
    try:
        result = await use_case.execute(project_id)

        if not result:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        return ProjectResponse(
            id=result.id,
            name=result.name,
            description=result.description,
            status=result.status,
            resolution=ResolutionSchema(
                width=result.resolution_width,
                height=result.resolution_height
            ),
            fps=result.fps,
            created_at=result.created_at,
            updated_at=result.updated_at,
            timeline=TimelineSchema(
                layers=[],
                total_duration=DurationSchema(seconds=result.total_duration)
            )
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    repository=Depends(get_project_repository)
):
    """List all projects.

    Returns a list of all video editing projects.
    """
    try:
        projects = await repository.find_all()

        return [
            ProjectResponse(
                id=project.id,
                name=project.name,
                description=project.description,
                status=project.status,
                resolution=ResolutionSchema(
                    width=project.timeline.resolution.width,
                    height=project.timeline.resolution.height
                ),
                fps=project.timeline.fps,
                created_at=project.created_at,
                updated_at=project.updated_at,
                timeline=TimelineSchema(
                    layers=[],
                    total_duration=DurationSchema(
                        seconds=project.timeline.calculate_total_duration().seconds
                    )
                )
            )
            for project in projects
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: str,
    repository=Depends(get_project_repository)
):
    """Delete a project.

    Permanently deletes a project and all its data.
    """
    try:
        deleted = await repository.delete(project_id)

        if not deleted:
            raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
