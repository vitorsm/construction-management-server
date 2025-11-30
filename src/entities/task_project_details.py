from collections import defaultdict
from datetime import datetime
from typing import List, Optional, Dict

from src.entities.task import Task, TaskStatus


class TaskProjectDetails:
    planned_start_date: Optional[datetime]
    planned_end_date: Optional[datetime]
    actual_start_date: Optional[datetime]
    actual_end_date: Optional[datetime]
    number_tasks_planned_to_finish_now: int
    number_tasks_finished_now: int
    number_not_planned_tasks: int
    qnt_tasks_by_status: Dict[str, int]

    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

        self.__fill_dates()

    def __fill_dates(self):
        planned_start_dates = []
        planned_end_dates = []
        actual_start_dates = []
        actual_end_dates = []

        current_date = datetime.now()
        self.qnt_tasks_by_status = defaultdict(int)
        self.number_tasks_planned_to_finish_now = 0
        self.number_tasks_finished_now = 0
        self.number_not_planned_tasks = 0

        for task in self.tasks:
            if task.planned_start_date:
                planned_start_dates.append(task.planned_start_date)

            if task.planned_end_date:
                planned_end_dates.append(task.planned_end_date)
                if task.planned_end_date <= current_date:
                    self.number_tasks_planned_to_finish_now += 1
            else:
                self.number_not_planned_tasks += 1

            if task.actual_start_date:
                actual_start_dates.append(task.actual_start_date)
            if task.actual_end_date:
                actual_end_dates.append(task.actual_end_date)
            if task.status == TaskStatus.DONE:
                self.number_tasks_finished_now += 1

            self.qnt_tasks_by_status[task.status.name] += 1

        self.planned_start_date = min(planned_start_dates) if planned_start_dates else None
        self.planned_end_date = min(planned_end_dates) if planned_end_dates else None
        self.actual_start_date = min(actual_start_dates) if actual_start_dates else None
        self.actual_end_date = min(actual_end_dates) if actual_end_dates else None
