"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.settings import settings
from presentation.api.routes import projects, timeline, effects, export, media

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    Visual Editing Web App - MVP

    A video editing API built with Domain-Driven Design and Clean Architecture.

    ## Features

    * **Projects**: Create and manage video editing projects
    * **Timeline**: Add and manage layers (video, image, audio)
    * **Effects**: Apply built-in effects to layers (blur, brightness, vintage, etc.)
    * **Export**: Export projects to video files (MP4, MOV, AVI, WEBM, GIF)

    ## Architecture

    Built with 4 architectural layers:
    - **Presentation Layer**: FastAPI endpoints
    - **Application Layer**: Use cases and business logic orchestration
    - **Domain Layer**: Core business entities and logic
    - **Infrastructure Layer**: External services (storage, media processing)

    ## Tech Stack

    - FastAPI for REST API
    - FFmpeg for video processing
    - OpenCV for image processing
    - Domain-Driven Design principles
    - Clean Architecture patterns
    """,
    debug=settings.debug
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router, prefix=settings.api_v1_prefix)
app.include_router(timeline.router, prefix=settings.api_v1_prefix)
app.include_router(effects.router, prefix=settings.api_v1_prefix)
app.include_router(export.router, prefix=settings.api_v1_prefix)
app.include_router(media.router, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "description": "Visual Editing Web App - MVP",
        "docs": "/docs",
        "api": settings.api_v1_prefix
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.app_version
    }


# Exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
