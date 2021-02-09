from datetime import datetime
from flask import current_app


def calculate_timeline () -> int:
    begin_str = current_app.config['BEGINNING']
    begin_time = datetime.strptime(begin_str, '%b %d %Y %I:%M%p')
    now = datetime.now()

    time_diff = now - begin_time

    return time_diff.days + 1

    