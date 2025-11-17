"""Export API routes."""
from fastapi import APIRouter, HTTPException, Depends

from presentation.schemas.media_schema import ExportRequest, ExportResponse
from presentation.api.dependencies import get_export_project_use_case, get_file_storage
from domain.shared.enums import ExportFormat

router = APIRouter(prefix="/projects/{project_id}", tags=["export"])


@router.post("/export", response_model=ExportResponse)
async def export_project(
    project_id: str,
    request: ExportRequest,
    use_case=Depends(get_export_project_use_case),
    file_storage=Depends(get_file_storage)
):
    """Export a project to video file.

    Renders the project timeline to a video file in the specified format.
    """
    try:
        # Convert format string to enum
        format_map = {
            "mp4": ExportFormat.MP4,
            "mov": ExportFormat.MOV,
            "avi": ExportFormat.AVI,
            "webm": ExportFormat.WEBM,
            "gif": ExportFormat.GIF
        }

        export_format = format_map.get(request.format.lower())
        if not export_format:
            raise ValueError(f"Invalid export format: {request.format}")

        # Get output path
        output_path = file_storage.get_export_path(request.output_filename)

        # Execute export
        result = await use_case.execute(
            project_id=project_id,
            output_path=output_path,
            export_format=export_format
        )

        return ExportResponse(
            output_path=result["output_path"],
            format=result["format"],
            resolution=result["resolution"],
            fps=result["fps"],
            layers_exported=result["layers_exported"]
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
