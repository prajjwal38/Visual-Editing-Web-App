"""In-memory implementation of Project Repository."""
from typing import Dict, List, Optional
import copy

from domain.project.project import Project
from domain.editing.repositories.project_repository import IProjectRepository


class InMemoryProjectRepository(IProjectRepository):
    """In-memory implementation of IProjectRepository.

    Infrastructure layer - concrete implementation.
    Suitable for MVP, testing, and development.
    """

    def __init__(self):
        self._storage: Dict[str, Project] = {}

    async def save(self, project: Project) -> Project:
        """Save a project.

        Args:
            project: Project to save

        Returns:
            Saved project
        """
        # Deep copy to simulate database persistence
        self._storage[project.id] = copy.deepcopy(project)
        return copy.deepcopy(project)

    async def find_by_id(self, project_id: str) -> Optional[Project]:
        """Find a project by ID.

        Args:
            project_id: ID of the project

        Returns:
            Project or None if not found
        """
        project = self._storage.get(project_id)
        if project:
            return copy.deepcopy(project)
        return None

    async def find_all(self) -> List[Project]:
        """Find all projects.

        Returns:
            List of all projects
        """
        return [copy.deepcopy(project) for project in self._storage.values()]

    async def delete(self, project_id: str) -> bool:
        """Delete a project.

        Args:
            project_id: ID of the project to delete

        Returns:
            True if deleted, False if not found
        """
        if project_id in self._storage:
            del self._storage[project_id]
            return True
        return False

    async def exists(self, project_id: str) -> bool:
        """Check if a project exists.

        Args:
            project_id: ID of the project

        Returns:
            True if exists, False otherwise
        """
        return project_id in self._storage

    def clear(self) -> None:
        """Clear all projects (useful for testing)."""
        self._storage.clear()
