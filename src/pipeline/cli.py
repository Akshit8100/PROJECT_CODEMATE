"""
Command Line Interface for the AI Function Calling Pipeline
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.json import JSON
from rich.prompt import Prompt, Confirm
from loguru import logger

from .pipeline_manager import PipelineManager

app = typer.Typer(help="AI Function Calling Pipeline CLI")
console = Console()

# Global pipeline manager
pipeline_manager: Optional[PipelineManager] = None


@app.command()
async def interactive():
    """Start interactive mode"""
    global pipeline_manager
    
    console.print(Panel.fit(
        "[bold blue]AI Function Calling Pipeline[/bold blue]\n"
        "Interactive Mode",
        border_style="blue"
    ))
    
    # Initialize pipeline
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Initializing pipeline...", total=None)
        
        pipeline_manager = PipelineManager()
        success = await pipeline_manager.initialize()
        
        if not success:
            console.print("[red]Failed to initialize pipeline![/red]")
            return
    
    console.print("[green]Pipeline initialized successfully![/green]")
    
    # Show available commands
    console.print("\n[bold]Available commands:[/bold]")
    console.print("• Type your query to process it")
    console.print("• 'functions' - List available functions")
    console.print("• 'search <keyword>' - Search functions")
    console.print("• 'history' - Show execution history")
    console.print("• 'status' - Show pipeline status")
    console.print("• 'help' - Show this help")
    console.print("• 'quit' or 'exit' - Exit the program")
    
    # Interactive loop
    while True:
        try:
            user_input = Prompt.ask("\n[bold cyan]Query[/bold cyan]").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                break
            elif user_input.lower() == 'help':
                show_help()
            elif user_input.lower() == 'functions':
                await show_functions()
            elif user_input.lower().startswith('search '):
                keyword = user_input[7:].strip()
                await search_functions(keyword)
            elif user_input.lower() == 'history':
                await show_history()
            elif user_input.lower() == 'status':
                await show_status()
            elif user_input:
                await process_query_interactive(user_input)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
    
    # Cleanup
    if pipeline_manager:
        await pipeline_manager.shutdown()
    
    console.print("\n[yellow]Goodbye![/yellow]")


@app.command()
async def query(
    text: str = typer.Argument(..., help="Query text to process"),
    execute: bool = typer.Option(True, "--execute/--no-execute", help="Execute the plan"),
    simulate: bool = typer.Option(False, "--simulate", help="Simulate execution"),
    output_file: Optional[str] = typer.Option(None, "--output", help="Save result to file")
):
    """Process a single query"""
    global pipeline_manager
    
    console.print(f"[bold]Processing query:[/bold] {text}")
    
    # Initialize pipeline
    pipeline_manager = PipelineManager()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Initializing pipeline...", total=None)
        success = await pipeline_manager.initialize()
        
        if not success:
            console.print("[red]Failed to initialize pipeline![/red]")
            return
        
        progress.update(task, description="Processing query...")
        result = await pipeline_manager.process_query(text, execute=execute, simulate=simulate)
    
    # Display result
    display_result(result)
    
    # Save to file if requested
    if output_file:
        save_result_to_file(result, output_file)
    
    # Cleanup
    await pipeline_manager.shutdown()


@app.command()
async def batch(
    file_path: str = typer.Argument(..., help="Path to file containing queries (one per line)"),
    execute: bool = typer.Option(True, "--execute/--no-execute", help="Execute the plans"),
    output_file: Optional[str] = typer.Option(None, "--output", help="Save results to file")
):
    """Process multiple queries from a file"""
    global pipeline_manager
    
    # Read queries from file
    try:
        with open(file_path, 'r') as f:
            queries = [line.strip() for line in f if line.strip()]
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return
    
    console.print(f"[bold]Processing {len(queries)} queries from {file_path}[/bold]")
    
    # Initialize pipeline
    pipeline_manager = PipelineManager()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        init_task = progress.add_task("Initializing pipeline...", total=None)
        success = await pipeline_manager.initialize()
        
        if not success:
            console.print("[red]Failed to initialize pipeline![/red]")
            return
        
        progress.remove_task(init_task)
        batch_task = progress.add_task("Processing queries...", total=len(queries))
        
        result = await pipeline_manager.process_batch_queries(queries, execute=execute)
        progress.update(batch_task, completed=len(queries))
    
    # Display summary
    summary = result.get('summary', {})
    console.print(f"\n[bold]Batch Processing Summary:[/bold]")
    console.print(f"Total queries: {summary.get('total_queries', 0)}")
    console.print(f"Successful: {summary.get('successful', 0)}")
    console.print(f"Failed: {summary.get('failed', 0)}")
    console.print(f"Success rate: {summary.get('success_rate', 0):.1%}")
    
    # Save to file if requested
    if output_file:
        save_result_to_file(result, output_file)
    
    # Cleanup
    await pipeline_manager.shutdown()


async def process_query_interactive(query: str):
    """Process a query in interactive mode"""
    global pipeline_manager
    
    if not pipeline_manager:
        console.print("[red]Pipeline not initialized![/red]")
        return
    
    # Ask user preferences
    execute = Confirm.ask("Execute the plan?", default=True)
    simulate = False
    if execute:
        simulate = Confirm.ask("Simulate execution?", default=False)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing query...", total=None)
        result = await pipeline_manager.process_query(query, execute=execute, simulate=simulate)
    
    display_result(result)


def display_result(result: dict):
    """Display query processing result"""
    if not result.get('success', False):
        console.print(f"[red]Error: {result.get('error', 'Unknown error')}[/red]")
        return
    
    plan = result.get('plan', {})
    execution_result = result.get('execution_result')
    
    # Display plan
    console.print("\n[bold]Generated Plan:[/bold]")
    console.print(f"Plan: {plan.get('plan', 'No description')}")
    
    function_calls = plan.get('function_calls', [])
    if function_calls:
        table = Table(title="Function Calls")
        table.add_column("Step", style="cyan")
        table.add_column("Function", style="magenta")
        table.add_column("Description", style="green")
        
        for i, call in enumerate(function_calls):
            table.add_row(
                str(i + 1),
                call.get('function_name', 'Unknown'),
                call.get('description', 'No description')
            )
        
        console.print(table)
    
    # Display execution results if available
    if execution_result:
        console.print(f"\n[bold]Execution Result:[/bold]")
        summary = execution_result.get('execution_summary', {})
        console.print(f"Success: {execution_result.get('success', False)}")
        console.print(f"Total functions: {summary.get('total_functions', 0)}")
        console.print(f"Successful: {summary.get('successful_functions', 0)}")
        console.print(f"Failed: {summary.get('failed_functions', 0)}")


async def show_functions():
    """Show available functions"""
    global pipeline_manager
    
    if not pipeline_manager:
        console.print("[red]Pipeline not initialized![/red]")
        return
    
    functions_info = pipeline_manager.get_available_functions()
    
    console.print(f"\n[bold]Available Functions ({functions_info.get('total_functions', 0)}):[/bold]")
    
    categories = functions_info.get('categories', [])
    for category in categories:
        console.print(f"\n[bold cyan]{category.title()}:[/bold cyan]")
        
        category_functions = [
            f for f in functions_info.get('functions', [])
            if f.get('category') == category
        ]
        
        for func in category_functions:
            console.print(f"  • {func.get('name', 'Unknown')}: {func.get('description', 'No description')}")


async def search_functions(keyword: str):
    """Search functions by keyword"""
    global pipeline_manager
    
    if not pipeline_manager:
        console.print("[red]Pipeline not initialized![/red]")
        return
    
    search_result = pipeline_manager.search_functions(keyword)
    functions = search_result.get('functions', [])
    
    console.print(f"\n[bold]Search results for '{keyword}' ({len(functions)} found):[/bold]")
    
    for func in functions:
        console.print(f"• [cyan]{func.get('name', 'Unknown')}[/cyan] ({func.get('category', 'Unknown')})")
        console.print(f"  {func.get('description', 'No description')}")


async def show_history():
    """Show execution history"""
    global pipeline_manager
    
    if not pipeline_manager:
        console.print("[red]Pipeline not initialized![/red]")
        return
    
    history_info = pipeline_manager.get_execution_history()
    history = history_info.get('history', [])
    
    console.print(f"\n[bold]Execution History ({len(history)} executions):[/bold]")
    
    for i, execution in enumerate(history):
        plan = execution.get('plan', {})
        summary = execution.get('execution_summary', {})
        
        console.print(f"\n{i + 1}. Query: {plan.get('query', 'Unknown')}")
        console.print(f"   Success: {execution.get('success', False)}")
        console.print(f"   Functions: {summary.get('total_functions', 0)}")


async def show_status():
    """Show pipeline status"""
    global pipeline_manager
    
    if not pipeline_manager:
        console.print("[red]Pipeline not initialized![/red]")
        return
    
    status = pipeline_manager.get_pipeline_status()
    
    console.print("\n[bold]Pipeline Status:[/bold]")
    console.print(f"Initialized: {status.get('initialized', False)}")
    console.print(f"Model loaded: {status.get('model_loaded', False)}")
    console.print(f"Available functions: {status.get('available_functions', 0)}")
    
    model_info = status.get('model_info', {})
    if model_info.get('loaded', False):
        console.print(f"Model: {model_info.get('model_name', 'Unknown')}")
        console.print(f"Device: {model_info.get('device', 'Unknown')}")


def show_help():
    """Show help information"""
    console.print("\n[bold]Available commands:[/bold]")
    console.print("• Type your query to process it")
    console.print("• 'functions' - List available functions")
    console.print("• 'search <keyword>' - Search functions")
    console.print("• 'history' - Show execution history")
    console.print("• 'status' - Show pipeline status")
    console.print("• 'help' - Show this help")
    console.print("• 'quit' or 'exit' - Exit the program")


def save_result_to_file(result: dict, file_path: str):
    """Save result to file"""
    try:
        with open(file_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        console.print(f"[green]Result saved to {file_path}[/green]")
    except Exception as e:
        console.print(f"[red]Error saving file: {e}[/red]")


async def main():
    """Main CLI entry point"""
    # Configure logging
    logger.remove()
    logger.add(
        "logs/pipeline.log",
        rotation="10 MB",
        retention="7 days",
        level="INFO"
    )
    
    # Run the CLI app
    await app()


if __name__ == "__main__":
    asyncio.run(main())
