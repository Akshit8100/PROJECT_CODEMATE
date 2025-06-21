#!/usr/bin/env python3
"""
Interactive Demo - Try Your Own Queries Live!
"""

import asyncio
import sys
import os
from working_demo import SimpleQueryProcessor, SimpleExecutionEngine, SimpleLogger

def print_header():
    print("AI Function Calling Pipeline - Interactive Demo")
    print("=" * 60)
    print("Type your queries and see the pipeline process them live!")
    print("Available sample queries:")
    print("• 'What time is it?'")
    print("• 'Read invoice data and calculate totals'")
    print("• 'Get system information'")
    print("• 'Process March invoices and send email'")
    print("• 'Read CSV data'")
    print("\nType 'quit' to exit, 'help' for more info")
    print("=" * 60)

def show_help():
    print("\nAvailable Query Types:")
    print("Time queries: 'What time is it?', 'Get current time'")
    print("Data queries: 'Read CSV data', 'Load invoice data'")
    print("System queries: 'Get system info', 'Check system status'")
    print("Complex queries: 'Process March invoices and send email summary'")
    print("File queries: 'Read data file', 'Load CSV'")
    print("\nThe AI will automatically:")
    print("• Understand your natural language query")
    print("• Select appropriate functions from 50+ available")
    print("• Plan the execution sequence")
    print("• Execute functions with real data")
    print("• Show you the complete results")

async def process_user_query(query):
    """Process a user query and show results"""
    print(f"\nProcessing: \"{query}\"")
    print("-" * 50)

    # Process query
    processor = SimpleQueryProcessor()
    plan = processor.process_query(query)

    print("AI Analysis:")
    print(f"   Plan: {plan['plan']}")
    print(f"   Functions needed: {len(plan['function_calls'])}")

    print("\nFunction Sequence:")
    for i, call in enumerate(plan['function_calls'], 1):
        print(f"   {i}. {call['function_name']} - {call['description']}")

    # Execute plan
    print("\nLive Execution:")
    engine = SimpleExecutionEngine()
    execution_result = await engine.execute_plan(plan)

    # Show results
    print(f"\nResults:")
    print(f"   Overall Success: {'Yes' if execution_result['success'] else 'No'}")
    summary = execution_result['execution_summary']
    print(f"   Functions Completed: {summary['successful_functions']}/{summary['total_functions']}")

    print("\nDetailed Results:")
    for result in execution_result['results']:
        func_name = result.get('function_name', 'unknown')
        if result.get('success'):
            print(f"   [SUCCESS] {func_name}:")

            # Show specific result data
            if 'datetime' in result:
                dt = result['datetime']
                print(f"      Time: {dt['formatted']} ({dt['weekday']})")
            elif 'data' in result and isinstance(result['data'], list):
                print(f"      Loaded {len(result['data'])} records")
                if result['data']:
                    print(f"      Columns: {list(result['data'][0].keys())}")
            elif 'summary' in result:
                summary = result['summary']
                print(f"      Total: ${summary['sum']:.2f}")
                print(f"      Count: {summary['count']} items")
                print(f"      Average: ${summary['mean']:.2f}")
            elif 'message' in result:
                print(f"      Message: {result['message']}")
            elif 'system_info' in result:
                info = result['system_info']
                print(f"      System: {info['system']}")
                print(f"      Python: {info['python_version']}")
        else:
            print(f"   [ERROR] {func_name}: {result.get('error', 'Failed')}")

async def main():
    """Main interactive loop"""
    print_header()
    
    while True:
        try:
            # Get user input
            print("\n" + "="*60)
            query = input("Enter your query: ").strip()

            if not query:
                continue
            elif query.lower() in ['quit', 'exit', 'q']:
                print("\nThanks for trying the AI Function Calling Pipeline!")
                break
            elif query.lower() in ['help', 'h']:
                show_help()
                continue

            # Process the query
            await process_user_query(query)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    asyncio.run(main())
