from datetime import date, timedelta
from calendar import monthrange

def add_months(source_date: date, months: int) -> date:
    """Add a specified number of months to a date, handling month boundaries correctly"""
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1

    # Handle the case where the day might not exist in the target month
    # For example, adding 1 month to Jan 31 should result in Feb 28/29
    day = min(source_date.day, monthrange(year, month)[1])

    return date(year, month, day)

def get_month_range(year: int, month: int) -> tuple[date, date]:
    """Return the start and end dates for a specific month"""
    start_date = date(year, month, 1)
    _, last_day = monthrange(year, month)
    end_date = date(year, month, last_day)
    return start_date, end_date

def calculate_next_occurrence(current_date: date, interval: str) -> date:
    """Calculate the next occurrence date based on the interval"""
    interval = interval.lower()

    if interval == "daily":
        return current_date + timedelta(days=1)
    elif interval == "weekly":
        return current_date + timedelta(days=7)
    elif interval == "biweekly":
        return current_date + timedelta(days=14)
    elif interval == "monthly":
        return add_months(current_date, 1)
    elif interval == "quarterly":
        return add_months(current_date, 3)
    elif interval in ["yearly", "annually"]:
        return add_months(current_date, 12)
    else:
        # Default to monthly if interval is not recognized
        return add_months(current_date, 1)