from collections import defaultdict
from typing import Dict, List

from src.entities.expense import Expense, ExpenseClass


class ExpenseProjectDetails:
    planned_cost: float
    actual_cost: float
    expenses_value_by_type: Dict[str, float]

    def __init__(self, expenses: List[Expense]):
        self.expenses = expenses
        self.__init_expenses_values()

    def __init_expenses_values(self):
        self.planned_cost = 0
        self.actual_cost = 0
        self.expenses_value_by_type = defaultdict(int)

        for expense in self.expenses:
            if expense.expense_class == ExpenseClass.PLANNING:
                self.planned_cost += expense.value
            if expense.expense_class == ExpenseClass.EXECUTION:
                self.actual_cost += expense.value

            self.expenses_value_by_type[expense.expense_type.name] += expense.value
