"""
Text processing utilities for MisterLister.
Handles filename parsing and date conversion.
"""

import unicodedata
from datetime import datetime

def split_by_type(s, *args):
    """
    Split string into segments based on character types.
    
    Args:
        s (str): String to split
        *args: Character types to use as split points (defaults to "A" and "1")
        
    Returns:
        list: List of string segments
    """
    if not s:
        return []
    
    args = args if args else ("A", "1")
    type_filters = {unicodedata.category(char) for char in args}
    
    result = []
    current_segment = s[0]
    prev_type = unicodedata.category(s[0])
    
    for char in s[1:]:
        char_type = unicodedata.category(char)
        if not args or prev_type in type_filters:
            if char_type != prev_type:
                result.append(current_segment)
                current_segment = char
            else:
                current_segment += char
        else:
            current_segment += char
        prev_type = char_type
    
    result.append(current_segment)
    return result

def convert_short_date(date_str):
    """
    Convert 6-digit date to MM-DD-YYYY format.
    
    Args:
        date_str (str): 6-digit date string (MMDDYY)
        
    Returns:
        str: Formatted date (MM-DD-YYYY) or original string if invalid
    """
    if len(date_str.strip()) != 6:
        return date_str
        
    try:
        mm = date_str[:2]
        dd = date_str[2:4]
        yy = date_str[4:6]
        current_yy = datetime.now().year % 100
        year_prefix = "19" if int(yy) > current_yy else "20"
        full_year = f"{year_prefix}{yy}"
        datetime.strptime(f"{mm}{dd}{full_year}", "%m%d%Y")
        return f"{mm}-{dd}-{full_year}"
    except ValueError:
        return date_str 