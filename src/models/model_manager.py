"""
Model Manager for handling different AI models
"""

import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    BitsAndBytesConfig,
    pipeline
)
from typing import Dict, Any, Optional, List
import yaml
import os
from loguru import logger


class ModelManager:
    """Manages AI model loading and inference"""
    
    def __init__(self, config_path: str = "config.yaml"):
        self.config = self._load_config(config_path)
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.device = self._get_device()
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            logger.warning(f"Could not load config: {e}. Using defaults.")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            "model": {
                "name": "mistralai/Mistral-7B-Instruct-v0.2",
                "device": "auto",
                "max_length": 2048,
                "temperature": 0.3,
                "top_p": 0.9
            },
            "alternative_models": [
                "mistralai/Mistral-7B-Instruct-v0.2",
                "microsoft/DialoGPT-medium",
                "NousResearch/Llama-2-7b-chat-hf",
                "teknium/OpenHermes-2.5-Mistral-7B",
                "HuggingFaceH4/zephyr-7b-beta",
                "gpt2-medium"
            ]
        }
    
    def _get_device(self) -> str:
        """Determine the best device to use"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def load_model(self, model_name: Optional[str] = None) -> bool:
        """Load the specified model"""
        if model_name is None:
            model_name = self.config["model"]["name"]
        
        try:
            logger.info(f"Loading model: {model_name}")
            
            # Configure quantization for large models if on GPU
            quantization_config = None
            if self.device == "cuda" and "7B" in model_name:
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16,
                    bnb_4bit_use_double_quant=True,
                    bnb_4bit_quant_type="nf4"
                )
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True,
                padding_side="left"
            )
            
            # Add pad token if it doesn't exist
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            model_kwargs = {
                "trust_remote_code": True,
                "torch_dtype": torch.float16 if self.device != "cpu" else torch.float32,
            }
            
            if quantization_config:
                model_kwargs["quantization_config"] = quantization_config
                model_kwargs["device_map"] = "auto"
            else:
                model_kwargs["device_map"] = self.device
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                **model_kwargs
            )
            
            # Create pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device_map="auto" if quantization_config else self.device,
                torch_dtype=torch.float16 if self.device != "cpu" else torch.float32,
            )
            
            logger.info(f"Successfully loaded model: {model_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            return False
    
    def try_load_models(self) -> bool:
        """Try loading models from the alternative list"""
        models_to_try = [self.config["model"]["name"]] + self.config.get("alternative_models", [])
        
        for model_name in models_to_try:
            logger.info(f"Attempting to load model: {model_name}")
            if self.load_model(model_name):
                return True
        
        logger.error("Failed to load any model")
        return False
    
    def generate_text(self, prompt: str, max_length: Optional[int] = None, **kwargs) -> str:
        """Generate text using the loaded model"""
        if self.pipeline is None:
            raise RuntimeError("No model loaded. Call load_model() first.")
        
        max_length = max_length or self.config["model"]["max_length"]
        temperature = kwargs.get("temperature", self.config["model"]["temperature"])
        top_p = kwargs.get("top_p", self.config["model"]["top_p"])
        
        try:
            # Generate text
            outputs = self.pipeline(
                prompt,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                num_return_sequences=1,
                return_full_text=False
            )
            
            generated_text = outputs[0]["generated_text"]
            return generated_text.strip()
            
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            raise
    
    def is_loaded(self) -> bool:
        """Check if a model is loaded"""
        return self.model is not None and self.tokenizer is not None
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the loaded model"""
        if not self.is_loaded():
            return {"loaded": False}
        
        return {
            "loaded": True,
            "model_name": self.model.config.name_or_path if hasattr(self.model.config, 'name_or_path') else "unknown",
            "device": self.device,
            "vocab_size": self.tokenizer.vocab_size,
            "max_length": self.config["model"]["max_length"]
        }
    
    def unload_model(self):
        """Unload the current model to free memory"""
        if self.model is not None:
            del self.model
            self.model = None
        
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        
        if self.pipeline is not None:
            del self.pipeline
            self.pipeline = None
        
        # Clear GPU cache if using CUDA
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        logger.info("Model unloaded successfully")
