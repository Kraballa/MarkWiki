from datetime import datetime

def time_ago(timestamp):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    Modified from: https://gist.github.com/rosenhouse/a0307caf0a1d2b26116b
    """
    # there is no universal way to get the local timezone
    # so instead we rely on datetimes feature to infer timezone
    # then recalc current datetime with the tzinfo
    now = datetime.now()
    timezone = now.astimezone().tzinfo
    now = datetime.now(timezone)
    delta = now - datetime.fromtimestamp(timestamp, timezone)

    deltaSeconds = delta.seconds
    deltaDays = delta.days

    if deltaDays < 0:
        return ''

    if deltaDays == 0:
        if deltaSeconds < 10:
            return "just now"
        if deltaSeconds < 60:
            return str(deltaSeconds) + " seconds ago"
        if deltaSeconds < 120:
            return  "a minute ago"
        if deltaSeconds < 3600:
            return str( int(deltaSeconds / 60) ) + " minutes ago"
        if deltaSeconds < 7200:
            return "an hour ago"
        if deltaSeconds < 86400:
            return str( int(deltaSeconds / 3600) ) + " hours ago"
    if deltaDays == 1:
        return "yesterday"
    if deltaDays < 7:
        return str(deltaDays) + " days ago"
    if deltaDays < 31:
        return str(deltaDays/7) + " weeks ago"
    if deltaDays < 365:
        return str(round(deltaDays/30),2) + " months ago"
    return str(deltaDays/365) + " years ago"