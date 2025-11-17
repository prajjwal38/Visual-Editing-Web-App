"""Project Repository interface."""
from abc import ABC, abstractmethod
from typing import List, Optional


class IProjectRepository(ABC):
    """Repository interface for Project aggregate.

    Following repository pattern from DDD.
    Infrastructure layer will provide concrete implementations.
    """

    @abstractmethod
    async def save(self, project) -> any:
        """Save a project."""
        pass

    @abstractmethod
    async def find_by_id(self, project_id: str) -> Optional[any]:
        """Find a project by ID."""
        pass

    @abstractmethod
    async def find_all(self) -> List[any]:
        """Find all projects."""
        pass

    @abstractmethod
    async def delete(self, project_id: str) -> bool:
        """Delete a project."""
        pass

    @abstractmethod
    async def exists(self, project_id: str) -> bool:
        """Check if a project exists."""
        pass
