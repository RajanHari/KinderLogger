from datetime import date, timedelta

def get_school_week_bounds(input_date: date):
    weekday = input_date.weekday()
    START_OF_WEEK = input_date - timedelta(days = weekday)
    END_OF_WEEK = START_OF_WEEK + timedelta(days=4)
    return START_OF_WEEK, END_OF_WEEK