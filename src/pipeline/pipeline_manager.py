"""
Pipeline Manager

Main orchestrator for the AI function calling pipeline.
"""

import asyncio
from typing import Dict, Any, Optional
from loguru import logger

from ..models.model_manager import ModelManager
from ..models.function_calling import FunctionCallingModel
from .query_processor import QueryProcessor
from .execution_engine import ExecutionEngine


class PipelineManager:
    """Main pipeline manager that orchestrates the entire process"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.model_manager = None
        self.function_calling_model = None
        self.query_processor = None
        self.execution_engine = None
        self.initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the pipeline components"""
        try:
            logger.info("Initializing AI Function Calling Pipeline...")
            
            # Initialize model manager
            self.model_manager = ModelManager(self.config_path)
            
            # Try to load a model
            if not self.model_manager.try_load_models():
                logger.error("Failed to load any AI model")
                return False
            
            # Initialize function calling model
            self.function_calling_model = FunctionCallingModel(self.model_manager)
            
            # Initialize query processor
            self.query_processor = QueryProcessor(self.function_calling_model)
            
            # Initialize execution engine
            self.execution_engine = ExecutionEngine()
            
            self.initialized = True
            logger.info("Pipeline initialization completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Pipeline initialization failed: {e}")
            return False
    
    async def process_query(self, query: str, execute: bool = True, simulate: bool = False) -> Dict[str, Any]:
        """Process a user query end-to-end"""
        if not self.initialized:
            return {
                "success": False,
                "error": "Pipeline not initialized. Call initialize() first."
            }
        
        try:
            logger.info(f"Processing query: {query}")
            
            # Step 1: Process the query to generate function call plan
            plan = self.query_processor.process_query(query)
            
            if not plan.get('valid', False):
                logger.warning("Generated plan is not valid")
            
            # Step 2: Execute the plan if requested
            execution_result = None
            if execute:
                if simulate:
                    execution_result = self.execution_engine.simulate_execution(plan)
                else:
                    execution_result = await self.execution_engine.execute_plan(plan)
            
            # Step 3: Create comprehensive result
            result = {
                "success": True,
                "query": query,
                "plan": plan,
                "execution_result": execution_result,
                "metadata": {
                    "model_info": self.model_manager.get_model_info(),
                    "pipeline_version": "1.0.0",
                    "timestamp": self._get_timestamp()
                }
            }
            
            logger.info("Query processing completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
    
    async def process_batch_queries(self, queries: list, execute: bool = True) -> Dict[str, Any]:
        """Process multiple queries in batch"""
        if not self.initialized:
            return {
                "success": False,
                "error": "Pipeline not initialized. Call initialize() first."
            }
        
        results = []
        successful = 0
        failed = 0
        
        for i, query in enumerate(queries):
            logger.info(f"Processing batch query {i+1}/{len(queries)}")
            
            result = await self.process_query(query, execute=execute)
            results.append(result)
            
            if result.get('success', False):
                successful += 1
            else:
                failed += 1
        
        return {
            "success": True,
            "batch_results": results,
            "summary": {
                "total_queries": len(queries),
                "successful": successful,
                "failed": failed,
                "success_rate": successful / len(queries) if queries else 0
            }
        }
    
    def get_available_functions(self) -> Dict[str, Any]:
        """Get information about all available functions"""
        if not self.initialized:
            return {"error": "Pipeline not initialized"}
        
        return {
            "functions": self.query_processor.function_registry.get_function_schemas(),
            "categories": list(self.query_processor.function_registry.categories.keys()),
            "total_functions": len(self.query_processor.function_registry.functions)
        }
    
    def search_functions(self, keyword: str) -> Dict[str, Any]:
        """Search for functions by keyword"""
        if not self.initialized:
            return {"error": "Pipeline not initialized"}
        
        return {
            "keyword": keyword,
            "functions": self.query_processor.search_functions(keyword)
        }
    
    def get_execution_history(self) -> Dict[str, Any]:
        """Get the execution history"""
        if not self.initialized:
            return {"error": "Pipeline not initialized"}
        
        return {
            "history": self.execution_engine.get_execution_history(),
            "total_executions": len(self.execution_engine.results_history)
        }
    
    def clear_history(self):
        """Clear execution history"""
        if self.initialized:
            self.execution_engine.clear_execution_history()
    
    def get_pipeline_status(self) -> Dict[str, Any]:
        """Get the current status of the pipeline"""
        return {
            "initialized": self.initialized,
            "model_loaded": self.model_manager.is_loaded() if self.model_manager else False,
            "model_info": self.model_manager.get_model_info() if self.model_manager else {},
            "available_functions": len(self.query_processor.function_registry.functions) if self.query_processor else 0
        }
    
    async def shutdown(self):
        """Shutdown the pipeline and cleanup resources"""
        logger.info("Shutting down pipeline...")
        
        if self.model_manager:
            self.model_manager.unload_model()
        
        if self.execution_engine:
            self.execution_engine.clear_execution_history()
        
        self.initialized = False
        logger.info("Pipeline shutdown completed")
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    async def __aenter__(self):
        """Async context manager entry"""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.shutdown()
