from datetime import datetime, timedelta
import jdatetime

def after(start_date, days_count):
    if days_count == 0:
        return start_date
    date_list = after_list(start_date, days_count)
    
    return date_list[days_count]

def before(start_date, days_count):
    date_list = before_list(start_date, days_count)
    
    return date_list[days_count]
    
def before_list(start_date, days_count):
    start_date = datetime.strptime(start_date, '%Y%m%d')    
    date_list = [(start_date - timedelta(days=i)).strftime('%Y%m%d') for i in range(days_count+1)]
    
    return date_list
    
def after_list(start_date, days_count):
    start_date = datetime.strptime(start_date, '%Y%m%d')    
    date_list = [(start_date + timedelta(days=i)).strftime('%Y%m%d') for i in range(days_count+1)]
    
    return date_list

def convert_to_shamsi(date_int):
    date_miladi = datetime.strptime(date_int, '%Y%m%d')    
    date_shamsi = jdatetime.date.fromgregorian(day=date_miladi.day, month=date_miladi.month, year=date_miladi.year)
    
    return date_shamsi.strftime('%Y%m%d')

def convert_to_miladi(shamsi_date_int):
    shamsi_date_str = f"{shamsi_date_int:08}"
    year = int(shamsi_date_str[:4])
    month = int(shamsi_date_str[4:6])
    day = int(shamsi_date_str[6:])
    date_shamsi = jdatetime.date(year, month, day)
    date_miladi = date_shamsi.togregorian()
    miladi_date_int = int(date_miladi.strftime('%Y%m%d'))
    
    return miladi_date_int

def format_date(date_int):
    date_miladi = datetime.strptime(date_int, '%Y%m%d')
    formatted_miladi = date_miladi.strftime('%a %d %B')
    date_shamsi = jdatetime.date.fromgregorian(day=date_miladi.day, month=date_miladi.month, year=date_miladi.year)
    formatted_shamsi = date_shamsi.strftime('%a %d %B')
    
    return {"miladi":formatted_miladi, "shamsi":formatted_shamsi}
