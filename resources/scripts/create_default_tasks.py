import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import uuid4

import psycopg

from src.entities.expense import ExpenseType, ExpenseClass
from src.entities.task import TaskStatus

INSERT_TASK= "INSERT INTO task (id, name, created_at, updated_at, deleted_at, created_by, updated_by, workspace_id, project_id, planned_start_date, planned_end_date, actual_start_date, actual_end_date, status, progress, parent_task_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
INSERT_EXPENSE = "INSERT INTO expense (id, name, created_at, updated_at, deleted_at, created_by, updated_by, workspace_id, project_id, expense_type, expense_class, value, notes, task_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


DB_NAME = os.environ.get("DB_NAME", "construction_management")
DB_USER = os.environ.get("DB_USER", "admin")
DB_PASS = os.environ.get("DB_PASS", "password")
DB_HOST = os.environ.get("DB_HOST", "127.0.0.1")

INPUT_FILE_PATH = "default_tasks.json"
PROJECT_ID = "d668aa6e-5775-4d8f-94d2-8d9df2c845a1"
USER_ID = "10000000-0000-0000-0000-000000000001"
WORKSPACE_ID = "f0ae47da-7352-455c-a3ad-02e7fb8d29c9"
PROJECT_START_DATE = datetime(year=2025, month=4, day=1)
DAY_TO_COMPLETE_TASK = datetime(year=2025, month=10, day=30)
# DAY_TO_COMPLETE_TASK = None
ONE_TO_N_EXPENSE_DONE = 2
MARGIN_PRICE_EXPENSE = 0.5
NOW = datetime.now()

conn = psycopg.connect(f"dbname={DB_NAME} user={DB_USER} password={DB_PASS} host={DB_HOST}")
cursor = conn.cursor()


def load_tasks_file() -> List[dict]:
    with open(INPUT_FILE_PATH, "r") as file:
        return json.load(file)


def insert_task(task_name: str, start_at: int, end_at: int, parent_task_id: Optional[str]) -> str:
    task_id = str(uuid4())

    planned_start_date = PROJECT_START_DATE + timedelta(days=start_at) if start_at is not None else None
    planned_end_date = PROJECT_START_DATE + timedelta(days=end_at) if end_at is not None else None
    actual_start_date = None
    actual_end_date = None

    status = TaskStatus.TODO.name
    progress = 0
    if DAY_TO_COMPLETE_TASK and planned_start_date and planned_end_date:
        if planned_start_date <= DAY_TO_COMPLETE_TASK:
            status = TaskStatus.IN_PROGRESS.name
            progress = int(random.random() * 100)
            actual_start_date = planned_start_date

        if planned_end_date <= DAY_TO_COMPLETE_TASK:
            status = TaskStatus.DONE.name
            progress = 100
            actual_end_date = planned_end_date

    task_tuple = (task_id, task_name, NOW, NOW, None, USER_ID, USER_ID, WORKSPACE_ID, PROJECT_ID, planned_start_date, planned_end_date, actual_start_date, actual_end_date, status, progress, parent_task_id)
    cursor.execute(INSERT_TASK, task_tuple)

    return task_id


def insert_expense(name: str, task_id: str, value: float, actual: bool = False):
    expense_id = str(uuid4())
    expense_type = get_expense_type(name)
    expanse_class = ExpenseClass.EXECUTION if actual else ExpenseClass.PLANNING
    expense_tuple = (expense_id, name, NOW, NOW, None, USER_ID, USER_ID, WORKSPACE_ID, PROJECT_ID, expense_type, expanse_class.name, value, None, task_id)

    cursor.execute(INSERT_EXPENSE, expense_tuple)

    return expense_id


def get_expense_type(expense_name: str) -> str:
    if "ão de obra" in expense_name or "onorários" in expense_name:
        return ExpenseType.LABOR.name
    if "Material" in expense_name or "material" in expense_name:
        return ExpenseType.MATERIAL.name
    if "matrícula" in expense_name or "Taxas" in expense_name or "icença" in expense_name:
        return ExpenseType.DOCUMENT.name
    if "ngenheiro" in expense_name or "rquitet" in expense_name or "ocument" in expense_name or "rojeto" in expense_name or "Laudo" in expense_name:
        return ExpenseType.PROJECT.name
    if "jurídico" in expense_name or "Serviço" in expense_name:
        return ExpenseType.SERVICE.name

    return ExpenseType.MATERIAL.name


def get_tasks_start_end_at(tasks: List[dict]):
    result = {}
    for step in tasks:
        starts = []
        ends = []
        for substep in step["subetapas"]:
            start = min([task["start_at"] for task in substep["tarefas"]])
            end = max([task["end_at"] for task in substep["tarefas"]])
            starts.append(start)
            ends.append(end)
            result[substep["subetapa"]] = start, end

        result[step["etapa"]] = min(starts), max(ends)
    return result


def create_items():
    tasks = load_tasks_file()
    dates_by_tasks = get_tasks_start_end_at(tasks)

    for step in tasks:
        print(step["etapa"])
        start, end = dates_by_tasks[step["etapa"]]
        step_id = insert_task(step["etapa"], start, end, None)
        for substep in step["subetapas"]:
            print(substep["subetapa"])
            start, end = dates_by_tasks[substep["subetapa"]]
            substep_id = insert_task(substep["subetapa"], start, end, step_id)
            for task in substep["tarefas"]:
                print(task["tarefa"])
                task_id = insert_task(task["tarefa"], task["start_at"], task["end_at"], substep_id)
                for cost in task["custos_detalhados"]:
                    print(cost["descricao"])
                    if cost["valor_R$"]:
                        insert_expense(cost["descricao"], task_id, cost["valor_R$"])
                        if DAY_TO_COMPLETE_TASK and not random.randint(0, ONE_TO_N_EXPENSE_DONE):
                            perc_cost = random.random() + MARGIN_PRICE_EXPENSE
                            insert_expense(cost["descricao"], task_id, perc_cost * cost["valor_R$"], True)


    conn.commit()


if __name__ == '__main__':
    create_items()
