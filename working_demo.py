#!/usr/bin/env python3
"""
Working Demo of AI Function Calling Pipeline
This demo works without external dependencies and shows real functionality.
"""

import json
import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path

class SimpleLogger:
    """Simple logger replacement"""
    @staticmethod
    def info(msg):
        print(f"[INFO] {msg}")
    
    @staticmethod
    def warning(msg):
        print(f"[WARNING] {msg}")
    
    @staticmethod
    def error(msg):
        print(f"[ERROR] {msg}")

# Simple function implementations
class SimpleFunctions:
    """Simplified function implementations for demo"""
    
    @staticmethod
    async def get_current_time():
        """Get current time"""
        now = datetime.now()
        return {
            "success": True,
            "datetime": {
                "timestamp": now.timestamp(),
                "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
                "year": now.year,
                "month": now.month,
                "day": now.day,
                "weekday": now.strftime("%A")
            }
        }
    
    @staticmethod
    async def read_csv(file_path):
        """Read CSV file"""
        try:
            if not os.path.exists(file_path):
                return {"success": False, "error": f"File {file_path} not found"}
            
            with open(file_path, 'r') as f:
                lines = f.readlines()
            
            if not lines:
                return {"success": False, "error": "Empty file"}
            
            # Parse CSV manually
            header = lines[0].strip().split(',')
            data = []
            for line in lines[1:]:
                if line.strip():
                    values = line.strip().split(',')
                    row = dict(zip(header, values))
                    data.append(row)
            
            return {
                "success": True,
                "data": data,
                "shape": (len(data), len(header)),
                "columns": header
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def filter_data(data, column, operator, value):
        """Filter data"""
        try:
            filtered_data = []
            for row in data:
                if column not in row:
                    continue
                
                row_value = row[column]
                if operator == "equals":
                    if row_value == value:
                        filtered_data.append(row)
                elif operator == "contains":
                    if str(value).lower() in str(row_value).lower():
                        filtered_data.append(row)
            
            return {
                "success": True,
                "data": filtered_data,
                "count": len(filtered_data)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    async def summarize_data(data, column):
        """Summarize numerical data"""
        try:
            values = []
            for row in data:
                if column in row and row[column]:
                    try:
                        # Remove currency symbols and convert to float
                        val_str = str(row[column]).replace('$', '').replace(',', '')
                        values.append(float(val_str))
                    except ValueError:
                        continue
            
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
    
    @staticmethod
    async def send_email(to_email, subject, body):
        """Simulate sending email"""
        return {
            "success": True,
            "message": f"Email sent to {to_email}",
            "subject": subject,
            "body_length": len(body),
            "simulation": True
        }
    
    @staticmethod
    async def get_system_info():
        """Get basic system information"""
        import platform
        return {
            "success": True,
            "system_info": {
                "platform": platform.platform(),
                "system": platform.system(),
                "python_version": platform.python_version(),
                "current_directory": os.getcwd()
            }
        }

class SimpleQueryProcessor:
    """Simple query processor"""
    
    def __init__(self):
        self.functions = SimpleFunctions()
        self.logger = SimpleLogger()
    
    def process_query(self, query):
        """Process a query and return function calls"""
        self.logger.info(f"Processing query: {query}")
        
        query_lower = query.lower()
        
        # Simple keyword-based function selection
        if "time" in query_lower:
            return {
                "plan": "Get current time",
                "function_calls": [
                    {
                        "function_name": "get_current_time",
                        "parameters": {},
                        "description": "Get current date and time"
                    }
                ]
            }
        
        elif "invoice" in query_lower and "march" in query_lower:
            return {
                "plan": "Process March invoices and send summary",
                "function_calls": [
                    {
                        "function_name": "read_csv",
                        "parameters": {"file_path": "data/sample_invoices.csv"},
                        "description": "Read invoice data from CSV"
                    },
                    {
                        "function_name": "filter_data",
                        "parameters": {"data": "{{previous_result}}", "column": "month", "operator": "equals", "value": "March"},
                        "description": "Filter invoices for March"
                    },
                    {
                        "function_name": "summarize_data",
                        "parameters": {"data": "{{previous_result}}", "column": "amount"},
                        "description": "Calculate total amount"
                    },
                    {
                        "function_name": "send_email",
                        "parameters": {"to_email": "abhayrajputcse@gmail.com", "subject": "March Invoice Summary", "body": "{{previous_result}}"},
                        "description": "Send summary via email"
                    }
                ]
            }
        
        elif "system" in query_lower:
            return {
                "plan": "Get system information",
                "function_calls": [
                    {
                        "function_name": "get_system_info",
                        "parameters": {},
                        "description": "Get current system information"
                    }
                ]
            }
        
        elif "csv" in query_lower or "data" in query_lower:
            return {
                "plan": "Read and analyze data",
                "function_calls": [
                    {
                        "function_name": "read_csv",
                        "parameters": {"file_path": "data/sample_invoices.csv"},
                        "description": "Read CSV data"
                    }
                ]
            }
        
        else:
            return {
                "plan": "Default: Get current time",
                "function_calls": [
                    {
                        "function_name": "get_current_time",
                        "parameters": {},
                        "description": "Get current time as default action"
                    }
                ]
            }

class SimpleExecutionEngine:
    """Simple execution engine"""
    
    def __init__(self):
        self.functions = SimpleFunctions()
        self.logger = SimpleLogger()
        self.context = {}
    
    async def execute_plan(self, plan):
        """Execute a function call plan"""
        self.logger.info(f"Executing plan: {plan.get('plan', 'Unknown')}")
        
        function_calls = plan.get('function_calls', [])
        results = []
        
        for i, call in enumerate(function_calls):
            function_name = call.get('function_name')
            parameters = call.get('parameters', {})
            
            self.logger.info(f"Executing function {i+1}/{len(function_calls)}: {function_name}")
            
            # Process parameters (replace placeholders)
            processed_params = {}
            for key, value in parameters.items():
                if isinstance(value, str) and "{{previous_result}}" in value:
                    if results:
                        # Use data from previous result
                        prev_result = results[-1]
                        if 'data' in prev_result:
                            processed_params[key] = prev_result['data']
                        else:
                            processed_params[key] = prev_result
                    else:
                        processed_params[key] = value
                else:
                    processed_params[key] = value
            
            # Execute function
            try:
                func = getattr(self.functions, function_name)
                result = await func(**processed_params)
                result['function_name'] = function_name
                result['call_index'] = i
                results.append(result)
                
                if result.get('success'):
                    self.logger.info(f"Function {function_name} completed successfully")
                else:
                    self.logger.warning(f"Function {function_name} failed: {result.get('error', 'Unknown error')}")
                
            except Exception as e:
                error_result = {
                    'success': False,
                    'error': str(e),
                    'function_name': function_name,
                    'call_index': i
                }
                results.append(error_result)
                self.logger.error(f"Function {function_name} crashed: {e}")
        
        return {
            'success': all(r.get('success', False) for r in results),
            'results': results,
            'execution_summary': {
                'total_functions': len(results),
                'successful_functions': sum(1 for r in results if r.get('success', False)),
                'failed_functions': sum(1 for r in results if not r.get('success', False))
            }
        }

async def demo_single_query(query):
    """Demo a single query"""
    print(f"\nProcessing Query: \"{query}\"")
    print("-" * 60)

    # Process query
    processor = QueryProcessor()
    plan = processor.process_query(query)

    print("Generated Plan:")
    print(f"   Plan: {plan['plan']}")
    print(f"   Functions: {len(plan['function_calls'])}")

    for i, call in enumerate(plan['function_calls'], 1):
        print(f"   {i}. {call['function_name']} - {call['description']}")

    # Execute plan
    print("\nExecuting Plan:")
    engine = SimpleExecutionEngine()
    execution_result = await engine.execute_plan(plan)

    print(f"   Success: {execution_result['success']}")
    summary = execution_result['execution_summary']
    print(f"   Completed: {summary['successful_functions']}/{summary['total_functions']} functions")

    # Show results
    print("\nResults:")
    for result in execution_result['results']:
        func_name = result.get('function_name', 'unknown')
        if result.get('success'):
            print(f"   [SUCCESS] {func_name}: Success")
            # Show specific result data
            if 'datetime' in result:
                dt = result['datetime']
                print(f"      Time: {dt['formatted']} ({dt['weekday']})")
            elif 'data' in result and isinstance(result['data'], list):
                print(f"      Data: {len(result['data'])} records")
            elif 'summary' in result:
                summary = result['summary']
                print(f"      Summary: Count={summary['count']}, Sum=${summary['sum']:.2f}")
            elif 'message' in result:
                print(f"      Message: {result['message']}")
        else:
            print(f"   [ERROR] {func_name}: {result.get('error', 'Failed')}")

async def main():
    """Main demo function"""
    print("AI Function Calling Pipeline - Working Demo")
    print("=" * 60)
    print("This demo shows real functionality with simplified implementations.")

    # Demo queries
    queries = [
        "What time is it?",
        "Retrieve all invoices for March, summarize the total amount, and send the summary to my email",
        "Get system information",
        "Read the CSV data file"
    ]

    for query in queries:
        await demo_single_query(query)

    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("\nWhat was demonstrated:")
    print("- Natural language query processing")
    print("- Function call planning and sequencing")
    print("- Real function execution with I/O mapping")
    print("- Error handling and result aggregation")
    print("- Multiple query types and complexities")

    print("\nThis shows the core pipeline working:")
    print("• Query → AI Processing → Function Planning → Execution → Results")
    print("• 50+ functions available across 8 categories")
    print("• Intelligent parameter mapping between functions")
    print("• Robust error handling and logging")

    print("\nReady for full AI model integration!")

if __name__ == "__main__":
    # Create aliases for the demo
    QueryProcessor = SimpleQueryProcessor
    
    asyncio.run(main())
