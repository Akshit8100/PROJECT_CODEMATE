"""
Text Operations Functions
"""

import re
import hashlib
from typing import Any, Dict, List, Optional
from .base import BaseFunction


class TextAnalysisFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "analyze_text"
    
    @property
    def description(self) -> str:
        return "Analyze text and provide statistics"
    
    @property
    def category(self) -> str:
        return "text_operations"
    
    async def execute(self, text: str) -> Dict[str, Any]:
        try:
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            paragraphs = text.split('\n\n')
            
            analysis = {
                "character_count": len(text),
                "character_count_no_spaces": len(text.replace(' ', '')),
                "word_count": len(words),
                "sentence_count": len([s for s in sentences if s.strip()]),
                "paragraph_count": len([p for p in paragraphs if p.strip()]),
                "average_word_length": sum(len(word) for word in words) / len(words) if words else 0,
                "average_sentence_length": len(words) / len([s for s in sentences if s.strip()]) if sentences else 0
            }
            
            return {"success": True, "analysis": analysis}
        except Exception as e:
            return {"success": False, "error": str(e)}


class FindReplaceFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "find_replace"
    
    @property
    def description(self) -> str:
        return "Find and replace text using patterns"
    
    @property
    def category(self) -> str:
        return "text_operations"
    
    async def execute(self, text: str, find_pattern: str, replace_with: str, use_regex: bool = False, case_sensitive: bool = True) -> Dict[str, Any]:
        try:
            if use_regex:
                flags = 0 if case_sensitive else re.IGNORECASE
                result_text = re.sub(find_pattern, replace_with, text, flags=flags)
                matches = len(re.findall(find_pattern, text, flags=flags))
            else:
                if case_sensitive:
                    result_text = text.replace(find_pattern, replace_with)
                    matches = text.count(find_pattern)
                else:
                    # Case-insensitive replacement
                    pattern = re.compile(re.escape(find_pattern), re.IGNORECASE)
                    result_text = pattern.sub(replace_with, text)
                    matches = len(pattern.findall(text))
            
            return {
                "success": True,
                "original_text": text[:100] + "..." if len(text) > 100 else text,
                "result_text": result_text,
                "replacements_made": matches
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class ExtractPatternsFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "extract_patterns"
    
    @property
    def description(self) -> str:
        return "Extract patterns from text using regex"
    
    @property
    def category(self) -> str:
        return "text_operations"
    
    async def execute(self, text: str, pattern: str, pattern_type: Optional[str] = None) -> Dict[str, Any]:
        try:
            if pattern_type:
                # Predefined patterns
                patterns = {
                    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                    "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                    "url": r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                    "ip": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
                    "date": r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
                }
                if pattern_type in patterns:
                    pattern = patterns[pattern_type]
                else:
                    return {"success": False, "error": f"Unknown pattern type: {pattern_type}"}
            
            matches = re.findall(pattern, text)
            
            return {
                "success": True,
                "pattern": pattern,
                "matches": matches,
                "count": len(matches)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class FormatTextFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "format_text"
    
    @property
    def description(self) -> str:
        return "Format text in various ways"
    
    @property
    def category(self) -> str:
        return "text_operations"
    
    async def execute(self, text: str, format_type: str) -> Dict[str, Any]:
        try:
            if format_type == "uppercase":
                result = text.upper()
            elif format_type == "lowercase":
                result = text.lower()
            elif format_type == "title":
                result = text.title()
            elif format_type == "capitalize":
                result = text.capitalize()
            elif format_type == "reverse":
                result = text[::-1]
            elif format_type == "remove_spaces":
                result = text.replace(' ', '')
            elif format_type == "normalize_spaces":
                result = re.sub(r'\s+', ' ', text).strip()
            elif format_type == "remove_punctuation":
                result = re.sub(r'[^\w\s]', '', text)
            else:
                return {"success": False, "error": f"Unknown format type: {format_type}"}
            
            return {
                "success": True,
                "original_text": text,
                "formatted_text": result,
                "format_type": format_type
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class GenerateHashFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "generate_hash"
    
    @property
    def description(self) -> str:
        return "Generate hash for text"
    
    @property
    def category(self) -> str:
        return "text_operations"
    
    async def execute(self, text: str, hash_type: str = "md5") -> Dict[str, Any]:
        try:
            text_bytes = text.encode('utf-8')
            
            if hash_type == "md5":
                hash_obj = hashlib.md5(text_bytes)
            elif hash_type == "sha1":
                hash_obj = hashlib.sha1(text_bytes)
            elif hash_type == "sha256":
                hash_obj = hashlib.sha256(text_bytes)
            elif hash_type == "sha512":
                hash_obj = hashlib.sha512(text_bytes)
            else:
                return {"success": False, "error": f"Unsupported hash type: {hash_type}"}
            
            return {
                "success": True,
                "text": text,
                "hash_type": hash_type,
                "hash": hash_obj.hexdigest()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class SplitTextFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "split_text"
    
    @property
    def description(self) -> str:
        return "Split text by delimiter or pattern"
    
    @property
    def category(self) -> str:
        return "text_operations"
    
    async def execute(self, text: str, delimiter: str = None, max_splits: int = -1, split_type: str = "delimiter") -> Dict[str, Any]:
        try:
            if split_type == "delimiter":
                if delimiter is None:
                    parts = text.split()  # Split by whitespace
                else:
                    parts = text.split(delimiter, max_splits)
            elif split_type == "lines":
                parts = text.splitlines()
            elif split_type == "words":
                parts = text.split()
            elif split_type == "sentences":
                parts = re.split(r'[.!?]+', text)
                parts = [p.strip() for p in parts if p.strip()]
            else:
                return {"success": False, "error": f"Unknown split type: {split_type}"}
            
            return {
                "success": True,
                "original_text": text[:100] + "..." if len(text) > 100 else text,
                "parts": parts,
                "count": len(parts)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class JoinTextFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "join_text"
    
    @property
    def description(self) -> str:
        return "Join text parts with delimiter"
    
    @property
    def category(self) -> str:
        return "text_operations"
    
    async def execute(self, text_parts: List[str], delimiter: str = " ") -> Dict[str, Any]:
        try:
            result = delimiter.join(text_parts)
            
            return {
                "success": True,
                "parts": text_parts,
                "delimiter": delimiter,
                "result": result
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
