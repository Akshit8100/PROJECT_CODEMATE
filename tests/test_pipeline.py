"""
Test cases for the pipeline components
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock
from pathlib import Path

# Add src to path
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from pipeline.pipeline_manager import PipelineManager
from pipeline.query_processor import QueryProcessor
from pipeline.execution_engine import ExecutionEngine
from models.function_calling import FunctionCallingModel


class TestPipelineManager:
    """Test the main pipeline manager"""
    
    @pytest.mark.asyncio
    async def test_pipeline_initialization(self):
        """Test pipeline initialization"""
        # This test might fail if models can't be loaded, so we'll mock it
        pipeline = PipelineManager()
        
        # Mock the model loading
        pipeline.model_manager = Mock()
        pipeline.model_manager.try_load_models = Mock(return_value=True)
        pipeline.model_manager.get_model_info = Mock(return_value={"loaded": True})
        pipeline.model_manager.is_loaded = Mock(return_value=True)
        
        success = await pipeline.initialize()
        assert success is True
        assert pipeline.initialized is True
    
    def test_pipeline_status(self):
        """Test pipeline status reporting"""
        pipeline = PipelineManager()
        status = pipeline.get_pipeline_status()
        
        assert 'initialized' in status
        assert 'model_loaded' in status
        assert 'available_functions' in status


class TestQueryProcessor:
    """Test the query processor"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Mock the function calling model
        self.mock_model = Mock()
        self.mock_model.plan_function_calls = Mock(return_value={
            "plan": "Test plan",
            "function_calls": [
                {
                    "function_name": "test_function",
                    "parameters": {"param1": "value1"},
                    "description": "Test function call"
                }
            ]
        })
        self.mock_model.validate_function_calls = Mock(return_value=(True, []))
        self.mock_model.optimize_function_sequence = Mock(side_effect=lambda x: x)
        
        self.processor = QueryProcessor(self.mock_model)
    
    def test_query_preprocessing(self):
        """Test query preprocessing"""
        query = "  Send   an  email  w/  invoice  data  "
        processed = self.processor._preprocess_query(query)
        
        assert "with" in processed
        assert "  " not in processed  # Multiple spaces should be normalized
    
    def test_process_query(self):
        """Test complete query processing"""
        query = "Send an email with invoice data"
        result = self.processor.process_query(query)
        
        assert 'plan' in result
        assert 'function_calls' in result
        assert 'query' in result
        assert result['query'] == query
    
    def test_analyze_query_complexity(self):
        """Test query complexity analysis"""
        simple_query = "What time is it?"
        complex_query = "Read data, filter it, analyze results, and send email report"
        
        simple_analysis = self.processor.analyze_query_complexity(simple_query)
        complex_analysis = self.processor.analyze_query_complexity(complex_query)
        
        assert simple_analysis['complexity'] == 'simple'
        assert complex_analysis['complexity'] in ['moderate', 'complex']
        assert complex_analysis['complexity_score'] > simple_analysis['complexity_score']


