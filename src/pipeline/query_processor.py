"""
Query Processor

Processes natural language queries and converts them to function call plans.
"""

import re
from typing import Dict, Any, List, Optional
from loguru import logger
from ..models.function_calling import FunctionCallingModel
from ..functions import registry


class QueryProcessor:
    """Processes user queries and generates function call plans"""
    
    def __init__(self, function_calling_model: FunctionCallingModel):
        self.function_calling_model = function_calling_model
        self.function_registry = registry
    
    def process_query(self, query: str) -> Dict[str, Any]:
        """Process a user query and return a function call plan"""
        try:
            logger.info(f"Processing query: {query}")
            
            # Preprocess the query
            processed_query = self._preprocess_query(query)
            
            # Get available functions
            available_functions = self.function_registry.get_function_schemas()
            
            # Generate function call plan
            plan = self.function_calling_model.plan_function_calls(
                processed_query, 
                available_functions
            )
            
            # Validate the plan
            is_valid, errors = self.function_calling_model.validate_function_calls(
                plan.get('function_calls', []), 
                available_functions
            )
            
            if not is_valid:
                logger.warning(f"Invalid function calls: {errors}")
                # Try to fix common issues
                plan = self._fix_common_issues(plan, errors)
            
            # Optimize the function sequence
            if 'function_calls' in plan:
                plan['function_calls'] = self.function_calling_model.optimize_function_sequence(
                    plan['function_calls']
                )
            
            # Add metadata
            plan['query'] = query
            plan['processed_query'] = processed_query
            plan['timestamp'] = self._get_timestamp()
            plan['valid'] = is_valid
            plan['errors'] = errors if not is_valid else []
            
            logger.info(f"Generated plan with {len(plan.get('function_calls', []))} function calls")
            return plan
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return self._create_error_response(query, str(e))
    
    def _preprocess_query(self, query: str) -> str:
        """Preprocess the query to improve AI understanding"""
        # Remove extra whitespace
        query = re.sub(r'\s+', ' ', query.strip())
        
        # Expand common abbreviations
        abbreviations = {
            "w/": "with",
            "w/o": "without",
            "etc.": "and so on",
            "e.g.": "for example",
            "i.e.": "that is",
        }
        
        for abbrev, expansion in abbreviations.items():
            query = query.replace(abbrev, expansion)
        
        # Add context clues for better understanding
        if "invoice" in query.lower() and "march" in query.lower():
            query += " (Note: Look for invoice data in CSV or database format)"
        
        if "email" in query.lower() and "send" in query.lower():
            query += " (Note: Use email function to send messages)"
        
        return query
    
    def _fix_common_issues(self, plan: Dict[str, Any], errors: List[str]) -> Dict[str, Any]:
        """Try to fix common issues in function call plans"""
        if 'function_calls' not in plan:
            return plan
        
        fixed_calls = []
        
        for call in plan['function_calls']:
            # Fix missing parameters
            if 'parameters' not in call:
                call['parameters'] = {}
            
            # Add default values for common missing parameters
            function_name = call.get('function_name', '')
            
            if function_name == 'send_email':
                if 'to_email' not in call['parameters']:
                    call['parameters']['to_email'] = 'abhayrajputcse@gmail.com'
                if 'subject' not in call['parameters']:
                    call['parameters']['subject'] = 'Automated Email'
                if 'body' not in call['parameters']:
                    call['parameters']['body'] = 'This is an automated email.'
            
            elif function_name == 'read_csv':
                if 'file_path' not in call['parameters']:
                    call['parameters']['file_path'] = 'data/sample.csv'
            
            elif function_name == 'read_file':
                if 'file_path' not in call['parameters']:
                    call['parameters']['file_path'] = 'data/sample.txt'
            
            fixed_calls.append(call)
        
        plan['function_calls'] = fixed_calls
        return plan
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def _create_error_response(self, query: str, error: str) -> Dict[str, Any]:
        """Create an error response"""
        return {
            "query": query,
            "plan": "Error occurred while processing query",
            "function_calls": [],
            "error": error,
            "timestamp": self._get_timestamp(),
            "valid": False
        }
    
    def get_function_info(self, function_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific function"""
        function = self.function_registry.get_function(function_name)
        if function:
            return function.to_dict()
        return None
    
    def list_functions_by_category(self, category: str) -> List[Dict[str, Any]]:
        """List all functions in a specific category"""
        functions = self.function_registry.get_functions_by_category(category)
        return [func.to_dict() for func in functions]
    
    def search_functions(self, keyword: str) -> List[Dict[str, Any]]:
        """Search for functions by keyword"""
        all_functions = self.function_registry.get_all_functions()
        matching_functions = []
        
        keyword_lower = keyword.lower()
        
        for func in all_functions:
            func_dict = func.to_dict()
            if (keyword_lower in func_dict['name'].lower() or 
                keyword_lower in func_dict['description'].lower() or
                keyword_lower in func_dict['category'].lower()):
                matching_functions.append(func_dict)
        
        return matching_functions
    
    def analyze_query_complexity(self, query: str) -> Dict[str, Any]:
        """Analyze the complexity of a query"""
        words = query.split()
        
        # Count different types of operations
        data_keywords = ['read', 'load', 'import', 'data', 'csv', 'excel', 'database']
        process_keywords = ['filter', 'sort', 'group', 'summarize', 'calculate', 'analyze']
        output_keywords = ['send', 'email', 'save', 'write', 'export', 'notify']
        
        data_ops = sum(1 for word in words if word.lower() in data_keywords)
        process_ops = sum(1 for word in words if word.lower() in process_keywords)
        output_ops = sum(1 for word in words if word.lower() in output_keywords)
        
        complexity_score = data_ops + process_ops + output_ops
        
        if complexity_score <= 2:
            complexity = "simple"
        elif complexity_score <= 4:
            complexity = "moderate"
        else:
            complexity = "complex"
        
        return {
            "complexity": complexity,
            "complexity_score": complexity_score,
            "data_operations": data_ops,
            "processing_operations": process_ops,
            "output_operations": output_ops,
            "estimated_functions": max(1, complexity_score)
        }
