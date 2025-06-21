"""
Data Processing Functions
"""

import pandas as pd
import json
import sqlite3
from typing import Any, Dict, List, Optional
from .base import BaseFunction


class ReadCSVFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "read_csv"
    
    @property
    def description(self) -> str:
        return "Read data from a CSV file and return as structured data"
    
    @property
    def category(self) -> str:
        return "data_processing"
    
    @property
    def examples(self) -> List[str]:
        return ["read_csv('data/sales.csv')", "read_csv('invoices.csv')"]
    
    async def execute(self, file_path: str, delimiter: str = ",") -> Dict[str, Any]:
        try:
            df = pd.read_csv(file_path, delimiter=delimiter)
            return {
                "success": True,
                "data": df.to_dict('records'),
                "shape": df.shape,
                "columns": df.columns.tolist()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class FilterDataFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "filter_data"
    
    @property
    def description(self) -> str:
        return "Filter data based on specified conditions"
    
    @property
    def category(self) -> str:
        return "data_processing"
    
    async def execute(self, data: List[Dict], column: str, operator: str, value: Any) -> Dict[str, Any]:
        try:
            filtered_data = []
            for row in data:
                if column not in row:
                    continue
                    
                row_value = row[column]
                if operator == "equals":
                    if row_value == value:
                        filtered_data.append(row)
                elif operator == "greater_than":
                    if float(row_value) > float(value):
                        filtered_data.append(row)
                elif operator == "less_than":
                    if float(row_value) < float(value):
                        filtered_data.append(row)
                elif operator == "contains":
                    if str(value).lower() in str(row_value).lower():
                        filtered_data.append(row)
            
            return {"success": True, "data": filtered_data, "count": len(filtered_data)}
        except Exception as e:
            return {"success": False, "error": str(e)}


class SummarizeDataFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "summarize_data"
    
    @property
    def description(self) -> str:
        return "Generate summary statistics for numerical data"
    
    @property
    def category(self) -> str:
        return "data_processing"
    
    async def execute(self, data: List[Dict], column: str) -> Dict[str, Any]:
        try:
            values = [float(row[column]) for row in data if column in row and row[column] is not None]
            
            if not values:
                return {"success": False, "error": "No valid numerical data found"}
            
            summary = {
                "count": len(values),
                "sum": sum(values),
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values)
            }
            
            return {"success": True, "summary": summary}
        except Exception as e:
            return {"success": False, "error": str(e)}


class GroupByFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "group_by"
    
    @property
    def description(self) -> str:
        return "Group data by a column and perform aggregation"
    
    @property
    def category(self) -> str:
        return "data_processing"
    
    async def execute(self, data: List[Dict], group_column: str, agg_column: str, operation: str = "sum") -> Dict[str, Any]:
        try:
            groups = {}
            for row in data:
                if group_column not in row or agg_column not in row:
                    continue
                
                group_key = row[group_column]
                agg_value = float(row[agg_column])
                
                if group_key not in groups:
                    groups[group_key] = []
                groups[group_key].append(agg_value)
            
            result = {}
            for group_key, values in groups.items():
                if operation == "sum":
                    result[group_key] = sum(values)
                elif operation == "mean":
                    result[group_key] = sum(values) / len(values)
                elif operation == "count":
                    result[group_key] = len(values)
                elif operation == "max":
                    result[group_key] = max(values)
                elif operation == "min":
                    result[group_key] = min(values)
            
            return {"success": True, "groups": result}
        except Exception as e:
            return {"success": False, "error": str(e)}


class QueryDatabaseFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "query_database"
    
    @property
    def description(self) -> str:
        return "Execute SQL query on SQLite database"
    
    @property
    def category(self) -> str:
        return "data_processing"
    
    async def execute(self, db_path: str, query: str) -> Dict[str, Any]:
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                columns = [description[0] for description in cursor.description]
                rows = cursor.fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                result = {"success": True, "data": data, "count": len(data)}
            else:
                conn.commit()
                result = {"success": True, "rows_affected": cursor.rowcount}
            
            conn.close()
            return result
        except Exception as e:
            return {"success": False, "error": str(e)}


class SortDataFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "sort_data"
    
    @property
    def description(self) -> str:
        return "Sort data by specified column"
    
    @property
    def category(self) -> str:
        return "data_processing"
    
    async def execute(self, data: List[Dict], column: str, ascending: bool = True) -> Dict[str, Any]:
        try:
            sorted_data = sorted(data, key=lambda x: x.get(column, 0), reverse=not ascending)
            return {"success": True, "data": sorted_data}
        except Exception as e:
            return {"success": False, "error": str(e)}


class JoinDataFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "join_data"
    
    @property
    def description(self) -> str:
        return "Join two datasets on a common column"
    
    @property
    def category(self) -> str:
        return "data_processing"
    
    async def execute(self, left_data: List[Dict], right_data: List[Dict], left_key: str, right_key: str) -> Dict[str, Any]:
        try:
            # Create lookup dictionary for right data
            right_lookup = {row[right_key]: row for row in right_data if right_key in row}
            
            joined_data = []
            for left_row in left_data:
                if left_key in left_row and left_row[left_key] in right_lookup:
                    merged_row = {**left_row, **right_lookup[left_row[left_key]]}
                    joined_data.append(merged_row)
            
            return {"success": True, "data": joined_data, "count": len(joined_data)}
        except Exception as e:
            return {"success": False, "error": str(e)}


class ValidateDataFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "validate_data"

    @property
    def description(self) -> str:
        return "Validate data against specified rules"

    @property
    def category(self) -> str:
        return "data_processing"

    async def execute(self, data: List[Dict[str, Any]], rules: Dict[str, Any]) -> Dict[str, Any]:
        try:
            validation_results = []
            errors = []

            for i, row in enumerate(data):
                row_errors = []

                for field, rule in rules.items():
                    if field not in row:
                        if rule.get('required', False):
                            row_errors.append(f"Missing required field: {field}")
                        continue

                    value = row[field]

                    # Type validation
                    if 'type' in rule:
                        expected_type = rule['type']
                        if expected_type == 'number' and not isinstance(value, (int, float)):
                            row_errors.append(f"{field}: Expected number, got {type(value).__name__}")
                        elif expected_type == 'string' and not isinstance(value, str):
                            row_errors.append(f"{field}: Expected string, got {type(value).__name__}")

                    # Range validation
                    if 'min' in rule and isinstance(value, (int, float)) and value < rule['min']:
                        row_errors.append(f"{field}: Value {value} below minimum {rule['min']}")
                    if 'max' in rule and isinstance(value, (int, float)) and value > rule['max']:
                        row_errors.append(f"{field}: Value {value} above maximum {rule['max']}")

                validation_results.append({
                    "row_index": i,
                    "valid": len(row_errors) == 0,
                    "errors": row_errors
                })

                if row_errors:
                    errors.extend(row_errors)

            return {
                "success": True,
                "validation_results": validation_results,
                "total_rows": len(data),
                "valid_rows": sum(1 for r in validation_results if r['valid']),
                "invalid_rows": sum(1 for r in validation_results if not r['valid']),
                "errors": errors
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class TransformDataFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "transform_data"

    @property
    def description(self) -> str:
        return "Transform data by applying functions to columns"

    @property
    def category(self) -> str:
        return "data_processing"

    async def execute(self, data: List[Dict[str, Any]], transformations: Dict[str, str]) -> Dict[str, Any]:
        try:
            transformed_data = []

            for row in data:
                new_row = row.copy()

                for column, transformation in transformations.items():
                    if column in new_row:
                        value = new_row[column]

                        if transformation == "uppercase" and isinstance(value, str):
                            new_row[column] = value.upper()
                        elif transformation == "lowercase" and isinstance(value, str):
                            new_row[column] = value.lower()
                        elif transformation == "abs" and isinstance(value, (int, float)):
                            new_row[column] = abs(value)
                        elif transformation == "round" and isinstance(value, float):
                            new_row[column] = round(value, 2)
                        elif transformation == "strip" and isinstance(value, str):
                            new_row[column] = value.strip()

                transformed_data.append(new_row)

            return {
                "success": True,
                "data": transformed_data,
                "transformations_applied": transformations,
                "rows_processed": len(transformed_data)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
