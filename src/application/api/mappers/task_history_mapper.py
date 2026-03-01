from typing import Optional

from src.application.api.mappers import uuid_mapper
from src.application.api.mappers.generic_entity_mapper import GenericEntityMapper
from src.application.api.mappers.generic_mapper import GenericMapper, Entity
from src.entities.task import TaskHistory, TaskStatus
from src.entities.user import User
from src.utils import date_utils, enum_utils


class TaskHistoryMapper(GenericEntityMapper[TaskHistory]):
    pass
