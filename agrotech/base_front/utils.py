from datetime import datetime, timedelta

visitors = {}


def track_visitor(visitor_id):
    current_time = datetime.now()

    if len(visitors) >= 50:
        visitors.clear()

    if visitor_id in visitors:
        last_visit_time = visitors[visitor_id]
        time_difference = current_time - last_visit_time
        if time_difference > timedelta(seconds=60):
            visitors[visitor_id] = current_time
            return True
        else:
            return False
    else:
        visitors[visitor_id] = current_time
        return True
