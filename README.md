# Visual Editing Web App - MVP

A professional-grade video editing API built with **Domain-Driven Design (DDD)** and **Clean Architecture** principles. This MVP demonstrates Object-Oriented Programming (OOP) best practices while providing a scalable foundation for a video editing platform.

## Target Users

Content creators (YouTubers, Instagram Reelers, TikTokers) who need quick edits, batch processing, and consistent branding templates.

## Core Value Proposition

Simplify video editing workflow from 2 hours to 15 minutes per reel through templates, batch processing, and streamlined effects.

## Architecture Overview

The application follows a **4-layer Clean Architecture**:

```
┌─────────────────────────────────────┐
│    Presentation Layer (FastAPI)     │  ← API Endpoints, Schemas
├─────────────────────────────────────┤
│    Application Layer (Use Cases)    │  ← Business Logic Orchestration
├─────────────────────────────────────┤
│    Domain Layer (Core Business)     │  ← Entities, Value Objects, Interfaces
├─────────────────────────────────────┤
│    Infrastructure Layer (External)  │  ← Repositories, Storage, FFmpeg
└─────────────────────────────────────┘
```

### Layer Responsibilities

#### 1. Presentation Layer (`presentation/`)
- FastAPI REST endpoints
- Request/Response schemas (Pydantic)
- Dependency injection setup
- HTTP concerns only

#### 2. Application Layer (`application/`)
- Use cases (orchestration)
- DTOs (Data Transfer Objects)
- Application-specific business rules
- Coordinates between domain and infrastructure

#### 3. Domain Layer (`domain/`)
- **Core business logic** (framework-agnostic)
- Entities (Project, Timeline, Layer, MediaAsset)
- Value Objects (Duration, Resolution, Position, Color)
- Domain Services (EffectRegistry)
- Repository interfaces
- **No dependencies on external frameworks**

#### 4. Infrastructure Layer (`infrastructure/`)
- Repository implementations (in-memory, PostgreSQL)
- File storage services
- Media processing (FFmpeg, OpenCV wrappers)
- External service integrations

## Tech Stack

- **Backend**: Python 3.11+
- **Framework**: FastAPI
- **Media Processing**: FFmpeg, OpenCV
- **Database**: In-memory (MVP) / PostgreSQL (production-ready)
- **Architecture**: DDD + Clean Architecture

## Features

### MVP Features

- ✅ **Project Management**: Create, read, delete video editing projects
- ✅ **Timeline Management**: Add layers (video, image, audio) with positioning
- ✅ **Effects System**:
  - Blur effect
  - Brightness adjustment
  - Vintage/Sepia filter
  - Sharpen effect
  - Crop effect
- ✅ **Export**: Render projects to MP4, MOV, AVI, WEBM, GIF
- ✅ **Plugin Architecture**: Extensible effect system via Strategy pattern

### Design Patterns Used

- **Repository Pattern**: Data access abstraction
- **Strategy Pattern**: Pluggable effects system
- **Aggregate Pattern**: Project as aggregate root
- **Factory Pattern**: Entity creation
- **Dependency Injection**: Loose coupling between layers

## Project Structure

```
video-editor/
├── main.py                          # FastAPI entry point
├── requirements.txt
├── README.md
│
├── domain/                          # DOMAIN LAYER (Core Business Logic)
│   ├── media/                       # Media Management Context
│   │   ├── entities/
│   │   │   ├── media_asset.py
│   │   │   └── media_library.py
│   │   └── repositories/
│   │       └── media_asset_repository.py
│   │
│   ├── editing/                     # Editing Context (CORE)
│   │   ├── entities/
│   │   │   ├── timeline.py          # Timeline aggregate
│   │   │   ├── layer.py
│   │   │   └── effect_instance.py
│   │   ├── value_objects/
│   │   │   ├── duration.py
│   │   │   ├── resolution.py
│   │   │   ├── position.py
│   │   │   └── color.py
│   │   ├── interfaces/
│   │   │   └── effect.py            # IEffect interface
│   │   ├── builtin_effects/
│   │   │   ├── blur_effect.py
│   │   │   ├── vintage_filter.py
│   │   │   ├── brightness_effect.py
│   │   │   ├── sharpen_effect.py
│   │   │   └── crop_effect.py
│   │   ├── services/
│   │   │   └── effect_registry.py
│   │   └── repositories/
│   │       └── project_repository.py
│   │
│   ├── shared/
│   │   └── enums.py
│   │
│   └── project/
│       └── project.py               # Project aggregate root
│
├── application/                     # APPLICATION LAYER (Use Cases)
│   ├── use_cases/
│   │   ├── project/
│   │   │   ├── create_project.py
│   │   │   └── get_project.py
│   │   ├── editing/
│   │   │   ├── add_layer_to_timeline.py
│   │   │   └── apply_effect_to_layer.py
│   │   └── export/
│   │       └── export_project.py
│   │
│   └── dtos/
│       ├── project_dto.py
│       └── layer_dto.py
│
├── infrastructure/                  # INFRASTRUCTURE LAYER
│   ├── persistence/
│   │   └── in_memory/
│   │       ├── project_repository_impl.py
│   │       └── media_asset_repository_impl.py
│   │
│   ├── storage/
│   │   └── file_storage_service.py
│   │
│   └── media_processing/
│       ├── video_processor.py       # FFmpeg wrapper
│       ├── image_processor.py       # OpenCV wrapper
│       └── ffmpeg_exporter.py
│
├── presentation/                    # PRESENTATION LAYER (API)
│   ├── api/
│   │   ├── routes/
│   │   │   ├── projects.py
│   │   │   ├── timeline.py
│   │   │   ├── effects.py
│   │   │   └── export.py
│   │   └── dependencies.py
│   │
│   └── schemas/
│       ├── project_schema.py
│       ├── media_schema.py
│       └── effect_schema.py
│
└── config/
    └── settings.py
```

