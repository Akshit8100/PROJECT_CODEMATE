"""
Function Calling Model

This module implements function calling capabilities using the AI model.
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple
from loguru import logger
from .model_manager import ModelManager


class FunctionCallingModel:
    """AI model with function calling capabilities"""
    
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.system_prompt = self._create_system_prompt()
    
    def _create_system_prompt(self) -> str:
        """Create the system prompt for function calling"""
        return """You are an AI assistant specialized in function calling and task automation. Your role is to analyze user requests and generate structured function call sequences.

TASK: Convert natural language requests into executable function call sequences.

RESPONSE FORMAT: Always respond with valid JSON in this exact format:
{
  "plan": "Brief description of your execution plan",
  "function_calls": [
    {
      "function_name": "exact_function_name",
      "parameters": {"param1": "value1", "param2": "value2"},
      "description": "What this function accomplishes"
    }
  ]
}

AVAILABLE FUNCTIONS (55+ total):

DATA PROCESSING (9 functions):
- read_csv(file_path): Read CSV data
- filter_data(data, column, operator, value): Filter data rows
- summarize_data(data, column): Calculate statistics
- group_by(data, column): Group data by column
- query_database(query, database_path): Execute SQL query
- sort_data(data, column, ascending): Sort data
- join_data(data1, data2, key): Join two datasets
- validate_data(data, rules): Validate data against rules
- transform_data(data, transformations): Transform data columns

COMMUNICATION (7 functions):
- send_email(to_email, subject, body): Send email
- send_sms(phone_number, message): Send SMS
- make_http_request(url, method, data): Make HTTP request
- post_to_slack(channel, message): Post to Slack
- send_notification(title, message): Send notification
- get_weather(location): Get weather information
- get_news(category, count): Get news articles

FILE OPERATIONS (10 functions):
- read_file(file_path): Read text file
- write_file(file_path, content): Write text file
- copy_file(source_path, destination_path): Copy file
- delete_file(file_path): Delete file
- list_directory(directory_path): List directory contents
- create_directory(directory_path): Create directory
- read_json(file_path): Read JSON file
- write_json(file_path, data): Write JSON file
- read_excel(file_path, sheet_name): Read Excel file
- get_file_info(file_path): Get file information

WEB OPERATIONS (8 functions):
- fetch_web_page(url): Fetch web page content
- extract_links(url): Extract links from page
- download_file(url, file_path): Download file
- check_website_status(url): Check website status
- extract_text_from_html(html_content): Extract text from HTML
- search_web(query, num_results): Search the web
- validate_url(url): Validate URL format
- get_webpage_metadata(url): Extract page metadata

SYSTEM OPERATIONS (8 functions):
- execute_command(command): Execute system command
- get_system_info(): Get system information
- get_process_list(limit): Get running processes
- get_environment_variable(variable_name): Get environment variable
- set_environment_variable(variable_name, value): Set environment variable
- get_current_directory(): Get current directory
- change_directory(directory_path): Change directory
- monitor_system_resources(): Monitor system resources

MATH OPERATIONS (5 functions):
- calculate(expression): Evaluate mathematical expression
- calculate_statistics(numbers): Calculate statistics
- convert_units(value, from_unit, to_unit, unit_type): Convert units
- generate_sequence(sequence_type, start, count): Generate number sequence
- solve_equation(equation_type, **params): Solve mathematical equation

TEXT OPERATIONS (7 functions):
- analyze_text(text): Analyze text properties
- find_replace(text, find_pattern, replace_with): Find and replace text
- extract_patterns(text, pattern, pattern_type): Extract patterns using regex
- format_text(text, format_type): Format text
- generate_hash(text, hash_type): Generate text hash
- split_text(text, delimiter, split_type): Split text
- join_text(text_parts, delimiter): Join text parts

DATETIME OPERATIONS (8 functions):
- get_current_time(timezone_name, format_string): Get current time
- parse_datetime(datetime_string, format_string): Parse datetime
- calculate_date_difference(start_date, end_date, unit): Calculate date difference
- add_time(base_date, amount, unit): Add time to date
- format_datetime(datetime_string, format_string): Format datetime
- get_calendar(year, month): Get calendar information
- is_weekend(date_string): Check if date is weekend
- get_timezone_info(): Get timezone information

RULES:
1. Always use exact function names from the list above
2. Provide all required parameters
3. Use {{previous_result}} to reference output from previous functions
4. Plan logical sequences where outputs feed into inputs
5. Be specific with parameter values
6. Respond only with valid JSON