class TestExecutionEngine:
    """Test the execution engine"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.engine = ExecutionEngine()
    
    @pytest.mark.asyncio
    async def test_execute_plan_empty(self):
        """Test executing an empty plan"""
        plan = {"function_calls": []}
        result = await self.engine.execute_plan(plan)
        
        assert result['success'] is False
        assert "No function calls" in result['message']
    
    def test_parameter_processing(self):
        """Test parameter processing with references"""
        # Setup some context
        self.engine.execution_context = {
            "result_0": {"data": [{"amount": 100}, {"amount": 200}]}
        }
        
        parameters = {
            "data": "{{output_from_previous}}",
            "column": "amount"
        }
        
        processed = self.engine._process_parameters(parameters)
        
        assert processed['column'] == "amount"
        assert processed['data'] == [{"amount": 100}, {"amount": 200}]
    
    def test_reference_resolution(self):
        """Test reference resolution"""
        self.engine.execution_context = {
            "result_0": {"data": "test_data", "success": True}
        }
        
        # Test direct reference
        result = self.engine._resolve_reference("result_0")
        assert result == {"data": "test_data", "success": True}
        
        # Test nested reference
        result = self.engine._resolve_reference("result_0.data")
        assert result == "test_data"
    
    def test_simulation_mode(self):
        """Test execution simulation"""
        plan = {
            "function_calls": [
                {
                    "function_name": "test_function",
                    "parameters": {},
                    "description": "Test function"
                }
            ]
        }
        
        result = self.engine.simulate_execution(plan)
        
        assert result['success'] is True
        assert len(result['results']) == 1
        assert result['results'][0]['simulated'] is True


class TestFunctionCalling:
    """Test the function calling model"""
    
    def setup_method(self):
        """Setup test fixtures"""
        # Mock model manager
        self.mock_model_manager = Mock()
        self.mock_model_manager.generate_text = Mock(return_value='{"plan": "test", "function_calls": []}')
        
        self.function_calling = FunctionCallingModel(self.mock_model_manager)
    
    def test_system_prompt_creation(self):
        """Test system prompt creation"""
        prompt = self.function_calling._create_system_prompt()
        
        assert "function_name" in prompt
        assert "parameters" in prompt
        assert "JSON" in prompt
    
    def test_response_parsing(self):
        """Test JSON response parsing"""
        # Test valid JSON
        valid_response = '{"plan": "test plan", "function_calls": []}'
        result = self.function_calling._parse_response(valid_response)
        
        assert result is not None
        assert result['plan'] == "test plan"
        
        # Test invalid JSON
        invalid_response = "This is not JSON"
        result = self.function_calling._parse_response(invalid_response)
        
        assert result is None
    
    def test_fallback_plan_creation(self):
        """Test fallback plan creation"""
        # Test email query
        email_query = "send an email to john@example.com"
        plan = self.function_calling._create_fallback_plan(email_query)
        
        assert 'function_calls' in plan
        assert len(plan['function_calls']) > 0
        assert plan['function_calls'][0]['function_name'] == 'send_email'
        
        # Test file query
        file_query = "read the data file"
        plan = self.function_calling._create_fallback_plan(file_query)
        
        assert plan['function_calls'][0]['function_name'] == 'read_file'
    
    def test_function_validation(self):
        """Test function call validation"""
        available_functions = [
            {
                'name': 'test_function',
                'parameters': [
                    {'name': 'required_param', 'required': True},
                    {'name': 'optional_param', 'required': False}
                ]
            }
        ]
        
        # Test valid function call
        valid_calls = [
            {
                'function_name': 'test_function',
                'parameters': {'required_param': 'value'}
            }
        ]
        
        is_valid, errors = self.function_calling.validate_function_calls(valid_calls, available_functions)
        assert is_valid is True
        assert len(errors) == 0
        
        # Test invalid function call (missing required parameter)
        invalid_calls = [
            {
                'function_name': 'test_function',
                'parameters': {}
            }
        ]
        
        is_valid, errors = self.function_calling.validate_function_calls(invalid_calls, available_functions)
        assert is_valid is False
        assert len(errors) > 0


class TestIntegration:
    """Integration tests"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_simulation(self):
        """Test end-to-end pipeline simulation"""
        # This test uses mocked components to avoid model loading
        pipeline = PipelineManager()
        
        # Mock all components
        pipeline.model_manager = Mock()
        pipeline.model_manager.try_load_models = Mock(return_value=True)
        pipeline.model_manager.get_model_info = Mock(return_value={"loaded": True})
        pipeline.model_manager.is_loaded = Mock(return_value=True)
        
        # Initialize
        success = await pipeline.initialize()
        assert success is True
        
        # Mock the query processing
        pipeline.query_processor.process_query = Mock(return_value={
            "plan": "Test plan",
            "function_calls": [
                {
                    "function_name": "get_current_time",
                    "parameters": {},
                    "description": "Get current time"
                }
            ],
            "valid": True,
            "query": "What time is it?"
        })
        
        # Process a query
        result = await pipeline.process_query("What time is it?", execute=False)
        
        assert result['success'] is True
        assert 'plan' in result
        assert 'query' in result


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
