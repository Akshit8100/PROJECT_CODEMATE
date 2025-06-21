"""
Math Operations Functions
"""

import math
import statistics
from typing import Any, Dict, List, Union
from .base import BaseFunction


class CalculateFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "calculate"
    
    @property
    def description(self) -> str:
        return "Perform basic mathematical calculations"
    
    @property
    def category(self) -> str:
        return "math_operations"
    
    async def execute(self, expression: str) -> Dict[str, Any]:
        try:
            # Safe evaluation of mathematical expressions
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            return {
                "success": True,
                "expression": expression,
                "result": result
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class StatisticsFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "calculate_statistics"
    
    @property
    def description(self) -> str:
        return "Calculate statistical measures for a list of numbers"
    
    @property
    def category(self) -> str:
        return "math_operations"
    
    async def execute(self, numbers: List[Union[int, float]]) -> Dict[str, Any]:
        try:
            if not numbers:
                return {"success": False, "error": "Empty list provided"}
            
            stats = {
                "count": len(numbers),
                "sum": sum(numbers),
                "mean": statistics.mean(numbers),
                "median": statistics.median(numbers),
                "min": min(numbers),
                "max": max(numbers),
                "range": max(numbers) - min(numbers)
            }
            
            if len(numbers) > 1:
                stats["stdev"] = statistics.stdev(numbers)
                stats["variance"] = statistics.variance(numbers)
            
            return {"success": True, "statistics": stats}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ConvertUnitsFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "convert_units"
    
    @property
    def description(self) -> str:
        return "Convert between different units of measurement"
    
    @property
    def category(self) -> str:
        return "math_operations"
    
    async def execute(self, value: float, from_unit: str, to_unit: str, unit_type: str) -> Dict[str, Any]:
        try:
            conversions = {
                "length": {
                    "mm": 0.001, "cm": 0.01, "m": 1, "km": 1000,
                    "inch": 0.0254, "ft": 0.3048, "yard": 0.9144, "mile": 1609.34
                },
                "weight": {
                    "g": 0.001, "kg": 1, "lb": 0.453592, "oz": 0.0283495
                },
                "temperature": {
                    # Special handling needed for temperature
                }
            }
            
            if unit_type == "temperature":
                # Handle temperature conversions separately
                if from_unit == "celsius" and to_unit == "fahrenheit":
                    result = (value * 9/5) + 32
                elif from_unit == "fahrenheit" and to_unit == "celsius":
                    result = (value - 32) * 5/9
                elif from_unit == "celsius" and to_unit == "kelvin":
                    result = value + 273.15
                elif from_unit == "kelvin" and to_unit == "celsius":
                    result = value - 273.15
                else:
                    return {"success": False, "error": f"Unsupported temperature conversion: {from_unit} to {to_unit}"}
            else:
                if unit_type not in conversions:
                    return {"success": False, "error": f"Unsupported unit type: {unit_type}"}
                
                unit_dict = conversions[unit_type]
                if from_unit not in unit_dict or to_unit not in unit_dict:
                    return {"success": False, "error": f"Unsupported units: {from_unit} or {to_unit}"}
                
                # Convert to base unit, then to target unit
                base_value = value * unit_dict[from_unit]
                result = base_value / unit_dict[to_unit]
            
            return {
                "success": True,
                "original_value": value,
                "original_unit": from_unit,
                "converted_value": result,
                "converted_unit": to_unit
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class GenerateSequenceFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "generate_sequence"
    
    @property
    def description(self) -> str:
        return "Generate mathematical sequences"
    
    @property
    def category(self) -> str:
        return "math_operations"
    
    async def execute(self, sequence_type: str, start: int, count: int, step: int = 1) -> Dict[str, Any]:
        try:
            if sequence_type == "arithmetic":
                sequence = [start + i * step for i in range(count)]
            elif sequence_type == "geometric":
                sequence = [start * (step ** i) for i in range(count)]
            elif sequence_type == "fibonacci":
                sequence = []
                a, b = 0, 1
                for _ in range(count):
                    sequence.append(a)
                    a, b = b, a + b
            elif sequence_type == "prime":
                sequence = []
                num = start
                while len(sequence) < count:
                    if self._is_prime(num):
                        sequence.append(num)
                    num += 1
            else:
                return {"success": False, "error": f"Unsupported sequence type: {sequence_type}"}
            
            return {
                "success": True,
                "sequence_type": sequence_type,
                "sequence": sequence,
                "count": len(sequence)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _is_prime(self, n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True


class SolveEquationFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "solve_equation"
    
    @property
    def description(self) -> str:
        return "Solve simple mathematical equations"
    
    @property
    def category(self) -> str:
        return "math_operations"
    
    async def execute(self, equation_type: str, **params) -> Dict[str, Any]:
        try:
            if equation_type == "quadratic":
                # ax^2 + bx + c = 0
                a, b, c = params.get('a', 1), params.get('b', 0), params.get('c', 0)
                discriminant = b**2 - 4*a*c
                
                if discriminant < 0:
                    return {"success": False, "error": "No real solutions"}
                elif discriminant == 0:
                    x = -b / (2*a)
                    solutions = [x]
                else:
                    x1 = (-b + math.sqrt(discriminant)) / (2*a)
                    x2 = (-b - math.sqrt(discriminant)) / (2*a)
                    solutions = [x1, x2]
                
                return {
                    "success": True,
                    "equation_type": equation_type,
                    "solutions": solutions,
                    "discriminant": discriminant
                }
            
            elif equation_type == "linear":
                # ax + b = 0
                a, b = params.get('a', 1), params.get('b', 0)
                if a == 0:
                    return {"success": False, "error": "Not a valid linear equation (a cannot be 0)"}
                
                x = -b / a
                return {
                    "success": True,
                    "equation_type": equation_type,
                    "solution": x
                }
            
            else:
                return {"success": False, "error": f"Unsupported equation type: {equation_type}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