EXAMPLES:
User: "Read invoice data and calculate March totals"
Response: {
  "plan": "Read CSV data, filter for March, calculate totals",
  "function_calls": [
    {"function_name": "read_csv", "parameters": {"file_path": "data/invoices.csv"}, "description": "Load invoice data"},
    {"function_name": "filter_data", "parameters": {"data": "{{previous_result}}", "column": "month", "operator": "equals", "value": "March"}, "description": "Filter March invoices"},
    {"function_name": "summarize_data", "parameters": {"data": "{{previous_result}}", "column": "amount"}, "description": "Calculate total amount"}
  ]
}"""
    
    def plan_function_calls(self, user_query: str, available_functions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Plan function calls based on user query"""
        try:
            # Create function descriptions for the prompt
            function_descriptions = self._create_function_descriptions(available_functions)
            
            # Create the full prompt
            prompt = f"""{self.system_prompt}

Available Functions:
{function_descriptions}

User Query: {user_query}

Response (JSON only):"""
            
            # Generate response
            response = self.model_manager.generate_text(
                prompt,
                max_length=1024,
                temperature=0.3  # Lower temperature for more consistent JSON
            )
            
            # Parse the response
            parsed_response = self._parse_response(response)
            
            if parsed_response is None:
                # Fallback: create a simple plan
                return self._create_fallback_plan(user_query)
            
            return parsed_response
            
        except Exception as e:
            logger.error(f"Error planning function calls: {e}")
            return self._create_fallback_plan(user_query)
    
    def _create_function_descriptions(self, available_functions: List[Dict[str, Any]]) -> str:
        """Create formatted function descriptions"""
        descriptions = []
        
        for func in available_functions:
            params = ", ".join([
                f"{p['name']}: {p['type']}" 
                for p in func.get('parameters', [])
            ])
            
            desc = f"- {func['name']}({params}): {func['description']}"
            descriptions.append(desc)
        
        return "\n".join(descriptions)
    
    def _parse_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse the AI model response to extract JSON"""
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            
            # If no JSON found, try to parse the entire response
            return json.loads(response)
            
        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response}")
            return None
    
    def _create_fallback_plan(self, user_query: str) -> Dict[str, Any]:
        """Create a fallback plan when AI parsing fails"""
        # Simple keyword-based fallback
        query_lower = user_query.lower()
        
        if "email" in query_lower and "send" in query_lower:
            return {
                "plan": "Send an email based on the user request",
                "function_calls": [
                    {
                        "function_name": "send_email",
                        "parameters": {
                            "to_email": "abhayrajputcse@gmail.com",
                            "subject": "Automated Email",
                            "body": "This is an automated email based on your request."
                        },
                        "description": "Send email to specified recipient"
                    }
                ]
            }
        
        elif "file" in query_lower and ("read" in query_lower or "open" in query_lower):
            return {
                "plan": "Read a file as requested",
                "function_calls": [
                    {
                        "function_name": "read_file",
                        "parameters": {
                            "file_path": "data/sample.txt"
                        },
                        "description": "Read the specified file"
                    }
                ]
            }
        
        elif "data" in query_lower and ("analyze" in query_lower or "process" in query_lower):
            return {
                "plan": "Analyze data as requested",
                "function_calls": [
                    {
                        "function_name": "read_csv",
                        "parameters": {
                            "file_path": "data/sample.csv"
                        },
                        "description": "Read CSV data for analysis"
                    },
                    {
                        "function_name": "summarize_data",
                        "parameters": {
                            "data": "{{output_from_previous}}",
                            "column": "amount"
                        },
                        "description": "Summarize the data"
                    }
                ]
            }
        
        else:
            return {
                "plan": "Get current system information",
                "function_calls": [
                    {
                        "function_name": "get_system_info",
                        "parameters": {},
                        "description": "Get basic system information"
                    }
                ]
            }
    
    def validate_function_calls(self, function_calls: List[Dict[str, Any]], available_functions: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """Validate that the planned function calls are valid"""
        errors = []
        available_function_names = {func['name'] for func in available_functions}
        
        for i, call in enumerate(function_calls):
            # Check if function exists
            if 'function_name' not in call:
                errors.append(f"Function call {i+1}: Missing 'function_name'")
                continue
            
            function_name = call['function_name']
            if function_name not in available_function_names:
                errors.append(f"Function call {i+1}: Unknown function '{function_name}'")
                continue
            
            # Check parameters
            if 'parameters' not in call:
                errors.append(f"Function call {i+1}: Missing 'parameters'")
                continue
            
            # Find function definition
            func_def = next((f for f in available_functions if f['name'] == function_name), None)
            if func_def:
                required_params = [p['name'] for p in func_def.get('parameters', []) if p.get('required', True)]
                provided_params = set(call['parameters'].keys())
                missing_params = set(required_params) - provided_params
                
                if missing_params:
                    errors.append(f"Function call {i+1}: Missing required parameters: {', '.join(missing_params)}")
        
        return len(errors) == 0, errors
    
    def optimize_function_sequence(self, function_calls: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Optimize the sequence of function calls"""
        # Simple optimization: remove duplicate calls
        seen = set()
        optimized = []
        
        for call in function_calls:
            call_signature = (call['function_name'], json.dumps(call['parameters'], sort_keys=True))
            if call_signature not in seen:
                seen.add(call_signature)
                optimized.append(call)
        
        return optimized
