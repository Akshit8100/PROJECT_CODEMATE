"""
DateTime Operations Functions
"""

from datetime import datetime, timedelta, timezone
import calendar
from typing import Any, Dict, List, Optional
from .base import BaseFunction


class GetCurrentTimeFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_current_time"
    
    @property
    def description(self) -> str:
        return "Get current date and time"
    
    @property
    def category(self) -> str:
        return "datetime_operations"
    
    async def execute(self, timezone_name: Optional[str] = None, format_string: Optional[str] = None) -> Dict[str, Any]:
        try:
            now = datetime.now()
            
            if timezone_name:
                # This is a simplified timezone handling
                # In production, you'd use pytz or zoneinfo
                if timezone_name.upper() == "UTC":
                    now = datetime.now(timezone.utc)
            
            result = {
                "timestamp": now.timestamp(),
                "iso_format": now.isoformat(),
                "year": now.year,
                "month": now.month,
                "day": now.day,
                "hour": now.hour,
                "minute": now.minute,
                "second": now.second,
                "weekday": now.strftime("%A"),
                "month_name": now.strftime("%B")
            }
            
            if format_string:
                result["formatted"] = now.strftime(format_string)
            
            return {"success": True, "datetime": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ParseDateTimeFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "parse_datetime"
    
    @property
    def description(self) -> str:
        return "Parse datetime string into components"
    
    @property
    def category(self) -> str:
        return "datetime_operations"
    
    async def execute(self, datetime_string: str, format_string: Optional[str] = None) -> Dict[str, Any]:
        try:
            if format_string:
                dt = datetime.strptime(datetime_string, format_string)
            else:
                # Try common formats
                formats = [
                    "%Y-%m-%d %H:%M:%S",
                    "%Y-%m-%d",
                    "%m/%d/%Y",
                    "%d/%m/%Y",
                    "%Y-%m-%dT%H:%M:%S",
                    "%Y-%m-%dT%H:%M:%SZ"
                ]
                
                dt = None
                for fmt in formats:
                    try:
                        dt = datetime.strptime(datetime_string, fmt)
                        break
                    except ValueError:
                        continue
                
                if dt is None:
                    return {"success": False, "error": "Could not parse datetime string"}
            
            result = {
                "timestamp": dt.timestamp(),
                "iso_format": dt.isoformat(),
                "year": dt.year,
                "month": dt.month,
                "day": dt.day,
                "hour": dt.hour,
                "minute": dt.minute,
                "second": dt.second,
                "weekday": dt.strftime("%A"),
                "month_name": dt.strftime("%B")
            }
            
            return {"success": True, "datetime": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


class CalculateDateDifferenceFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "calculate_date_difference"
    
    @property
    def description(self) -> str:
        return "Calculate difference between two dates"
    
    @property
    def category(self) -> str:
        return "datetime_operations"
    
    async def execute(self, start_date: str, end_date: str, unit: str = "days") -> Dict[str, Any]:
        try:
            # Parse dates
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            
            diff = end_dt - start_dt
            
            if unit == "days":
                result = diff.days
            elif unit == "hours":
                result = diff.total_seconds() / 3600
            elif unit == "minutes":
                result = diff.total_seconds() / 60
            elif unit == "seconds":
                result = diff.total_seconds()
            elif unit == "weeks":
                result = diff.days / 7
            else:
                return {"success": False, "error": f"Unsupported unit: {unit}"}
            
            return {
                "success": True,
                "start_date": start_date,
                "end_date": end_date,
                "difference": result,
                "unit": unit,
                "total_seconds": diff.total_seconds()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class AddTimeFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "add_time"
    
    @property
    def description(self) -> str:
        return "Add time to a date"
    
    @property
    def category(self) -> str:
        return "datetime_operations"
    
    async def execute(self, base_date: str, amount: int, unit: str) -> Dict[str, Any]:
        try:
            dt = datetime.fromisoformat(base_date.replace('Z', '+00:00'))
            
            if unit == "days":
                new_dt = dt + timedelta(days=amount)
            elif unit == "hours":
                new_dt = dt + timedelta(hours=amount)
            elif unit == "minutes":
                new_dt = dt + timedelta(minutes=amount)
            elif unit == "seconds":
                new_dt = dt + timedelta(seconds=amount)
            elif unit == "weeks":
                new_dt = dt + timedelta(weeks=amount)
            else:
                return {"success": False, "error": f"Unsupported unit: {unit}"}
            
            return {
                "success": True,
                "original_date": base_date,
                "amount_added": amount,
                "unit": unit,
                "new_date": new_dt.isoformat(),
                "formatted": new_dt.strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class FormatDateTimeFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "format_datetime"
    
    @property
    def description(self) -> str:
        return "Format datetime in specified format"
    
    @property
    def category(self) -> str:
        return "datetime_operations"
    
    async def execute(self, datetime_string: str, format_string: str) -> Dict[str, Any]:
        try:
            dt = datetime.fromisoformat(datetime_string.replace('Z', '+00:00'))
            formatted = dt.strftime(format_string)
            
            return {
                "success": True,
                "original": datetime_string,
                "format": format_string,
                "formatted": formatted
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetCalendarFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_calendar"
    
    @property
    def description(self) -> str:
        return "Get calendar information for a month"
    
    @property
    def category(self) -> str:
        return "datetime_operations"
    
    async def execute(self, year: int, month: int) -> Dict[str, Any]:
        try:
            cal = calendar.monthcalendar(year, month)
            month_name = calendar.month_name[month]
            
            # Get additional info
            first_weekday = calendar.weekday(year, month, 1)
            days_in_month = calendar.monthrange(year, month)[1]
            
            return {
                "success": True,
                "year": year,
                "month": month,
                "month_name": month_name,
                "calendar": cal,
                "first_weekday": first_weekday,
                "days_in_month": days_in_month,
                "weekday_names": list(calendar.day_name)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class IsWeekendFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "is_weekend"
    
    @property
    def description(self) -> str:
        return "Check if a date falls on weekend"
    
    @property
    def category(self) -> str:
        return "datetime_operations"
    
    async def execute(self, date_string: str) -> Dict[str, Any]:
        try:
            dt = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            weekday = dt.weekday()  # Monday is 0, Sunday is 6
            
            is_weekend = weekday >= 5  # Saturday (5) or Sunday (6)
            
            return {
                "success": True,
                "date": date_string,
                "weekday": dt.strftime("%A"),
                "weekday_number": weekday,
                "is_weekend": is_weekend
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetTimezoneInfoFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_timezone_info"
    
    @property
    def description(self) -> str:
        return "Get timezone information"
    
    @property
    def category(self) -> str:
        return "datetime_operations"
    
    async def execute(self) -> Dict[str, Any]:
        try:
            now = datetime.now()
            utc_now = datetime.now(timezone.utc)
            
            # Calculate offset
            offset = now - utc_now.replace(tzinfo=None)
            offset_hours = offset.total_seconds() / 3600
            
            return {
                "success": True,
                "local_time": now.isoformat(),
                "utc_time": utc_now.isoformat(),
                "offset_hours": offset_hours,
                "offset_string": f"UTC{'+' if offset_hours >= 0 else ''}{offset_hours:.1f}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
