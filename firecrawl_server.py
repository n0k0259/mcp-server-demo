from mcp.server.fastmcp import FastMCP
from firecrawl import FirecrawlApp
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("Firecrawl")

# Initialize Firecrawl with API key from environment
firecrawl_app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

@mcp.tool()
async def scrape_url(url: str, include_tags: Optional[List[str]] = None, exclude_tags: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Scrape a single URL and return its content.
    
    Args:
        url: The URL to scrape
        include_tags: List of HTML tags to include (optional)
        exclude_tags: List of HTML tags to exclude (optional)
    
    Returns:
        Dictionary containing scraped content including markdown, metadata, etc.
    """
    try:
        scrape_params = {
            "formats": ["markdown", "html"]
        }
        
        if include_tags:
            scrape_params["includeTags"] = include_tags
        if exclude_tags:
            scrape_params["excludeTags"] = exclude_tags
            
        result = firecrawl_app.scrape_url(url, scrape_params)
        return {
            "success": True,
            "url": url,
            "markdown": result.get("markdown", ""),
            "html": result.get("html", ""),
            "metadata": result.get("metadata", {}),
            "links": result.get("links", [])
        }
    except Exception as e:
        return {
            "success": False,
            "url": url,
            "error": str(e),
            "markdown": "",
            "html": "",
            "metadata": {},
            "links": []
        }

@mcp.tool()
async def search_web(query: str, num_results: int = 5) -> Dict[str, Any]:
    """
    Search the web using Firecrawl's search functionality.
    
    Args:
        query: The search query
        num_results: Number of results to return (default: 5, max: 10)
    
    Returns:
        Dictionary containing search results with URLs, titles, and snippets
    """
    try:
        # Limit num_results to prevent excessive API usage
        num_results = min(num_results, 10)
        
        search_params = {
            "limit": num_results,
            "scrapeOptions": {
                "formats": ["markdown"]
            }
        }
        
        result = firecrawl_app.search(query, search_params)
        
        return {
            "success": True,
            "query": query,
            "results": result.get("data", []),
            "total_results": len(result.get("data", []))
        }
    except Exception as e:
        return {
            "success": False,
            "query": query,
            "error": str(e),
            "results": [],
            "total_results": 0
        }

@mcp.tool()
async def crawl_website(url: str, max_pages: int = 5, include_paths: Optional[List[str]] = None, exclude_paths: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Crawl a website starting from a given URL.
    
    Args:
        url: The starting URL to crawl
        max_pages: Maximum number of pages to crawl (default: 5, max: 20)
        include_paths: List of path patterns to include (optional)
        exclude_paths: List of path patterns to exclude (optional)
    
    Returns:
        Dictionary containing crawled pages data
    """
    try:
        # Limit max_pages to prevent excessive API usage
        max_pages = min(max_pages, 20)
        
        crawl_params = {
            "limit": max_pages,
            "scrapeOptions": {
                "formats": ["markdown"]
            }
        }
        
        if include_paths:
            crawl_params["includePaths"] = include_paths
        if exclude_paths:
            crawl_params["excludePaths"] = exclude_paths
            
        result = firecrawl_app.crawl_url(url, crawl_params)
        
        return {
            "success": True,
            "starting_url": url,
            "pages_crawled": len(result.get("data", [])),
            "data": result.get("data", []),
            "metadata": result.get("metadata", {})
        }
    except Exception as e:
        return {
            "success": False,
            "starting_url": url,
            "error": str(e),
            "pages_crawled": 0,
            "data": [],
            "metadata": {}
        }

# @mcp.tool()
# async def extract_structured_data(url: str, schema: Dict[str, Any]) -> Dict[str, Any]:
#     """
#     Extract structured data from a URL using a provided schema.
    
#     Args:
#         url: The URL to extract data from
#         schema: JSON schema defining the structure of data to extract
    
#     Returns:
#         Dictionary containing extracted structured data
#     """
#     try:
#         scrape_params = {
#             "formats": ["extract"],
#             "extract": {
#                 "schema": schema
#             }
#         }
        
#         result = firecrawl_app.scrape_url(url, scrape_params)
        
#         return {
#             "success": True,
#             "url": url,
#             "extracted_data": result.get("extract", {}),
#             "metadata": result.get("metadata", {})
#         }
#     except Exception as e:
#         return {
#             "success": False,
#             "url": url,
#             "error": str(e),
#             "extracted_data": {},
#             "metadata": {}
#         }

if __name__ == "__main__":
    mcp.run(transport="stdio")