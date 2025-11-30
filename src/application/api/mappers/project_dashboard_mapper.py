from src.entities.expense_project_details import ExpenseProjectDetails
from src.entities.task_project_details import TaskProjectDetails
from src.utils import date_utils


class ProjectDashboardMapper:

    @staticmethod
    def to_dto(task_project_details: TaskProjectDetails, expense_project_details: ExpenseProjectDetails):
        return {
            "tasks": {
                "planned_start_date": date_utils.datetime_to_iso(task_project_details.planned_start_date),
                "planned_end_date": date_utils.datetime_to_iso(task_project_details.planned_end_date),
                "actual_start_date": date_utils.datetime_to_iso(task_project_details.actual_start_date),
                "actual_end_date": date_utils.datetime_to_iso(task_project_details.actual_end_date),
                "number_tasks_planned_to_finish_now": task_project_details.number_tasks_planned_to_finish_now,
                "number_tasks_finished_now": task_project_details.number_tasks_finished_now,
                "number_not_planned_tasks": task_project_details.number_not_planned_tasks,
                "qnt_tasks_by_status": task_project_details.qnt_tasks_by_status
            },
            "expenses": {
                "planned_cost": expense_project_details.planned_cost,
                "actual_cost": expense_project_details.actual_cost,
                "expenses_value_by_type": expense_project_details.expenses_value_by_type
            }
        }