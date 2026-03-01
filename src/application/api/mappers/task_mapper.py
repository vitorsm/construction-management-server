from typing import Optional, List

from src.application.api.mappers.generic_entity_mapper import GenericEntityMapper
from src.application.api.mappers.generic_mapper import GenericMapper
from src.entities.task import Task
from src.utils import date_utils


class TaskMapper(GenericEntityMapper[Task]):

    @staticmethod
    def to_dtos_tree(tasks: List[Task]) -> List[dict]:
        tasks_by_id = {task.id: task for task in tasks}
        root_tasks = []
        for task in tasks:
            if task.parent_task_id and task.parent_task_id in tasks_by_id:
                tasks_by_id[task.parent_task_id].add_child_task(task)
            else:
                root_tasks.append(task)

        root_tasks.sort(key=lambda task: task.name)
        return GenericMapper.to_dtos(root_tasks, TaskMapper.to_dto)

    @staticmethod
    def to_dto(task: Optional[Task]) -> Optional[dict]:
        if not task:
            return None

        children = []
        children_planned_start_date = []
        children_planned_end_date = []

        if task.children_tasks:
            for child in task.children_tasks:
                children.append(TaskMapper.to_dto(child))

                if child.planned_start_date:
                    children_planned_start_date.append(child.planned_start_date)
                if child.planned_end_date:
                    children_planned_end_date.append(child.planned_end_date)

            children.sort(key=lambda t: t["name"])

        planned_start_date = task.planned_start_date if task.planned_start_date else min(
            children_planned_start_date) if children_planned_start_date else None
        planned_end_date = task.planned_end_date if task.planned_end_date else max(
            children_planned_end_date) if children_planned_end_date else None

        task.planned_start_date = planned_start_date
        task.planned_end_date = planned_end_date

        start_date = task.actual_start_date if task.actual_start_date else planned_start_date
        end_date = task.actual_end_date if task.actual_end_date else planned_end_date

        return {
            "id": str(task.id),
            "name": task.name,
            "workspace": {"id": str(task.workspace.id)},
            "project": {"id": str(task.project.id)},
            "created_at": date_utils.datetime_to_iso(task.created_at),
            "updated_at": date_utils.datetime_to_iso(task.updated_at),
            "deleted_at": date_utils.datetime_to_iso(task.deleted_at),
            "created_by": {"id": str(task.created_by.id)},
            "updated_by": {"id": str(task.updated_by.id)},
            "start_date": date_utils.datetime_to_iso(start_date),
            "end_date": date_utils.datetime_to_iso(end_date),
            "planned_start_date": date_utils.datetime_to_iso(planned_start_date),
            "planned_end_date": date_utils.datetime_to_iso(planned_end_date),
            "actual_start_date": date_utils.datetime_to_iso(task.actual_start_date),
            "actual_end_date": date_utils.datetime_to_iso(task.actual_end_date),
            "status": task.status.name,
            "progress": task.progress,
            "files": task.files,
            "children": children,
            "parent_task_id": str(task.parent_task_id) if task.parent_task_id else None,
            "planned_expenses_values": task.get_planned_expenses_value(),
            "actual_expenses_values": task.get_actual_expenses_value()
        }
