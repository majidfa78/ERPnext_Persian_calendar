import frappe
from datetime import datetime, date
from typing import Union, Tuple

def gregorian_to_jalali(g_year: int, g_month: int, g_day: int) -> Tuple[int, int, int]:
    """Convert Gregorian to Jalali (Shamsi) date"""
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    
    gy2 = g_year + 1 if g_month > 2 else g_year
    
    days = 355666 + (365 * g_year) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + \
           ((gy2 + 399) // 400) + g_day + g_d_m[g_month - 1]
    
    j_year = -159 + (33 * days // 12053)
    days -= 1461 * j_year // 4
    
    j_month = 1 + (days - 146097 * j_year // 4800) // 30
    j_day = days - 146097 * j_year // 4800 - 30 * j_month + 1
    
    return (j_year, j_month, j_day)


def get_shamsi_date(
    input_date: Union[date, datetime, str, None] = None, 
    format_str: str = "%Y/%m/%d"
) -> str:
    """
    Convert date/datetime/string to Shamsi string.
    
    Usage in Jinja: {{ get_shamsi_date(doc.posting_date) }}
    """
    if input_date is None:
        input_date = date.today()
    
    # Parse string input
    if isinstance(input_date, str):
        try:
            if ' ' in input_date:
                input_date = datetime.strptime(input_date, "%Y-%m-%d %H:%M:%S")
            else:
                input_date = datetime.strptime(input_date, "%Y-%m-%d")
        except ValueError:
            # Fallback for 'now' or other frappe formats
            input_date = frappe.utils.now_datetime() if input_date == 'now' else date.today()

    g_year, g_month, g_day = input_date.year, input_date.month, input_date.day
    
    j_year, j_month, j_day = gregorian_to_jalali(g_year, g_month, g_day)
    
    # Persian month names (optional)
    persian_months = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 
                      'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
    
    result = format_str
    result = result.replace("%Y", str(j_year))
    result = result.replace("%m", str(j_month).zfill(2))
    result = result.replace("%d", str(j_day).zfill(2))
    result = result.replace("%B", persian_months[j_month - 1])  # Month name
    
    return result
