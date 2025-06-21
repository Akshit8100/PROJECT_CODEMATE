"""
Test cases for function library
"""

import pytest
import asyncio
import tempfile
import os
from pathlib import Path

# Add src to path
import sys
sys.path.append(str(Path(__file__).parent.parent / "src"))

from functions.data_processing import ReadCSVFunction, FilterDataFunction, SummarizeDataFunction
from functions.file_operations import ReadFileFunction, WriteFileFunction
from functions.text_operations import TextAnalysisFunction, FormatTextFunction
from functions.math_operations import CalculateFunction, StatisticsFunction
from functions.datetime_operations import GetCurrentTimeFunction


class TestDataProcessingFunctions:
    """Test data processing functions"""
    
    @pytest.mark.asyncio
    async def test_read_csv_function(self):
        """Test CSV reading function"""
        # Create a temporary CSV file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("name,age,city\n")
            f.write("John,25,New York\n")
            f.write("Jane,30,Los Angeles\n")
            temp_file = f.name
        
        try:
            func = ReadCSVFunction()
            result = await func.execute(temp_file)
            
            assert result['success'] is True
            assert len(result['data']) == 2
            assert result['data'][0]['name'] == 'John'
            assert result['data'][1]['age'] == '30'
        finally:
            os.unlink(temp_file)
    
    @pytest.mark.asyncio
    async def test_filter_data_function(self):
        """Test data filtering function"""
        data = [
            {'name': 'John', 'age': 25, 'city': 'New York'},
            {'name': 'Jane', 'age': 30, 'city': 'Los Angeles'},
            {'name': 'Bob', 'age': 25, 'city': 'Chicago'}
        ]
        
        func = FilterDataFunction()
        result = await func.execute(data, 'age', 'equals', 25)
        
        assert result['success'] is True
        assert len(result['data']) == 2
        assert all(row['age'] == 25 for row in result['data'])
    
    @pytest.mark.asyncio
    async def test_summarize_data_function(self):
        """Test data summarization function"""
        data = [
            {'amount': 100},
            {'amount': 200},
            {'amount': 300}
        ]
        
        func = SummarizeDataFunction()
        result = await func.execute(data, 'amount')
        
        assert result['success'] is True
        assert result['summary']['sum'] == 600
        assert result['summary']['mean'] == 200
        assert result['summary']['count'] == 3


class TestFileOperationsFunctions:
    """Test file operations functions"""
    
    @pytest.mark.asyncio
    async def test_write_and_read_file(self):
        """Test file writing and reading"""
        content = "Hello, World!\nThis is a test file."
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            temp_file = f.name
        
        try:
            # Test writing
            write_func = WriteFileFunction()
            write_result = await write_func.execute(temp_file, content)
            
            assert write_result['success'] is True
            
            # Test reading
            read_func = ReadFileFunction()
            read_result = await read_func.execute(temp_file)
            
            assert read_result['success'] is True
            assert read_result['content'] == content
            assert read_result['lines'] == 2
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestTextOperationsFunctions:
    """Test text operations functions"""
    
    @pytest.mark.asyncio
    async def test_text_analysis_function(self):
        """Test text analysis function"""
        text = "Hello world! This is a test. How are you?"
        
        func = TextAnalysisFunction()
        result = await func.execute(text)
        
        assert result['success'] is True
        assert result['analysis']['word_count'] == 8
        assert result['analysis']['sentence_count'] == 3
        assert result['analysis']['character_count'] == len(text)
    
    @pytest.mark.asyncio
    async def test_format_text_function(self):
        """Test text formatting function"""
        text = "hello world"
        
        func = FormatTextFunction()
        
        # Test uppercase
        result = await func.execute(text, 'uppercase')
        assert result['success'] is True
        assert result['formatted_text'] == "HELLO WORLD"
        
        # Test title case
        result = await func.execute(text, 'title')
        assert result['success'] is True
        assert result['formatted_text'] == "Hello World"


class TestMathOperationsFunctions:
    """Test math operations functions"""
    
    @pytest.mark.asyncio
    async def test_calculate_function(self):
        """Test calculation function"""
        func = CalculateFunction()
        
        # Test basic arithmetic
        result = await func.execute("2 + 3 * 4")
        assert result['success'] is True
        assert result['result'] == 14
        
        # Test with math functions
        result = await func.execute("sqrt(16)")
        assert result['success'] is True
        assert result['result'] == 4.0
    
    @pytest.mark.asyncio
    async def test_statistics_function(self):
        """Test statistics function"""
        numbers = [1, 2, 3, 4, 5]
        
        func = StatisticsFunction()
        result = await func.execute(numbers)
        
        assert result['success'] is True
        assert result['statistics']['mean'] == 3.0
        assert result['statistics']['sum'] == 15
        assert result['statistics']['count'] == 5


class TestDateTimeOperationsFunctions:
    """Test datetime operations functions"""
    
    @pytest.mark.asyncio
    async def test_get_current_time_function(self):
        """Test get current time function"""
        func = GetCurrentTimeFunction()
        result = await func.execute()
        
        assert result['success'] is True
        assert 'datetime' in result
        assert 'timestamp' in result['datetime']
        assert 'year' in result['datetime']
        assert 'month' in result['datetime']


class TestFunctionSchemas:
    """Test function schema generation"""
    
    def test_function_schema_generation(self):
        """Test that functions generate proper schemas"""
        func = ReadCSVFunction()
        schema = func.schema
        
        assert schema.name == "read_csv"
        assert schema.category == "data_processing"
        assert len(schema.parameters) > 0
        assert any(param.name == "file_path" for param in schema.parameters)
    
    def test_function_to_dict(self):
        """Test function to dictionary conversion"""
        func = CalculateFunction()
        func_dict = func.to_dict()
        
        assert 'name' in func_dict
        assert 'description' in func_dict
        assert 'category' in func_dict
        assert 'parameters' in func_dict
        assert func_dict['name'] == "calculate"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
