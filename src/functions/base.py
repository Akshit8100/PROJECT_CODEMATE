"""
Base classes for the function library
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from pydantic import BaseModel, Field
import inspect
import json
from loguru import logger


class FunctionParameter(BaseModel):
    """Represents a function parameter"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Any = None


class FunctionSchema(BaseModel):
    """Schema for a function that can be called by the AI"""
    name: str
    description: str
    parameters: List[FunctionParameter]
    returns: str
    category: str
    examples: List[str] = []


class BaseFunction(ABC):
    """Base class for all callable functions"""
    
    def __init__(self):
        self.schema = self._generate_schema()
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Function name"""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Function description"""
        pass
    
    @property
    @abstractmethod
    def category(self) -> str:
        """Function category"""
        pass
    
    @property
    def examples(self) -> List[str]:
        """Usage examples"""
        return []
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the function with given parameters"""
        pass
    
    def _generate_schema(self) -> FunctionSchema:
        """Generate function schema from the execute method"""
        sig = inspect.signature(self.execute)
        parameters = []
        
        for param_name, param in sig.parameters.items():
            if param_name == 'self':
                continue
                
            param_type = str(param.annotation) if param.annotation != inspect.Parameter.empty else "Any"
            required = param.default == inspect.Parameter.empty
            default = param.default if param.default != inspect.Parameter.empty else None
            
            parameters.append(FunctionParameter(
                name=param_name,
                type=param_type,
                description=f"Parameter {param_name}",
                required=required,
                default=default
            ))
        
        return_type = str(sig.return_annotation) if sig.return_annotation != inspect.Signature.empty else "Any"
        
        return FunctionSchema(
            name=self.name,
            description=self.description,
            parameters=parameters,
            returns=return_type,
            category=self.category,
            examples=self.examples
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert function to dictionary representation"""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "parameters": [param.dict() for param in self.schema.parameters],
            "returns": self.schema.returns,
            "examples": self.examples
        }


class FunctionRegistry:
    """Registry for managing all available functions"""
    
    def __init__(self):
        self.functions: Dict[str, BaseFunction] = {}
        self.categories: Dict[str, List[str]] = {}
    
    def register(self, function: BaseFunction):
        """Register a function"""
        self.functions[function.name] = function
        
        if function.category not in self.categories:
            self.categories[function.category] = []
        self.categories[function.category].append(function.name)
        
        logger.info(f"Registered function: {function.name} ({function.category})")
    
    def get_function(self, name: str) -> Optional[BaseFunction]:
        """Get a function by name"""
        return self.functions.get(name)
    
    def get_functions_by_category(self, category: str) -> List[BaseFunction]:
        """Get all functions in a category"""
        if category not in self.categories:
            return []
        return [self.functions[name] for name in self.categories[category]]
    
    def get_all_functions(self) -> List[BaseFunction]:
        """Get all registered functions"""
        return list(self.functions.values())
    
    def get_function_schemas(self) -> List[Dict[str, Any]]:
        """Get schemas for all functions"""
        return [func.to_dict() for func in self.functions.values()]
    
    def auto_register_functions(self):
        """Auto-register all function classes in the module"""
        # This will be called after all modules are imported
        pass
    
    def to_json(self) -> str:
        """Export all function schemas to JSON"""
        return json.dumps(self.get_function_schemas(), indent=2)
