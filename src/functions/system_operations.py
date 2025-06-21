"""
System Operations Functions
"""

import os
import subprocess
import psutil
import platform
from typing import Any, Dict, List, Optional
from .base import BaseFunction


class ExecuteCommandFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "execute_command"
    
    @property
    def description(self) -> str:
        return "Execute a system command"
    
    @property
    def category(self) -> str:
        return "system_operations"
    
    async def execute(self, command: str, timeout: int = 30, shell: bool = True) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            return {
                "success": True,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {timeout} seconds"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetSystemInfoFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_system_info"
    
    @property
    def description(self) -> str:
        return "Get system information"
    
    @property
    def category(self) -> str:
        return "system_operations"
    
    async def execute(self) -> Dict[str, Any]:
        try:
            info = {
                "platform": platform.platform(),
                "system": platform.system(),
                "processor": platform.processor(),
                "architecture": platform.architecture(),
                "python_version": platform.python_version(),
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total,
                "memory_available": psutil.virtual_memory().available,
                "disk_usage": {
                    "total": psutil.disk_usage('/').total if platform.system() != 'Windows' else psutil.disk_usage('C:').total,
                    "free": psutil.disk_usage('/').free if platform.system() != 'Windows' else psutil.disk_usage('C:').free
                }
            }
            
            return {"success": True, "system_info": info}
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetProcessListFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_process_list"
    
    @property
    def description(self) -> str:
        return "Get list of running processes"
    
    @property
    def category(self) -> str:
        return "system_operations"
    
    async def execute(self, limit: int = 10) -> Dict[str, Any]:
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage and limit results
            processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
            processes = processes[:limit]
            
            return {"success": True, "processes": processes, "count": len(processes)}
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetEnvironmentVariableFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_environment_variable"
    
    @property
    def description(self) -> str:
        return "Get environment variable value"
    
    @property
    def category(self) -> str:
        return "system_operations"
    
    async def execute(self, variable_name: str, default_value: Optional[str] = None) -> Dict[str, Any]:
        try:
            value = os.getenv(variable_name, default_value)
            
            return {
                "success": True,
                "variable_name": variable_name,
                "value": value,
                "exists": variable_name in os.environ
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class SetEnvironmentVariableFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "set_environment_variable"
    
    @property
    def description(self) -> str:
        return "Set environment variable (for current session)"
    
    @property
    def category(self) -> str:
        return "system_operations"
    
    async def execute(self, variable_name: str, value: str) -> Dict[str, Any]:
        try:
            os.environ[variable_name] = value
            
            return {
                "success": True,
                "message": f"Environment variable {variable_name} set to {value}"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetCurrentDirectoryFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_current_directory"
    
    @property
    def description(self) -> str:
        return "Get current working directory"
    
    @property
    def category(self) -> str:
        return "system_operations"
    
    async def execute(self) -> Dict[str, Any]:
        try:
            cwd = os.getcwd()
            
            return {
                "success": True,
                "current_directory": cwd,
                "absolute_path": os.path.abspath(cwd)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class ChangeDirectoryFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "change_directory"
    
    @property
    def description(self) -> str:
        return "Change current working directory"
    
    @property
    def category(self) -> str:
        return "system_operations"
    
    async def execute(self, directory_path: str) -> Dict[str, Any]:
        try:
            if not os.path.exists(directory_path):
                return {"success": False, "error": f"Directory {directory_path} does not exist"}
            
            if not os.path.isdir(directory_path):
                return {"success": False, "error": f"{directory_path} is not a directory"}
            
            old_cwd = os.getcwd()
            os.chdir(directory_path)
            new_cwd = os.getcwd()
            
            return {
                "success": True,
                "old_directory": old_cwd,
                "new_directory": new_cwd
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class MonitorSystemResourcesFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "monitor_system_resources"
    
    @property
    def description(self) -> str:
        return "Monitor current system resource usage"
    
    @property
    def category(self) -> str:
        return "system_operations"
    
    async def execute(self) -> Dict[str, Any]:
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/' if platform.system() != 'Windows' else 'C:')
            
            resources = {
                "cpu_percent": cpu_percent,
                "memory": {
                    "total": memory.total,
                    "available": memory.available,
                    "percent": memory.percent,
                    "used": memory.used
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "percent": (disk.used / disk.total) * 100
                }
            }
            
            return {"success": True, "resources": resources}
        except Exception as e:
            return {"success": False, "error": str(e)}
