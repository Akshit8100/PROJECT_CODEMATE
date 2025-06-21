"""
Execution Engine

Executes function call sequences and manages input/output mapping.
"""

import asyncio
import json
from typing import Dict, Any, List, Optional, Union
from loguru import logger
from ..functions import registry


class ExecutionEngine:
    """Executes function call sequences with proper input/output mapping"""
    
    def __init__(self):
        self.function_registry = registry
        self.execution_context = {}
        self.results_history = []
    
    async def execute_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a complete function call plan"""
        try:
            logger.info(f"Executing plan: {plan.get('plan', 'Unknown plan')}")
            
            function_calls = plan.get('function_calls', [])
            if not function_calls:
                return self._create_execution_result(
                    plan, [], "No function calls to execute", False
                )
            
            results = []
            self.execution_context = {}
            
            for i, call in enumerate(function_calls):
                logger.info(f"Executing function {i+1}/{len(function_calls)}: {call.get('function_name', 'unknown')}")
                
                result = await self._execute_single_function(call, i)
                results.append(result)
                
                # Store result in context for future function calls
                self.execution_context[f"result_{i}"] = result
                
                # If function failed and it's critical, stop execution
                if not result.get('success', False) and self._is_critical_function(call):
                    logger.warning(f"Critical function failed: {call.get('function_name')}")
                    break
            
            # Determine overall success
            success = all(result.get('success', False) for result in results)
            
            execution_result = self._create_execution_result(
                plan, results, "Execution completed", success
            )
            
            # Store in history
            self.results_history.append(execution_result)
            
            return execution_result
            
        except Exception as e:
            logger.error(f"Error executing plan: {e}")
            return self._create_execution_result(
                plan, [], f"Execution error: {str(e)}", False
            )
    
    async def _execute_single_function(self, call: Dict[str, Any], call_index: int) -> Dict[str, Any]:
        """Execute a single function call"""
        try:
            function_name = call.get('function_name')
            parameters = call.get('parameters', {})
            description = call.get('description', '')
            
            # Get the function from registry
            function = self.function_registry.get_function(function_name)
            if not function:
                return {
                    'success': False,
                    'error': f"Function '{function_name}' not found",
                    'function_name': function_name,
                    'call_index': call_index
                }
            
            # Process parameters (handle references to previous results)
            processed_parameters = self._process_parameters(parameters)
            
            # Execute the function
            logger.debug(f"Calling {function_name} with parameters: {processed_parameters}")
            result = await function.execute(**processed_parameters)
            
            # Add metadata to result
            result.update({
                'function_name': function_name,
                'call_index': call_index,
                'description': description,
                'parameters_used': processed_parameters
            })
            
            logger.info(f"Function {function_name} completed with success: {result.get('success', False)}")
            return result
            
        except Exception as e:
            logger.error(f"Error executing function {call.get('function_name', 'unknown')}: {e}")
            return {
                'success': False,
                'error': str(e),
                'function_name': call.get('function_name', 'unknown'),
                'call_index': call_index
            }
    
    def _process_parameters(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Process parameters, resolving references to previous results"""
        processed = {}
        
        for key, value in parameters.items():
            if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
                # This is a reference to a previous result
                reference = value[2:-2].strip()
                resolved_value = self._resolve_reference(reference)
                processed[key] = resolved_value
            else:
                processed[key] = value
        
        return processed
    
    def _resolve_reference(self, reference: str) -> Any:
        """Resolve a reference to a previous result"""
        try:
            # Handle different types of references
            if reference == "output_from_previous":
                # Get the data from the most recent result
                if self.execution_context:
                    latest_key = max(self.execution_context.keys())
                    latest_result = self.execution_context[latest_key]
                    return latest_result.get('data', latest_result)
            
            elif reference.startswith("result_"):
                # Direct reference to a specific result
                if reference in self.execution_context:
                    result = self.execution_context[reference]
                    return result.get('data', result)
            
            elif "." in reference:
                # Nested reference like "result_0.data"
                parts = reference.split('.')
                obj = self.execution_context
                for part in parts:
                    if isinstance(obj, dict) and part in obj:
                        obj = obj[part]
                    else:
                        return None
                return obj
            
            # If no specific pattern matches, try to find it in context
            for context_key, context_value in self.execution_context.items():
                if reference in str(context_key):
                    return context_value.get('data', context_value)
            
            logger.warning(f"Could not resolve reference: {reference}")
            return None
            
        except Exception as e:
            logger.error(f"Error resolving reference '{reference}': {e}")
            return None
    
    def _is_critical_function(self, call: Dict[str, Any]) -> bool:
        """Determine if a function is critical for the overall plan"""
        function_name = call.get('function_name', '')
        
        # Consider data loading functions as critical
        critical_functions = [
            'read_csv', 'read_file', 'read_json', 'read_excel',
            'query_database', 'fetch_web_page'
        ]
        
        return function_name in critical_functions
    
    def _create_execution_result(self, plan: Dict[str, Any], results: List[Dict[str, Any]], 
                               message: str, success: bool) -> Dict[str, Any]:
        """Create a standardized execution result"""
        return {
            'success': success,
            'message': message,
            'plan': plan,
            'results': results,
            'execution_summary': {
                'total_functions': len(results),
                'successful_functions': sum(1 for r in results if r.get('success', False)),
                'failed_functions': sum(1 for r in results if not r.get('success', False)),
                'execution_time': self._get_timestamp()
            }
        }
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get the history of all executions"""
        return self.results_history.copy()
    
    def clear_execution_history(self):
        """Clear the execution history"""
        self.results_history.clear()
        self.execution_context.clear()
    
    def get_function_output(self, execution_result: Dict[str, Any], function_name: str) -> Optional[Any]:
        """Get the output of a specific function from an execution result"""
        results = execution_result.get('results', [])
        
        for result in results:
            if result.get('function_name') == function_name:
                return result.get('data', result)
        
        return None
    
    def simulate_execution(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate execution without actually running functions"""
        function_calls = plan.get('function_calls', [])
        simulated_results = []
        
        for i, call in enumerate(function_calls):
            function_name = call.get('function_name', 'unknown')
            
            # Create a simulated result
            simulated_result = {
                'success': True,
                'function_name': function_name,
                'call_index': i,
                'description': call.get('description', ''),
                'simulated': True,
                'message': f"Simulated execution of {function_name}"
            }
            
            simulated_results.append(simulated_result)
        
        return self._create_execution_result(
            plan, simulated_results, "Simulation completed", True
        )
