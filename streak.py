from datetime import timedelta

def calculate_streak(progress, start_date, today):
    streak = 0
    for i in range((today - start_date).days + 1):
        day = start_date + timedelta(days=i)
        key = day.strftime("%Y/%m/%d")

        if day == today:
            if progress.get(key):
                streak += 1
            break

        if progress.get(key):
            streak += 1
        else:
            streak = 0
    return streak

def get_streak_color(days):
    if days < 15:
        return "yellow"
    elif days < 30:
        return "orange"
    elif days < 45:
        return "red"
    elif days < 60:
        return "blue"
    else:
        return "purple"