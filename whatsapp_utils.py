from datetime import datetime

def extract_datetime_from_filename(filename):
    parts = filename.split(" at ")
    date_part = parts[0].split(" ")[-1]
    time_part = parts[1].split(".ogg")[0]
    time_part = time_part.replace('.', ':')
    datetime_str = f"{date_part} {time_part}"
    return datetime.strptime(datetime_str, '%Y-%m-%d %I:%M:%S %p')

