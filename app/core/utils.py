def clean(value):
    if value is None:
        return None
    value = value.strip()
    return value if value != "" else None


def clean_int(value):
    value = clean(value)
    return int(value) if value else None


def clean_date(value):
    value = clean(value)
    if value:
        from datetime import datetime

        return datetime.strptime(value, "%Y-%m-%d")
    return None
