from uuid import UUID

from src.adapters.postgres.postgres_project_repository import PostgresProjectRepository
from tests.mocks import project_mock


project_repository = PostgresProjectRepository()


if __name__ == '__main__':
    project = project_mock.get_valid_project()
    project.name = "using repository"
    project.created_by.id = UUID("b315b9a7-8f81-4436-b557-bfb01330e8d5")
    project.updated_by.id = UUID("b315b9a7-8f81-4436-b557-bfb01330e8d5")
    project.workspace.id = UUID("f5b9b673-e166-417e-b1a7-5d9f325ce597")
    project_repository.create(project)

