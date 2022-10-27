from datetime import datetime

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_day_number(timestamp):
    ts = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    return float(ts.timetuple().tm_yday)


def get_bin_number(timestamp):
    ts = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    return float(ts.hour * 12 + ts.minute // 5)


def get_week_day(timestamp):
    ts = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    return ts.weekday()


def get_month(timestamp):
    ts = datetime.strptime(timestamp, TIMESTAMP_FORMAT)
    return ts.month
