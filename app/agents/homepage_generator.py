"""
Homepage Content Generator Agent System

This module implements a system for automatically generating website homepage content
using a multi-agent approach based on JSON mapping configuration.

The system follows these steps:
1. Crawl a target website to extract content
2. Load JSON mapping with section structure and prompts
3. Process each section/subsection with specialized AI agents
4. Assemble generated content into a complete homepage document
5. Export final document in markdown or HTML format
"""

from typing import Dict, List, Optional, Any, Iterator, Tuple
import json
import os
from pathlib import Path

from agno.agent import Agent, RunResponse
from agno.models.anthropic import Claude
from agno.tools.crawl4ai import Crawl4aiTools
from agno.utils.pprint import pprint_run_response
from app.core import settings


class HomepageGeneratorAgent:
    """
    Agent system for generating complete website homepage content based on
    a structured JSON mapping and target website content.
    """
    
    def __init__(self):
        """Initialize the homepage generator agent system."""
        self.AGENT_STORAGE = settings.AGENT_STORAGE
        self._load_mapping()
        self._setup_agents()
        
    def _load_mapping(self):
        """Load the homepage mapping JSON file."""
        mapping_path = Path(__file__).parent / "home_page_mapping.json"
        
        with open(mapping_path, 'r') as f:
            self.mapping = json.load(f)
        
        print(f"Loaded homepage mapping with {len(self.mapping['homepage_sections'])} sections.")
        
    def _setup_agents(self):
        """Set up the different specialized agents used in the content generation pipeline."""
        # Create a Crawl4aiTools instance with direct scraping mode to avoid asyncio issues
        self.crawl_tool = Crawl4aiTools(max_length=None)
        
        # Crawler agent for extracting website content
        self.crawler_agent = self._create_crawler_agent()
        
        # Content generator agent for creating section content
        self.content_generator = self._create_content_generator_agent()
        
        # Document composer for assembling the final output
        self.document_composer = self._create_document_composer_agent()
        
    def _create_crawler_agent(self):
        """Create an agent specialized in crawling websites and extracting content."""
        return Agent(
            name="Website Crawler Agent",
            role="You are an expert at crawling websites and extracting relevant content for analysis",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Crawl website URLs to extract text content",
                "Focus on extracting primary content, not navigation or footer elements",
                "Identify and categorize content by page sections",
                "Extract headings, paragraphs, lists, and other structured content",
                "Ignore boilerplate and template elements",
                "Provide content in a clean, structured format",
                "Extract any relevant metadata like page titles and descriptions",
                "Identify key messaging and unique selling propositions",
                "Format output as structured JSON with sections and content types",
                "Assign content relevance scores to help with prompt generation"
            ],
            show_tool_calls=True,
            # Use direct HTML content instead of the Crawl4aiTools which uses asyncio.run() internally
            tools=[],  # We'll manually fetch the website content to avoid asyncio issues
            stream=True,
            markdown=True,
        )
        
    def _create_content_generator_agent(self):
        """Create an agent specialized in generating content from prompts."""
        return Agent(
            name="Content Generator Agent",
            role="You are an expert marketing copywriter specialized in creating compelling website content",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=8096),
            instructions=[
                "Generate high-quality marketing content based on prompts and website data",
                "Adapt your writing style to match the appropriate tone for each section",
                "Create concise, impactful copy that follows SEO best practices",
                "Use persuasive language that drives conversions and engagement",
                "Ensure all content is factually accurate and based on the provided information",
                "Generate content that aligns with the brand voice and company values",
                "Create compelling headlines, subheadlines, and calls-to-action",
                "Keep content concise and within the word count specified in prompts",
                "Use active voice and action-oriented language",
                "Format output in clean markdown for easy integration"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
        
    def _create_document_composer_agent(self):
        """Create an agent specialized in assembling the final document."""
        return Agent(
            name="Document Composer Agent",
            role="You are an expert at organizing and assembling content into cohesive documents",
            model=Claude(id="claude-3-7-sonnet-20250219", max_tokens=12000),
            instructions=[
                "Compile generated content from multiple sections into a cohesive document",
                "Organize content according to the provided structure",
                "Ensure consistency in tone, style, and formatting across sections",
                "Add necessary transitions between sections for smooth flow",
                "Format the document according to the requested output format (Markdown or HTML)",
                "Ensure proper heading hierarchy and document structure",
                "Remove any duplicative content or inconsistencies",
                "Maintain proper semantic structure for SEO optimization",
                "Include placeholder comments for any missing content",
                "Ensure the document follows accessibility best practices"
            ],
            show_tool_calls=True,
            stream=True,
            markdown=True,
        )
        
    async def crawl_website(self, url: str) -> Dict[str, Any]:
        """
        Crawl the target website to extract content.
        
        Args:
            url: The URL of the website to crawl
            
        Returns:
            Dict containing extracted website content
        """
        print(f"Crawling website: {url}")
        
        # Use requests library instead of Crawl4aiTools which has asyncio issues
        import requests
        from bs4 import BeautifulSoup
        
        try:
            # Get the website content
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content and clean it up
            # Remove script and style elements
            for script_or_style in soup(['script', 'style', 'header', 'footer', 'nav']):
                script_or_style.extract()
            
            # Extract text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            extracted_html = str(soup)
            
            # Now let's use our crawler agent to analyze the content
            prompt = f"""
            Please analyze the content from the website at {url}.
            
            Focus on extracting:
            1. Main value propositions and key messaging
            2. Product/service descriptions
            3. Benefits and features
            4. Customer testimonials and case studies
            5. Company information and unique selling points
            6. Any statistical data or industry insights
            7. Current calls-to-action and offers
            
            I've already downloaded the website content for you, so no need to crawl it.
            Here's a sample of the content (showing first and important parts):
            
            {text[:5000]}
            
            Structure your analysis into categories and provide a comprehensive summary
            of the site's main messaging. Format the result as structured data.
            """
            
            # Get the analysis from our agent
            response_stream = self.crawler_agent.run(prompt)
            content = ""
            
            # Handle streaming response by collecting all content
            if hasattr(response_stream, '__iter__') and not hasattr(response_stream, 'content'):
                for response_chunk in response_stream:
                    if hasattr(response_chunk, 'content'):
                        content += response_chunk.content
            else:
                # If it's already a RunResponse object with content
                content = response_stream.content if hasattr(response_stream, 'content') else str(response_stream)
                
            return {
                "url": url,
                "raw_content": text,
                "html_content": extracted_html[:100000],  # Limit to avoid huge strings
                "analysis": content,
                "extracted_data": self._parse_content(content)
            }
            
        except Exception as e:
            print(f"Error crawling website: {e}")
            return {
                "url": url,
                "raw_content": f"Error crawling website: {e}",
                "extracted_data": {}
            }
        
    def _parse_content(self, content: str) -> Dict[str, Any]:
        """Parse the extracted content into a structured format."""
        # In a real implementation, this would parse the Markdown/JSON response
        # from the crawler agent into a structured data format
        return {
            "parsed_content": content,
            "sections": {}  # Would contain categorized content
        }
        
    async def generate_section_content(self, section: Dict[str, Any], website_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content for a specific section using prompts from the mapping.
        
        Args:
            section: The section configuration from the mapping
            website_data: The extracted website data
            
        Returns:
            Dict containing the generated content for the section
        """
        section_name = section["section_name"]
        print(f"Generating content for section: {section_name}")
        
        section_content = {
            "name": section_name,
            "description": section["section_description"],
            "sub_sections": []
        }
        
        for sub_section in section["sub_sections"]:
            sub_name = sub_section["sub_section_name"]
            print(f"  Processing sub-section: {sub_name}")
            
            sub_content = {
                "name": sub_name,
                "description": sub_section["sub_section_description"],
                "content": ""
            }
            
            # Generate content for each prompt in the sub-section
            prompt_results = []
            for prompt_config in sub_section.get("prompts", []):
                prompt_id = prompt_config["id"]
                prompt_text = prompt_config["prompt_text"]
                
                # Enhance the prompt with website data
                enhanced_prompt = self._enhance_prompt_with_data(prompt_text, website_data)
                  # Generate content using the prompt
                response_stream = self.content_generator.run(enhanced_prompt)
                content = ""
                
                # Handle streaming response
                if hasattr(response_stream, '__iter__') and not hasattr(response_stream, 'content'):
                    for response_chunk in response_stream:
                        if hasattr(response_chunk, 'content'):
                            content += response_chunk.content
                else:
                    # If it's already a RunResponse object with content
                    content = response_stream.content if hasattr(response_stream, 'content') else str(response_stream)
                
                prompt_results.append({
                    "id": prompt_id,
                    "title": prompt_config["title"],
                    "generated_content": content
                })
            
            # Combine prompt results for this sub-section
            if prompt_results:
                combined_content = self._combine_prompt_results(prompt_results)
                sub_content["content"] = combined_content
            
            section_content["sub_sections"].append(sub_content)
        
        return section_content
        
    def _enhance_prompt_with_data(self, prompt: str, website_data: Dict[str, Any]) -> str:
        """Enhance the prompt with relevant data from the website."""
        # Extract relevant content from website_data based on semantic similarity
        # and append it to the prompt for context
        enhanced_prompt = f"""
        Based on the website data provided below, {prompt}
        
        WEBSITE ANALYSIS:
        {website_data.get('analysis', '')}
        
        WEBSITE RAW CONTENT SAMPLE:
        {website_data.get('raw_content', '')[:1000]}  # Using first 1000 chars for brevity
        
        Please generate the content following the instructions above.
        Make sure the content is concise, compelling, and aligns with the website's
        existing messaging and brand voice.
        """
        
        return enhanced_prompt
        
    def _combine_prompt_results(self, prompt_results: List[Dict[str, Any]]) -> str:
        """Combine the results from multiple prompts into cohesive content."""
        combined = "## Generated Content\n\n"
        
        for result in prompt_results:
            combined += f"### {result['title']}\n\n"
            combined += result['generated_content'] + "\n\n"
            
        return combined
        
    async def assemble_document(self, sections_content: List[Dict[str, Any]], output_format: str = "markdown") -> str:
        """
        Assemble all generated section content into a complete document.
        
        Args:
            sections_content: List of generated content for each section
            output_format: The desired output format ("markdown" or "html")
            
        Returns:
            String containing the complete assembled document
        """
        print("Assembling final document...")
        
        # Create a prompt for the document composer
        sections_json = json.dumps(sections_content, indent=2)
        
        prompt = f"""
        Please assemble the following generated content sections into a cohesive homepage document.
        
        The output should be in {output_format} format.
        
        Follow this process:
        1. Create a logical flow between sections
        2. Add any necessary transitions or connecting elements
        3. Ensure consistent formatting and style throughout
        4. Create a clear structure with appropriate heading hierarchy
        5. Remove any obvious duplication or inconsistencies
        
        GENERATED SECTIONS:
        {sections_json}
          Please provide the complete, assembled document in {output_format} format.
        """
        
        response_stream = self.document_composer.run(prompt)
        content = ""
        
        # Handle streaming response
        if hasattr(response_stream, '__iter__') and not hasattr(response_stream, 'content'):
            for response_chunk in response_stream:
                if hasattr(response_chunk, 'content'):
                    content += response_chunk.content
        else:
            # If it's already a RunResponse object with content
            content = response_stream.content if hasattr(response_stream, 'content') else str(response_stream)
            
        return content
        
    async def generate_homepage(self, url: str, output_format: str = "markdown") -> str:
        """
        Generate a complete homepage using the multi-agent system.
        
        Args:
            url: The URL of the website to analyze
            output_format: The desired output format ("markdown" or "html")
            
        Returns:
            String containing the complete homepage content
        """
        print(f"Starting homepage generation for URL: {url}")
        
        # Step 1: Crawl the website
        website_data = await self.crawl_website(url)
        
        # Step 2: Generate content for each section
        sections_content = []
        for section in self.mapping["homepage_sections"]:
            section_content = await self.generate_section_content(section, website_data)
            sections_content.append(section_content)
            
        # Step 3: Assemble the final document
        final_document = await self.assemble_document(sections_content, output_format)
        
        print("Homepage generation completed successfully.")
        return final_document
        
    def run_homepage_generator(self, url: str, output_format: str = "markdown") -> str:
        """
        Run the homepage generator for the given URL.
        
        Args:
            url: The URL of the website to analyze
            output_format: The desired output format ("markdown" or "html")
            
        Returns:
            String containing the complete homepage content
        """
        import asyncio
        
        try:
            # Check if we're already in an event loop
            try:
                loop = asyncio.get_running_loop()
                # We're inside an event loop, use a different approach
                print("Already inside an event loop, using create_task")
                
                async def run_generator():
                    try:
                        return await self.generate_homepage(url, output_format)
                    except Exception as e:
                        print(f"Error in run_generator: {e}")
                        return f"# Error during homepage generation: {e}"
                
                # Create and run the task
                task = loop.create_task(run_generator())
                
                # Wait for the task to complete (if we're in an async context)
                # This is a workaround that works in both sync and async contexts
                while not task.done():
                    loop.run_until_complete(asyncio.sleep(0.1))
                    
                return task.result()
                
            except RuntimeError:
                # No running event loop, use asyncio.run
                print("No running event loop, using asyncio.run")
                return asyncio.run(self.generate_homepage(url, output_format))
                
        except Exception as e:
            print(f"Error generating homepage: {e}")
            return f"# Error: {e}"
