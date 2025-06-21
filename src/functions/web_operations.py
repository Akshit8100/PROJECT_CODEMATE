"""
Web Operations Functions
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import Any, Dict, List, Optional
from .base import BaseFunction


class FetchWebPageFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "fetch_web_page"
    
    @property
    def description(self) -> str:
        return "Fetch content from a web page"
    
    @property
    def category(self) -> str:
        return "web_operations"
    
    async def execute(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            
            return {
                "success": True,
                "content": response.text[:5000],  # Limit content size
                "status_code": response.status_code,
                "headers": dict(response.headers),
                "url": response.url
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class ExtractLinksFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "extract_links"
    
    @property
    def description(self) -> str:
        return "Extract all links from a web page"
    
    @property
    def category(self) -> str:
        return "web_operations"
    
    async def execute(self, url: str, base_url: Optional[str] = None) -> Dict[str, Any]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            links = []
            
            for link in soup.find_all('a', href=True):
                href = link['href']
                if base_url:
                    href = urljoin(base_url, href)
                
                links.append({
                    "url": href,
                    "text": link.get_text(strip=True),
                    "title": link.get('title', '')
                })
            
            return {"success": True, "links": links, "count": len(links)}
        except Exception as e:
            return {"success": False, "error": str(e)}


class DownloadFileFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "download_file"
    
    @property
    def description(self) -> str:
        return "Download a file from URL"
    
    @property
    def category(self) -> str:
        return "web_operations"
    
    async def execute(self, url: str, file_path: str, chunk_size: int = 8192) -> Dict[str, Any]:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # Create directory if it doesn't exist
            import os
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            total_size = 0
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        file.write(chunk)
                        total_size += len(chunk)
            
            return {
                "success": True,
                "file_path": file_path,
                "size": total_size,
                "content_type": response.headers.get('content-type', 'unknown')
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class CheckWebsiteStatusFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "check_website_status"
    
    @property
    def description(self) -> str:
        return "Check if a website is accessible"
    
    @property
    def category(self) -> str:
        return "web_operations"
    
    async def execute(self, url: str, timeout: int = 10) -> Dict[str, Any]:
        try:
            response = requests.head(url, timeout=timeout)
            
            return {
                "success": True,
                "status_code": response.status_code,
                "accessible": response.status_code < 400,
                "response_time": response.elapsed.total_seconds(),
                "headers": dict(response.headers)
            }
        except Exception as e:
            return {
                "success": False,
                "accessible": False,
                "error": str(e)
            }


class ExtractTextFromHTMLFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "extract_text_from_html"
    
    @property
    def description(self) -> str:
        return "Extract plain text from HTML content"
    
    @property
    def category(self) -> str:
        return "web_operations"
    
    async def execute(self, html_content: str, remove_scripts: bool = True) -> Dict[str, Any]:
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            if remove_scripts:
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
            
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return {
                "success": True,
                "text": text[:2000],  # Limit text size
                "length": len(text)
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class SearchWebFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "search_web"

    @property
    def description(self) -> str:
        return "Search the web using a search engine (simulation)"

    @property
    def category(self) -> str:
        return "web_operations"

    async def execute(self, query: str, num_results: int = 5) -> Dict[str, Any]:
        try:
            # This is a simulation - in real implementation, you'd use Google Custom Search API
            results = [
                {
                    "title": f"Search result {i+1} for '{query}'",
                    "url": f"https://example.com/result/{i+1}",
                    "snippet": f"This is a sample search result snippet for query '{query}'"
                }
                for i in range(num_results)
            ]

            return {
                "success": True,
                "results": results,
                "query": query,
                "simulation": True
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class ValidateURLFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "validate_url"

    @property
    def description(self) -> str:
        return "Validate if a URL is properly formatted"

    @property
    def category(self) -> str:
        return "web_operations"

    async def execute(self, url: str) -> Dict[str, Any]:
        try:
            from urllib.parse import urlparse

            parsed = urlparse(url)
            is_valid = bool(parsed.netloc) and bool(parsed.scheme)

            return {
                "success": True,
                "url": url,
                "is_valid": is_valid,
                "scheme": parsed.scheme,
                "domain": parsed.netloc,
                "path": parsed.path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


class GetWebPageMetadataFunction(BaseFunction):
    @property
    def name(self) -> str:
        return "get_webpage_metadata"

    @property
    def description(self) -> str:
        return "Extract metadata from a web page (title, description, etc.)"

    @property
    def category(self) -> str:
        return "web_operations"

    async def execute(self, url: str) -> Dict[str, Any]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            metadata = {
                "title": soup.title.string if soup.title else "No title",
                "description": "",
                "keywords": "",
                "author": "",
                "language": soup.get('lang', 'unknown')
            }

            # Extract meta tags
            for meta in soup.find_all('meta'):
                name = meta.get('name', '').lower()
                content = meta.get('content', '')

                if name == 'description':
                    metadata['description'] = content
                elif name == 'keywords':
                    metadata['keywords'] = content
                elif name == 'author':
                    metadata['author'] = content

            return {
                "success": True,
                "url": url,
                "metadata": metadata
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
