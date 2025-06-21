"""
Function Library for AI Function Calling Pipeline

This module contains a comprehensive library of functions that can be called
by the AI model to fulfill user requests.
"""

from .base import BaseFunction, FunctionRegistry
from .data_processing import *
from .communication import *
from .file_operations import *
from .web_operations import *
from .system_operations import *
from .math_operations import *
from .text_operations import *
from .datetime_operations import *

# Initialize the global function registry
registry = FunctionRegistry()

# Auto-register all functions
registry.auto_register_functions()

__all__ = [
    'BaseFunction',
    'FunctionRegistry', 
    'registry'
]
