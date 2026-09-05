from datetime import datetime, timezone
from models import History, db

def count_transactions_this_month(employee_id):
    current_month = datetime.now().month
    current_year = datetime.now().year

    start_of_month = datetime(current_year, current_month, 1)

    if current_month == 12:
        end_of_month = datetime(current_year + 1, 1, 1)
    else:
        end_of_month = datetime(current_year, current_month + 1, 1)

    count = History.query.filter(
        History.employee_id == employee_id,
        History.date >= start_of_month,
        History.date < end_of_month
    ).count()

    return count