## Installation

### Prerequisites

1. **Python 3.11+**
   ```bash
   python --version  # Should be 3.11 or higher
   ```

2. **FFmpeg** (required for video processing)
   ```bash
   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install ffmpeg

   # macOS
   brew install ffmpeg

   # Windows
   # Download from https://ffmpeg.org/download.html
   ```

3. **Verify FFmpeg installation**
   ```bash
   ffmpeg -version
   ffprobe -version
   ```

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Visual-Editing-Web-App
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   ```bash
   cp .env.example .env
   ```

5. **Run the application**
   ```bash
   python main.py
   ```

   Or with uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API**
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

## API Usage

### Example Workflow

#### 1. Create a Project
```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Instagram Reel",
    "description": "Fitness motivation reel",
    "resolution_width": 1080,
    "resolution_height": 1920,
    "fps": 30.0
  }'
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "My Instagram Reel",
  "description": "Fitness motivation reel",
  "status": "draft",
  "resolution_width": 1080,
  "resolution_height": 1920,
  "fps": 30.0,
  "layer_count": 0,
  "total_duration": 0.0
}
```

#### 2. List Available Effects
```bash
curl "http://localhost:8000/api/v1/effects"
```

#### 3. Add a Layer to Timeline
```bash
curl -X POST "http://localhost:8000/api/v1/projects/{project_id}/timeline/layers" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Main Video",
    "layer_type": "video",
    "start_time": 0.0,
    "duration": 15.5,
    "media_asset_id": "asset-id-here",
    "position_x": 0.0,
    "position_y": 0.0
  }'
```

#### 4. Apply Effect to Layer
```bash
curl -X POST "http://localhost:8000/api/v1/projects/{project_id}/layers/{layer_id}/effects" \
  -H "Content-Type: application/json" \
  -d '{
    "effect_name": "blur",
    "parameters": {
      "kernel_size": 21,
      "sigma": 0
    }
  }'
```

#### 5. Export Project
```bash
curl -X POST "http://localhost:8000/api/v1/projects/{project_id}/export" \
  -H "Content-Type: application/json" \
  -d '{
    "output_filename": "my_reel.mp4",
    "format": "mp4"
  }'
```

## Development

### Running Tests
```bash
pytest tests/
```

### Code Formatting
```bash
black .
```

### Type Checking
```bash
mypy .
```

### Linting
```bash
flake8 .
```

## Domain-Driven Design Concepts

### Bounded Contexts

1. **Media Management Context**: Handles media assets (videos, images, audio)
2. **Editing Context**: Core domain - timeline, layers, effects
3. **Project Context**: Project aggregate root

### Entities vs Value Objects

**Entities** (have identity):
- Project
- MediaAsset
- Layer
- EffectInstance

**Value Objects** (immutable, no identity):
- Duration
- Resolution
- Position
- Color

### Aggregates

**Project Aggregate**:
- Root: Project
- Contains: Timeline → Layers → Effects
- Enforces: Consistency boundaries

## Extensibility

### Adding a New Effect

1. Create effect class implementing `IEffect`:
```python
# domain/editing/builtin_effects/my_effect.py
from domain.editing.interfaces.effect import IEffect

class MyEffect(IEffect):
    @property
    def name(self) -> str:
        return "my_effect"

    @property
    def description(self) -> str:
        return "My custom effect"

    def get_default_parameters(self) -> Dict[str, Any]:
        return {"intensity": 1.0}

    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        # Validation logic
        return True

    def apply(self, frame: np.ndarray, parameters: Dict[str, Any]) -> np.ndarray:
        # Effect implementation
        return processed_frame
```

2. Register in EffectRegistry:
```python
# domain/editing/services/effect_registry.py
from domain.editing.builtin_effects.my_effect import MyEffect

def _register_builtin_effects(self):
    # ... existing effects
    self.register(MyEffect())
```

### Adding Database Persistence

1. Implement `IProjectRepository` for PostgreSQL:
```python
# infrastructure/persistence/postgres/project_repository_impl.py
class PostgresProjectRepository(IProjectRepository):
    async def save(self, project: Project) -> Project:
        # PostgreSQL implementation
        pass
```

2. Update dependency injection in `presentation/api/dependencies.py`

## Future Enhancements

- [ ] File upload API for media assets
- [ ] PostgreSQL persistence layer
- [ ] Batch processing for multiple videos
- [ ] Template system for consistent branding
- [ ] Real-time preview generation
- [ ] Video transitions between layers
- [ ] Text overlay layers
- [ ] Audio mixing and normalization
- [ ] Cloud storage integration (S3, Google Cloud Storage)
- [ ] Background job processing (Celery)
- [ ] WebSocket support for real-time updates

## License

MIT License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Follow DDD and Clean Architecture principles
4. Write tests for new features
5. Submit a pull request

## Support

For issues and questions, please open a GitHub issue.

---

**Built with Domain-Driven Design and Clean Architecture**

Demonstrating professional software engineering practices for scalable, maintainable applications.
