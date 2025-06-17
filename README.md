# MCP Server Demo

This demo showcases multiple Model Context Protocol (MCP) servers working together with AWS Bedrock.

## Servers Included

1. **Math Server** (`mathserver.py`) - Basic arithmetic operations
2. **Weather Server** (`weather.py`) - Weather information (mock data)
3. **Firecrawl Server** (`firecrawl_server.py`) - Web scraping and crawling capabilities

## Setup

1. **Install dependencies:**
   ```bash
   uv install -r requirements.txt
   ```

2. **Configure environment variables:**
   Create a `.env` file with:
   ```env
   # AWS Configuration for Bedrock
   AWS_PROFILE=your-aws-profile-name
   AWS_REGION=us-east-1
   
   # Firecrawl API Key
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   ```

3. **Set up AWS credentials:**
   Make sure your AWS profile is configured in `~/.aws/credentials`:
   ```ini
   [your-profile-name]
   aws_access_key_id = YOUR_ACCESS_KEY
   aws_secret_access_key = YOUR_SECRET_KEY
   ```

4. **Get Firecrawl API Key:**
   - Sign up at [Firecrawl.dev](https://firecrawl.dev)
   - Get your API key from the dashboard
   - Add it to your `.env` file

## Running the Demo

### Option 1: Run all servers together (Recommended)
```bash
python client.py
```

### Option 2: Run servers individually

1. **Start the weather server:**
   ```bash
   python weather.py
   ```

2. **Test individual servers:**
   ```bash
   # Test math server
   python mathserver.py
   
   # Test firecrawl server
   python run_firecrawl_server.py
   ```

## Available Tools

### Math Server
- `add(a, b)` - Add two numbers
- `multiple(a, b)` - Multiply two numbers

### Weather Server
- `get_weather(location)` - Get weather for a location

### Firecrawl Server
- `scrape_url(url, include_tags, exclude_tags)` - Scrape content from a URL
- `search_web(query, num_results)` - Search the web
- `crawl_website(url, max_pages, include_paths, exclude_paths)` - Crawl a website
- `extract_structured_data(url, schema)` - Extract structured data using a schema

## Example Usage

The client will automatically test all servers with sample queries:

1. **Math**: "what's (3 + 5) x 12?"
2. **Weather**: "what is the weather in California?"
3. **Firecrawl Search**: "Search for 'Python web scraping tools' and give me the top 3 results"
4. **Firecrawl Scraping**: "Scrape the content from https://python.org and summarize what Python is"

## Architecture
# mcp-server-demo
