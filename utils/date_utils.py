import re
from dateutil import parser
from datetime import datetime, timedelta
import pytz

def parse_relative_dates(date_str):
    now = datetime.now(pytz.UTC)
    date_str = re.sub(r'\babout\b|\balmost\b|\bnearly\b', '', date_str).strip()

    hours_match = re.search(r'(\d+)\s*hours?\s*ago', date_str)
    if hours_match:
        hours = int(hours_match.group(1))
        return now - timedelta(hours=hours)

    minutes_match = re.search(r'(\d+)\s*minutes?\s*ago', date_str)
    if minutes_match:
        minutes = int(minutes_match.group(1))
        return now - timedelta(minutes=minutes)

    days_match = re.search(r'(\d+)\s*days?\s*ago', date_str)
    if days_match:
        days = int(days_match.group(1))
        return now - timedelta(days=days)

    weeks_match = re.search(r'(\d+)\s*weeks?\s*ago', date_str)
    if weeks_match:
        weeks = int(weeks_match.group(1))
        return now - timedelta(weeks=weeks)

    if "yesterday" in date_str.lower():
        return now - timedelta(days=1)
    if "last week" in date_str.lower():
        return now - timedelta(weeks=1)
    if "a day ago" in date_str.lower():
        return now - timedelta(days=1)
    if "a week ago" in date_str.lower():
        return now - timedelta(weeks=1)

    return None

def get_timezone(timezone_str):
    timezone_map = {
        'IST': 'Asia/Kolkata',
        'ET': 'America/New_York',
        'GMT': 'Etc/GMT',
        'UTC': 'UTC'
    }
    return pytz.timezone(timezone_map.get(timezone_str, 'UTC'))

def parse_date(date_str):
    date_str = date_str.strip()
    relative_date = parse_relative_dates(date_str)
    if relative_date:
        return relative_date.strftime('%d/%m/%Y %H:%M')

    date_str = re.sub(r"\bat\b|\bUpdated On\b|\bPublished\b|\bon\b", '', date_str, flags=re.IGNORECASE).strip()
    timezone_match = re.search(r'\b(IST|ET|GMT|UTC)\b', date_str)
    timezone = timezone_match.group(1) if timezone_match else None
    date_str = re.sub(r"\b(IST|ET|GMT|UTC)\b", '', date_str).strip()

    try:
        parsed_date = parser.parse(date_str, fuzzy=True)

        if timezone:
            tz = get_timezone(timezone)
            parsed_date = tz.localize(parsed_date)
            parsed_date = parsed_date.astimezone(pytz.UTC)

        return parsed_date.strftime('%d/%m/%Y %H:%M')
    except (parser.ParserError, ValueError):
        return f"Unrecognized format: {date_str}"
