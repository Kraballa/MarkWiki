from datetime import datetime

def time_ago(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    Modified from: https://gist.github.com/rosenhouse/a0307caf0a1d2b26116b
    """
    now = datetime.utcnow()
    diff = now - datetime.fromtimestamp(time)

    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return  "a minute ago"
        if second_diff < 3600:
            return str( int(second_diff / 60) ) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str( int(second_diff / 3600) ) + " hours ago"
    if day_diff == 1:
        return "yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(int(day_diff/7)) + " weeks ago"
    if day_diff < 365:
        return str(round(int(day_diff/30)),2) + " months ago"
    return str(int(day_diff/365)) + " years ago"